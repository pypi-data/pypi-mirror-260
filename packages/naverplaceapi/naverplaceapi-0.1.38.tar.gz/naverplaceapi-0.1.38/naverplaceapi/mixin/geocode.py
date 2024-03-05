import requests


class GeocodeMixin:
    def geocode(self, query: str, lon: float = None, lat: float = None, proxies=None):
        params = {
            'query': query,
            # 'coordinate': f'{lon},{lat}'
        }
        headers = {
            "X-NCP-APIGW-API-KEY-ID": "ufwgfnnu1l",
            "X-NCP-APIGW-API-KEY": "xQUQeO7a09VHRM5ecrqUClVzkM3mxV2vrlAVMAh1"
        }
        response = requests.get("https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode",
                                 params=params,
                                 headers=headers,
                                 proxies=proxies)
        response.raise_for_status()
        response_data = response.json()
        return response_data
