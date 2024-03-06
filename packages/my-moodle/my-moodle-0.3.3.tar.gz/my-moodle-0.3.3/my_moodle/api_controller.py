"""
Copyright © 2024 Mark Crowe <https://github.com/marcocrowe>. All rights reserved.
API Controller Class
"""

import json
import requests
from my_moodle.moodle_api_functions import MoodleApiFunctions


class ApiController:
    """Api Controller"""

    WEB_SERVICE_PATH: str = "webservice/rest/server.php"

    def __init__(
        self, server: str, token: str, rest_format: str = "json", timeout: float = 300.0
    ):
        self._moodle_url: str = (
            f"{server}/{self.WEB_SERVICE_PATH}?wstoken={token}&moodlewsrestformat={rest_format}"
        )
        self._timeout: float = timeout
        self._token: str = token

    @property
    def moodle_url(self):
        """Moodle URL

        Returns:
            str: The Moodle URL
        """
        return self._moodle_url

    @property
    def timeout(self) -> float:
        """Timeout

        Returns:
            float: The timeout
        """
        return self._timeout

    @timeout.setter
    def timeout(self, value: float) -> None:
        """Set the timeout

        Args:
            value (float): The timeout
        """
        self._timeout = value

    @property
    def token(self) -> str:
        """Token

        Returns:
            str: The token
        """
        return self._token

    def call_moodle_api(self, function_name: str, params: dict) -> list:
        """Call a Moodle API function

        Args:
            function_name (str): The function name
            params (dict): The parameters

        Returns:
            dict: The result
        """
        url = f"{self.moodle_url}&wsfunction={function_name}"
        response: requests.Response = requests.post(
            url, params=params, timeout=self.timeout
        )
        return json.loads(response.content)

    def get_course_contents(self, course_id: str) -> list:
        """Get contents from a course

        Args:
            course_id (str): The course id

        Returns:
            list: A json list of contents
        """
        params = {"courseid": course_id}
        return self.call_moodle_api(MoodleApiFunctions.CORE_COURSE_GET_CONTENTS, params)

    def get_course_enrolled_users(self, course_id: str) -> list:
        """Get enrolled users in a course

        Args:
            course_id (str): The course id

        Returns:
            list: A json list of enrolled users
        """
        params = {"courseid": course_id}
        return self.call_moodle_api(
            MoodleApiFunctions.CORE_ENROL_GET_ENROLLED_USERS, params
        )

    def get_enrolled_courses(self) -> list:
        """Get all course you have enrolled on

        Returns:
            list
        """
        params = {"classification": "inprogress"}
        return self.call_moodle_api(
            MoodleApiFunctions.CORE_COURSE_GET_ENROLLED_COURSES_BY_TIMELINE_CLASSIFICATION,
            params,
        )
