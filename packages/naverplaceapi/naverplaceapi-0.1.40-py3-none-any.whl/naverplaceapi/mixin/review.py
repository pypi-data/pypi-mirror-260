import json
import math
import re

from selenium.common import NoSuchElementException, StaleElementReferenceException
from seleniumwire import webdriver, utils
from selenium import webdriver
import time
import requests
from bs4 import BeautifulSoup
from seleniumwire import webdriver as wired_webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from naverplaceapi.mixin.utils import HEADERS, parse_naver_var_in_script_texts
from . import query
from ..tor_manager import tor_manager


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
    if naver_var is None:
        return None

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
        if "too many request" in response:
            tor_manager.new_identity()

        json_data = json.loads(response)
        responses.append(json_data)
    return responses



def extract_graphql_request(driver):
    for request in driver.requests:
        request_url = request.url
        if "graphql" not in request_url:
            continue
        return request
    return None


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


def _request_get_fsas_review_like_selenium(driver, place_id, page_no, page_cnt):
    # 수정된 요청 보내기
    import requests
    data = query.get_fsas_reviews.create(place_id, page_no, page_cnt)

    # 요청 새 세션 생성
    s = requests.Session()
    # Selenium Cookie 획득
    cookies = driver.get_cookies()
    for cookie in cookies:
        s.cookies.set(cookie['name'], cookie['value'])

    # 블로그 정보 요청 GraphQL의 헤더 정보를 획득
    request_headers = None
    graphql_request = extract_graphql_request(driver)
    if graphql_request is not None:
        request_headers = graphql_request.headers

    # 이전 요청과 동일한 형식으로 데이터 요청
    response = s.post("https://pcmap-api.place.naver.com/graphql", headers=request_headers, data=json.dumps(data))
    return response


def _request_get_visitor_review_like_selenium(driver, place_id, page_no, page_cnt):
    # 수정된 요청 보내기
    import requests
    data = query.get_visitor_reviews.create(place_id, page_no, page_cnt)

    # 요청 새 세션 생성
    s = requests.Session()
    # Selenium Cookie 획득
    cookies = driver.get_cookies()
    for cookie in cookies:
        s.cookies.set(cookie['name'], cookie['value'])

    # 블로그 정보 요청 GraphQL의 헤더 정보를 획득
    request_headers = None
    graphql_request = extract_graphql_request(driver)
    if graphql_request is not None:
        request_headers = graphql_request.headers

    # 이전 요청과 동일한 형식으로 데이터 요청
    response = s.post("https://pcmap-api.place.naver.com/graphql", headers=request_headers, data=json.dumps(data))
    return response


