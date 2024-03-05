import json
import re
from urllib.parse import urlencode

import pandas as pd
import time
from selenium.common import NoSuchElementException
from seleniumwire import webdriver as wired_webdriver
from selenium import webdriver
from seleniumwire import webdriver, utils
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from rotate_ip_aws_gw.ip_rotator import ApiGateway
from . import query
from .utils import HEADERS, parse_naver_var_in_script_texts


def wait_for_graphql_response(driver,
                              max_attempts=10,
                              waiting_time=2
                              ):
    current_attempt = 0

    while current_attempt < max_attempts:
        need_to_waiting = False
        for request in driver.requests:
            request_url = request.url
            if "graphql" not in request_url:
                continue
            if request.response is None:
                need_to_waiting = True
                break
        if need_to_waiting == False:
            break
        time.sleep(waiting_time)


def get_value_by_path(data, path):
    keys = path.split('.')  # 경로를 점을 기준으로 분할하여 리스트 생성
    result = data

    for key in keys:
        if isinstance(result, dict) and key in result:
            result = result[key]
        else:
            return None  # 경로를 따라가는 동안 오류 발생 시 None 반환

    return result


def extract_naver_var(html_text):
    soup = BeautifulSoup(html_text, "html.parser", from_encoding="utf-8")
    scripts = soup.find_all("script")

    naver_var = parse_naver_var_in_script_texts(scripts)
    variable_name = 'window.__APOLLO_STATE__'
    pattern = re.compile(rf'\b{re.escape(variable_name)}\s*=\s*(.*?)(\n)')
    match = pattern.search(naver_var)

    if match is None:
        return None
    # 첫페이지
    data = match.group(1)
    json_data = json.loads(data[:-1])
    return json_data


def collect_graphql_responses(driver):
    responses = []
    for request in driver.requests:
        request_url = request.url
        if "graphql" not in request_url:
            continue
        response = utils.decode(
            request.response.body,
            request.response.headers.get("Content-Encoding", "identity")
        )
        response = response.decode("utf8")
        json_data = json.loads(response)
        responses.append(json_data)
    return responses


