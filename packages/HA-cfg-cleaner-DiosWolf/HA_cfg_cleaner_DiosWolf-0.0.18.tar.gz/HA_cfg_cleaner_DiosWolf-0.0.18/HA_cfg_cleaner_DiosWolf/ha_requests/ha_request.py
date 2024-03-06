from requests import post, Response
from HA_cfg_cleaner_DiosWolf.data_classes_json.file_config import HostInfo


class HARequests:
    def __init__(self, configuration: HostInfo):
        self.configuration = configuration

    def __set_url(self) -> str:
        url = (
            self.configuration.host
            + ":"
            + self.configuration.port
            + self.configuration.automations_off_url
        )
        return url

    def __set_header_auth(self, headers: dict[str, any]) -> dict[str, any]:
        auth_headers = {"Authorization": self.configuration.api_key}
        auth_headers = auth_headers | headers
        return auth_headers

    def post_requests(
        self, data: dict[str, any], headers: dict[str, any] = {}
    ) -> Response:
        url = self.__set_url()
        auth_headers = self.__set_header_auth(headers)
        with post(url, headers=auth_headers, json=data) as resp:
            return resp
