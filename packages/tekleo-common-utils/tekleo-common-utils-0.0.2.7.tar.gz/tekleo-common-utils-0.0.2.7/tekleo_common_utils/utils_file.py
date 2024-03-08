from injectable import injectable
import requests
from requests.auth import HTTPBasicAuth


@injectable
class UtilsFile:
    def open_file_to_bytes(self, file_path: str):
        file = open(file_path, 'rb')
        binary_content = file.read(-1)
        file.close()
        return binary_content

    def download_file_to_bytes(self, file_url: str, basic_auth_username: str = '', basic_auth_password: str = ''):
        response = None
        use_basic_auth = len(basic_auth_username) > 0 and len(basic_auth_password) > 0
        if use_basic_auth:
            response = requests.get(file_url, auth=HTTPBasicAuth(basic_auth_username, basic_auth_password))
        else:
            response = requests.get(file_url)
        return response.content
