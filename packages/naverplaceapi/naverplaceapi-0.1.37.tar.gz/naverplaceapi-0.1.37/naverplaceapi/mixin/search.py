import json
import urllib
import urllib.parse
import urllib.request


class SearchMixin:
    CLIENT_ID = "ak4jckPbdjMcrMmFDSgv"
    CLIENT_SECRET = "Ye3VCcl2in"
    def all_search(self,
                  query,
                  type,  # ex) all/place
                  searchCoord, #    ex. 126.942428;37.485309
                  boundary = None
                  ):
        encoded_keyword = urllib.parse.quote(query)
        # url = f"https://openapi.naver.com/v1/search/local.json?query={encoded_keyword}&display={page_size}"
        url = f"https://map.naver.com/p/api/search/allSearch?query={encoded_keyword}&type={type}&searchCoord={searchCoord}&boundary={boundary}"
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        rescode = response.getcode()

        if rescode == 200:
            response_body = response.read()
            results = json.loads(response_body)
            return results['result']
        else:
            return None
    def search(self,
               keyword: str, page_size: int = 5,
               start:int = 10,
               client_id: str = CLIENT_ID, client_secret: str = CLIENT_SECRET,
               proxies=None):
        encoded_keyword = urllib.parse.quote(keyword)
        url = f"https://openapi.naver.com/v1/search/local.json?query={encoded_keyword}&display={page_size}&start=5"

        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id", client_id)
        request.add_header("X-Naver-Client-Secret", client_secret)
        response = urllib.request.urlopen(request)
        rescode = response.getcode()

        result_list = []
        if rescode == 200:
            response_body = response.read()
            results = json.loads(response_body)['items']

            for result in results:
                result['title'] = result['title'].replace('<b>', '').replace('</b>', '')
                result_list.append(result)
        return result_list
    def search_blog(self,
               keyword: str, page_size: int = 5,
               client_id: str = CLIENT_ID, client_secret: str = CLIENT_SECRET,
               proxies=None):
        encoded_keyword = urllib.parse.quote(keyword)
        url = f"https://openapi.naver.com/v1/search/blog.json?query={encoded_keyword}&display={page_size}"

        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id", client_id)
        request.add_header("X-Naver-Client-Secret", client_secret)
        response = urllib.request.urlopen(request)
        rescode = response.getcode()

        result_list = []
        if rescode == 200:
            response_body = response.read()
            results = json.loads(response_body)['items']

            for result in results:
                result['title'] = result['title'].replace('<b>', '').replace('</b>', '')
                result_list.append(result)
        return result_list