class ReviewMixin:
    def get_visitor_reviews(self, business_id: str, page_no: int, page_cnt: int, proxies=None):
        data = query.get_visitor_reviews.create(business_id, page_no, page_cnt)
        response = requests.post("https://pcmap-api.place.naver.com/graphql", headers=HEADERS, data=json.dumps(data),
                                 proxies=proxies)
        response.raise_for_status()
        response_data = response.json()
        graphql_data = response_data['data']['visitorReviews']
        if graphql_data is None:
            graphql_data = {}
        # ['visitorReviews']
        graphql_data['business_id'] = business_id
        return graphql_data

    def get_ugc_reviews(self, business_id: str, page_no: int, page_cnt: int, proxies=None):
        data = query.get_ugc_reviews.create(business_id, page_no, page_cnt)
        response = requests.post("https://pcmap-api.place.naver.com/graphql", headers=HEADERS, data=json.dumps(data),
                                 proxies=proxies)
        response.raise_for_status()
        response_data = response.json()
        graphql_data = response_data['data']['restaurant']['fsasReviews']
        graphql_data['business_id'] = business_id
        return graphql_data

    def get_visitor_review_stats(self, business_id: str, proxies=None):
        data = query.get_visitor_review_stats.create(business_id)
        response = requests.post("https://pcmap-api.place.naver.com/graphql", headers=HEADERS, data=json.dumps(data),
                                 proxies=proxies)
        response.raise_for_status()
        response_data = response.json()
        graphql_data = response_data['data']['visitorReviewStats']
        if graphql_data is None:
            return None
        graphql_data['_id'] = graphql_data['id']
        graphql_data['business_id'] = business_id
        return graphql_data

    def get_visitor_review_photos_in_visitor_review_tab(self, store_id: str, page_no: int, page_size: int,
                                                        proxies=None):
        data = query.get_visitor_review_photos_in_visitor_review_tab.create(store_id, page_no, page_size)
        response = requests.post("https://pcmap-api.place.naver.com/graphql", headers=HEADERS, data=json.dumps(data),
                                 proxies=proxies)
        response.raise_for_status()
        response_data = response.json()
        graphql_data = response_data['data']['visitorReviews']
        if graphql_data is None:
            graphql_data = {}
        graphql_data['business_id'] = store_id
        return graphql_data

    def get_visitor_review_theme_lists(self, store_id: str, page_no, page_size, proxies=None):
        data = query.get_visitor_review_theme_lists.create(store_id, page_no, page_size)
        response = requests.post("https://pcmap-api.place.naver.com/graphql", headers=HEADERS, data=json.dumps(data),
                                 proxies=proxies)
        response.raise_for_status()
        response_data = response.json()
        graphql_data = response_data['data']['themeLists']
        graphql_data['business_id'] = store_id

        return graphql_data

    def get_blog_reviews_in_html(self,
                                 business_id: str,
                                 page_no=1,
                                 page_size=10,
                                 use_tor:bool =False,
                                 tor_port:int =9150,
                                 proxies=None):
        page_size = max(min(page_size, 10), 1)
        
        # Selenium Option 설정
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-dev-shm-usage')
        # options.add_argument('headless')
        options.add_argument('--no-sandbox')
        seleniumwire_options = {}
        if use_tor is True:
            seleniumwire_options['proxy'] = {
                'http': f'socks5://127.0.0.1:{tor_port}',
                'https': f'socks5://127.0.0.1:{tor_port}',
                'no_proxy': 'localhost,127.0.0.1'
            }

        driver = wired_webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                                        options=options,
                                        seleniumwire_options=seleniumwire_options)

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
        url = "https://pcmap.place.naver.com/restaurant/{}/review/ugc?type=photoView".format(business_id)
        driver.get(url)

        html_text = driver.page_source
        naver_var = extract_naver_var(html_text)
        if naver_var is None:
            tor_manager.new_identity()
            driver.clone()
            return None;

        # 페이지 로딩을 위해 잠시 대기합니다.
        # JavaScript를 사용하여 스크롤을 페이지의 가장 아래로 내립니다.

        interval_page = 6
        try:
            pagination_element = driver.find_element(By.CLASS_NAME, "fvwqf")
            max_try = 12
            try_count = 0
            while pagination_element is not None:
                time.sleep(interval_page)
                pagination_element.click()
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                pagination_element = driver.find_element(By.CLASS_NAME, "fvwqf")
                if try_count == max_try:
                    break
                try_count += 1
        except NoSuchElementException as e:
            pass
        except StaleElementReferenceException as e:
            pass

        wait_for_graphql_response(driver)
        graphql_responses = collect_graphql_responses(driver)

        blogs = []
        for graphql_response in graphql_responses:
            for response in graphql_response:
                blogs_response = get_value_by_path(response, "data.fsasReviews")
                if blogs_response is not None:
                    blogs.append(blogs_response)

        driver.close()
        return {
            'html_text': html_text,
            'blogs': blogs,
            'naver_var': naver_var
        }



        # 안댐...
        # gql_response = _request_get_fsas_review_like_selenium(driver, business_id, page_no, page_size)
        # gql_response.raise_for_status()
        # response_data = gql_response.json()
        # graphql_data = response_data['data']['fsasReviews']
        # graphql_data['business_id'] = business_id
        # return graphql_data

    def get_visitor_reviews_in_html(self,
                                    business_id: str,
                                    page_no=1,
                                    page_size=10,
                                    use_tor:bool = False,
                                    tor_port:int = 9150,
                                    proxies=None):
        page_size = max(min(page_size, 10), 1)

        options = webdriver.ChromeOptions()
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('headless')
        options.add_argument('--no-sandbox')

        if use_tor is True:
            tor_host = f'socks5://127.0.0.1:{tor_port}'
            options.add_argument(f'--proxy-server={tor_host}')

        driver = wired_webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        def request_interceptor(request):
            if request.path.endswith(('.png', '.jpg', '.gif', 'jpeg')):
                request.abort()

        driver.request_interceptor = request_interceptor

        url = "https://pcmap.place.naver.com/restaurant/{}/review/ugc?type=photoView".format(business_id)
        driver.get(url)
        time.sleep(4)
        gql_response = _request_get_visitor_review_like_selenium(driver, business_id, page_no, page_size)

        gql_response.raise_for_status()
        response_data = gql_response.json()
        graphql_data = response_data['data']['fsasReviews']
        graphql_data['business_id'] = business_id
        return graphql_data