class PlaceMixin:
    def search_places(self, keyword: str, page_no: int, page_size: int, proxies=None):
        data = query.get_restaurants.create(keyword, page_no, page_size)
        response = requests.post("https://pcmap-api.place.naver.com/graphql", headers=HEADERS, data=json.dumps(data),
                                 proxies=proxies)
        response.raise_for_status()
        response_data = response.json()
        graphql_data = response_data['data']['restaurants']
        return graphql_data

    def _get_tor_session(self):
        # initialize a requests Session
        session = requests.Session()
        # this requires a running Tor service in your machine and listening on port 9050 (by default)
        session.proxies = {"http": "socks5://localhost:9150", "https": "socks5://localhost:9150"}
        # session.proxies = {'http': 'http://67.43.227.229:29003', 'https':'https://67.43.227.229:29003'}
        return session

    def get_place(self,
                  business_id,
                  use_tor:bool=True,
                  tor_port:int=9150,
                  proxies=None):
        # url = f"https://pcmap.place.naver.com/restaurant/{business_id}/home"
        url = "https://pcmap.place.naver.com/restaurant/{}".format(business_id)

        if use_tor:
            session = self._get_tor_session()
            ip = session.get("http://icanhazip.com").text
            response = session.get(url)
            # proxies = {"http": f"socks5://localhost:{tor_port}", "https": f"socks5://localhost:{tor_port}"}
        else:
            response = requests.get(url, proxies=proxies)
        response.raise_for_status()
        html_text = response.content

        broadcasts = self.__parse_broadcast_in_html(html_text)
        return broadcasts

    def get_restaurant(self, business_id, proxies):
        data = query.get_restaurant.create(business_id)
        response = requests.post("https://pcmap-api.place.naver.com/graphql", headers=HEADERS, data=json.dumps(data),
                                 proxies=proxies)
        response.raise_for_status()
        response_data = response.json()
        graphql_data = response_data['data']
        return graphql_data

    def __parse_broadcast_in_html(self, html_text: str):
        soup = BeautifulSoup(html_text, "html.parser", from_encoding="utf-8")
        scripts = soup.find_all("script")

        naver_var = parse_naver_var_in_script_texts(scripts)
        variable_name = 'window.__APOLLO_STATE__'
        pattern = re.compile(rf'\b{re.escape(variable_name)}\s*=\s*(.*?)(\n)')
        match = pattern.search(naver_var)

        if match:
            data = match.group(1)
            return json.loads(data[:-1])
        else:
            return None

    def get_place_summary(self, id: str, proxies=None):
        url = f"https://map.naver.com/v5/api/sites/summary/" + id + "?lang=ko"
        data = {
            "language": 'kor',
            "order_by": "2"
        }
        response = requests.get(url, data=data, proxies=proxies)
        response.raise_for_status()
        resposne_data = response.json()
        resposne_data['_id'] = id
        return resposne_data

    def get_menus(self, business_id, proxies=None):
        url = f"https://pcmap.place.naver.com/restaurant/{business_id}/menu/list"
        response = requests.get(url, proxies=proxies)
        response.raise_for_status()
        html_text = response.content
        menus = self.__parse_menus_internal(html_text)
        result = {
            "business_id": business_id,
            "menus": menus
        }
        return result

    def __parse_menus_internal(self, html_text: str):
        soup = BeautifulSoup(html_text, "html.parser", from_encoding="utf-8")
        scripts = soup.find_all("script")
        naver_string = None

        for s in scripts:
            if s.string is None:
                continue
            if "var naver=" in s.string:
                naver_string = s.string

        menu_regex = re.compile(r'\{"__typename":"Menu".*?\}')
        menu_string_list = re.findall(menu_regex, naver_string)

        # 일반
        menus = []
        for menu_string in menu_string_list:
            menu_json = json.loads(menu_string)
            menu = {
                "name": menu_json["name"],
                "price": menu_json["price"],
                "description": menu_json["description"],
                "imageUrl": menu_json["images"][0] if menu_json["images"] else "",
                "isRecommended": menu_json["recommend"],
            }
            menus.append(menu)
        # baemin
        baemin_menu_regex = re.compile(r'\{"__typename":"BaeminMenu".*?\}')
        baemin_menu_string_list = re.findall(baemin_menu_regex, naver_string)

        for baemin_menu_string in baemin_menu_string_list:
            baemin_menu_json = json.loads(baemin_menu_string)
            menu = {
                "name": baemin_menu_json["name"],
                "price": baemin_menu_json["price"],
                "imageUrl": menu_json["images"][0] if menu_json["images"] else "",

            }
            menus.append(menu)
        return menus

    def search_keyword_in_html(self,
                               keyword, # 관심지역내 검색 키워드
                               x=None,  # 관심지역내 검색 중심 위치 좌표
                               y=None,  # 관심지역내 현재 중심 위치 좌표
                               bounds=None,   # 관심지역 좌표영역(좌하단 좌표, 우상단 좌표)
                               is_current_location_search=True, # 주변 지역 검색 포함 여부
                               is_headless=True,  # Selenium, 브라우저 출력 여부
                               interval_page=3,
                               use_tor= False,
                               tor_port= 9150,
                               aws_api_gw_endpoint=None,
                               proxies=None): # 프록시 서버 사용 여부
        params = {
            'query': keyword,
            "x": x,
            'y': y,
            'clientX': x,
            'clientY': y,
            'bounds': bounds,
            'isCurrentLocationSearch': is_current_location_search
        }
        encoded_params = urlencode(params)
        base_url = "https://pcmap.place.naver.com/restaurant/list"
        url = base_url + '?' + encoded_params

        options = webdriver.ChromeOptions()
        options.add_argument('--disable-dev-shm-usage')
        if is_headless is True:
            options.add_argument('headless')
            options.add_argument('--no-sandbox')
        seleniumwire_options = {}
        if use_tor is True:
            seleniumwire_options['proxy'] = {
                'http':f'socks5://127.0.0.1:{tor_port}',
                'https':f'socks5://127.0.0.1:{tor_port}',
                'no_proxy': 'localhost,127.0.0.1'
            }
        driver = wired_webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                                        options=options,
                                        seleniumwire_options=seleniumwire_options)
        driver.get("http://icanhazip.com")
        html_text = driver.page_source
        try:
            if aws_api_gw_endpoint is None:

                def request_interceptor(request):
                    if "cc.naver.com" in request.host:
                        request.abort()
                    if "sentry" in request.host:
                        request.abort()
                    if "search.pstatic.net" in request.host:
                        request.abort()
                    if request.path.endswith(('.png', '.jpg', '.gif', 'jpeg', "css")):
                        request.abort()

                driver.request_interceptor = request_interceptor
                driver.get(url)
            else:
                gw = ApiGateway(site='')
                gw.getAsSelenium(driver, url, aws_api_gw_endpoint)
        except Exception as e:
            driver.quit()
            return {
                'html_text': None,
                'restaurants': [],
                'ad_business': [],
                'naver_var': None
            }
        html_text = driver.page_source
        try:
            pagination_element = driver.find_element(By.CLASS_NAME, "zRM9F")
        except NoSuchElementException as e:
            driver.quit()
            return {
                'html_text': html_text,
                'restaurants': [],
                'ad_business': [],
                'naver_var': None
            }
        child_elements = pagination_element.find_elements(By.XPATH, "./*")

        def move_second_to_last(arr):
            if len(arr) >= 2:
                second_element = arr.pop(1)
                arr.append(second_element)
            return arr

        # 두 번째 요소를 가져옵니다.
        child_elements = move_second_to_last(child_elements)

        for child_element in child_elements[1:]:
            try:
                if child_element.aria_role != 'button':
                    continue
                child_element.click()
                time.sleep(interval_page)
            except NoSuchElementException as e:
                pass

        wait_for_graphql_response(driver)
        graphql_responses = collect_graphql_responses(driver)
        naver_var = extract_naver_var(html_text)

        restaurants = []
        ad_business = []
        for graphql_response in graphql_responses:
            for response in graphql_response:
                restaurants_response = get_value_by_path(response, "data.restaurants")
                if restaurants_response is not None:
                    restaurants.append(restaurants_response)

                ad_business_response = get_value_by_path(response, "data.adBusinesses")
                if ad_business_response is not None:
                    ad_business.append(ad_business_response)
        driver.close()
        return {
            'html_text': html_text,
            'restaurants': restaurants,
            'ad_business': ad_business,
            'naver_var': naver_var
        }

    def search_keyword_in_html_in_first_page(self, keyword, x=None, y=None, bounds=None, proxies=None):
        url = "https://pcmap.place.naver.com/restaurant/list?query={}".format(keyword)
        # url = 'https://map.naver.com/v5/search/'
        response = requests.get(url,
                                params={
                                    "x": x,
                                    'y': y,
                                    'clientX': x,
                                    'clientY': y,
                                    'bounds': bounds
                                },
                                proxies=proxies)
        response.raise_for_status()
        html_text = response.content
        soup = BeautifulSoup(html_text, "html.parser", from_encoding="utf-8")
        scripts = soup.find_all("script")

        naver_var = parse_naver_var_in_script_texts(scripts)
        variable_name = 'window.__APOLLO_STATE__'
        pattern = re.compile(rf'\b{re.escape(variable_name)}\s*=\s*(.*?)(\n)')
        match = pattern.search(naver_var)

        if match is None:
            return None

        data = match.group(1)
        json_data = json.loads(data[:-1])

        return json_data
    #
    #
    # def search_keyword_in_bound(self, keyword, x, y, bound):
