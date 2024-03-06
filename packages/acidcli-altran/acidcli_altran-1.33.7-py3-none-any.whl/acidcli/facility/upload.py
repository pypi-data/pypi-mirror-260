# Copyright Capgemini Engineering B.V.

"""upload.

Upload json or files to url
"""
import requests
from requests import RequestException
from loguru import logger

from acidcli.exceptions import CLIError


# pylint: disable=too-few-public-methods
class Upload:
    """Class to handle uploading of data."""

    def __init__(self, api_key=None, bearer_token=None, username=None, password=None):
        """Initialize credentials for upload."""
        self.auth_header = None

        if api_key is not None:
            self.auth_header = {"X-API-KEY": api_key}

        if bearer_token is not None:
            self.auth_header = {"Authorization": f"Bearer {bearer_token}"}

        if self.auth_header is None:
            if username is None or password is None:
                raise CLIError("Error during upload, Credentials are not found?")
            self.username = username
            self.password = password

    def upload_file(self, url, data_stream):
        """upload_file.

        Uploads files to url

        :param url: url to upload to
        :param data_stream: data_stream to upload
        """
        logger.info(f"Uploading File to {url}")

        self.__upload_put(url, data_stream=data_stream)

    def upload_nuget_package(self, url, packages):
        """upload_nuget_package.

        Uploads NuGet package to url

        :param url: url to upload to
        :param packages: packages to upload
        """
        logger.info(f"Uploading Nuget Package to {url}")

        try:
            self.__upload_put(url, files=packages)
        except CLIError as error:
            logger.warning("Are you redeploying the same Nuget package again?")
            raise CLIError(error) from error

    def upload_json(self, url, json):
        """upload_json.

        Uploads json to url

        :param url: url to upload to
        :param json: json to upload
        """
        logger.debug(f"Uploading json to {url}")

        self.__upload_post(url, json=json)

    def download_json(self, url, params=None):
        """download_json.

        Downloads json from url

        :param url: url to download from
        :param params: parameters to send in request
        :return: json loaded to object
        """
        logger.debug(f"Downloading json from {url}")

        return self.__download_get(url, params=params).json()

    def __upload_post(self, url, json=None, files=None):
        """__upload_post.

        Uploads files and json to url

        :param url: url to upload to
        :param json: json to upload
        :param files: files to upload
        """
        try:
            if self.auth_header is not None:
                header = self.auth_header
                response = requests.post(url, headers=header, files=files, json=json, timeout=30)
            else:
                response = requests.post(url, auth=(self.username, self.password), files=files, json=json, timeout=30)
        except RequestException as error:
            raise CLIError(error) from error

        if not response.ok:
            raise CLIError(f"Requests error response: HTTP {response.status_code}, {response.reason}")

    def __download_get(self, url, params):
        """__download_get.

        Download data from url

        :param url: url to download from
        :param params: parameters to pass
        :return: response
        """
        try:
            if self.auth_header is not None:
                header = self.auth_header
                response = requests.get(url, headers=header, params=params, timeout=30)
            else:
                response = requests.get(url, auth=(self.username, self.password), params=params, timeout=30)
        except RequestException as error:
            raise CLIError(error) from error

        if not response.ok:
            raise CLIError(f"Requests error response: HTTP {response.status_code}, {response.reason}")

        return response

    def __upload_put(self, url, data_stream=None, files=None):
        """__upload_put.

        Uploads files and json to url

        :param url: url to upload to
        :param data_stream: data_stream to upload
        """
        try:
            response = requests.put(
                url, auth=(self.username, self.password), data=data_stream, files=files, timeout=30
            )
        except RequestException as error:
            raise CLIError(error) from error

        if not response.ok:
            raise CLIError(f"Requests error response: HTTP {response.status_code}, {response.reason}")


# pylint: enable=too-few-public-methods
