import requests

from .utils import HEADERS


class CategoryMixin:
    def get_categories(self,
                       keyword: str,
                       search_use: bool = True,
                       nmb_use: bool = True,
                       only_leaf: bool = True,
                       project_place_brand: bool = True,
                       is_use_keyword_like_match: bool = False,
                       proxies=None):
        parameters = {
            'search': keyword,
            'searchUse': search_use,
            'nmbUse': nmb_use,
            'onlyLeaf': only_leaf,
            'projectPlaceBrand': project_place_brand,
            'isUseKeywordLikeMatch': is_use_keyword_like_match
        }
        response = requests.get("https://new.smartplace.naver.com/api/pbp/public/categories",
                                headers=HEADERS,
                                params=parameters,
                                proxies=proxies)
        response.raise_for_status()
        response_data = response.json()
        return response_data
