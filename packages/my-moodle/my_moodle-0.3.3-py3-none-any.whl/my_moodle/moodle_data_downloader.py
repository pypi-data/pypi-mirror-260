"""
Copyright © 2024 Mark Crowe <https://github.com/marcocrowe>. All rights reserved.
Moodle data downloader Class
"""

from pathlib import Path
import os
import re
import requests

from my_moodle.json_utility import JsonUtility
from my_moodle.moodle_data_utility import MoodleDataUtility
from my_moodle.api_controller import ApiController
from my_moodle.csv_utility import CsvUtility
from my_moodle.enrolled_users_fields import EnrolledUsersFields


class MoodleDataDownloader:
    """Moodle data downloader"""

    def __init__(
        self,
        program_name: str,
        server: str,
        token: str,
        data_dir: str = "data",
        test_data_dir: str = "test-data",
        debug: bool = False,
        timeout: float = 300.0,
        rest_format: str = "json",
    ):
        self.program_name = program_name
        self._api_controller: ApiController = ApiController(
            server, token, rest_format, timeout
        )
        """Test data directory"""
        self._test_data_dir: str = test_data_dir
        self.data_dir = data_dir
        self.debug = debug

    @property
    def api_controller(self) -> ApiController:
        """API controller

        Returns:
            ApiController: The API controller
        """
        return self._api_controller

    @property
    def test_data_dir(self) -> str:
        """Test data directory

        Returns:
            str: The test data directory
        """
        return self._test_data_dir

    def create_directory(self, directory: str) -> str:
        """Create a directory

        Args:
            directory (str): The directory to create

        Returns:
            str: The directory path
        """
        directory_path = Path(self.data_dir, directory)
        os.makedirs(directory_path, exist_ok=True)
        return directory_path.absolute()

    def download_my_data(self):
        """Download my data"""
        courses = self.download_courses()
        self.download_courses_contents(courses)

    def download_courses_contents(self, courses: list) -> None:
        """Download courses contents

        Args:
            courses (list): The courses
        """
        for course in courses:
            if course.get("coursecategory") != "N-TUTORR":
                course_id: str = course.get("id", "")
                course_name: str = MoodleDataUtility.parse_course_name(course)
                directory_path: str = self.create_directory(course_name)

                self.download_enrolled_students(
                    course_id,
                    course_name,
                    Path(directory_path, "enrolled-students.csv").absolute(),
                )
                self.download_course_contents(course_id, directory_path, course_name)

    def download_course_contents(
        self, course_id: str, directory_path: str, course_name: str
    ) -> None:
        """Download all files from a course

        Args:
            course_id (str): The course id
            directory_path (str): The directory path
        """
        course_files = self.api_controller.get_course_contents(course_id)

        if self.debug:
            os.makedirs(self.test_data_dir, exist_ok=True)

            JsonUtility.save_json_to_file(
                course_files,
                Path(directory_path, f"{course_name}-contents.json").absolute(),
            )

        files = MoodleDataUtility.process_course_contents_to_file_list(course_files)

        for file in files:
            print(
                "id:",
                file["id"],
                ", ",
                "Filename:",
                file["name"],
                ",",
                "URL:",
                file["url"],
            )
            file_name: str = (
                f"{file['filenumber']:02d}-{self.cleaned_filename(file['name'])}"
            )
            file_path: Path = Path(directory_path, file_name)
            file_url: str = (
                f"{file['url']}?forcedownload=1&token={self.api_controller.token}"
            )
            self.download_file(
                file_url, file_path.absolute(), self.api_controller.timeout
            )

    @staticmethod
    def cleaned_filename(filename: str) -> str:
        """Generate a clean filename.
        Removes illegal characters and replaces spaces with spaces.
        Collapses multiple whitespaces into one.

        Args:
            filename (str): The filename

        Returns:
            str: The generated filename
        """
        # Define the pattern to match illegal characters
        illegal_chars_pattern = r'[/:*?"<>|\\\0-\x1f\x7f]'

        # Replace illegal characters with an empty string
        cleaned_filename = re.sub(illegal_chars_pattern, " ", filename)

        # Remove leading/trailing whitespaces and collapse multiple whitespaces into one
        cleaned_filename = re.sub(r"\s+", " ", cleaned_filename).strip()

        # Replace spaces with underscores
        cleaned_filename = cleaned_filename.replace(" ", "-")

        return cleaned_filename

    @staticmethod
    def download_file(file_url: str, save_path: str, timeout: float) -> None:
        """Download a file from Moodle"""
        try:
            response = requests.get(file_url, stream=True, timeout=timeout)
            response.raise_for_status()

            if response.status_code == 200:
                with open(save_path, "wb") as file:
                    for chunk in response.iter_content(1024):
                        file.write(chunk)
                print(f"Saved to: {save_path}")
            else:
                print("Download refused:", response.status_code)
        except requests.exceptions.RequestException as e:
            print("Failed to download file:", str(e))
            print()

    def download_courses(self) -> list:
        """Download courses

        Returns:
            list: The courses data
        """
        courses_data: list = self.api_controller.get_enrolled_courses()

        if self.debug:
            os.makedirs(self.test_data_dir, exist_ok=True)
            filename: str = f"courses-{self.cleaned_filename(self.program_name)}.json"
            JsonUtility.save_json_to_file(
                MoodleDataUtility.process_courses(courses_data),
                Path(self.test_data_dir, filename).absolute(),
            )

        return courses_data["courses"]

    def download_favorite_courses_contents(self) -> None:
        """Download favorite courses

        Returns:
            list: The favorite courses data
        """
        favorite_courses_data: list = MoodleDataUtility.get_courses_favoured(
            self.download_courses()
        )

        self.download_courses_contents(favorite_courses_data)

    def download_enrolled_students(
        self, course_id: str, course_name: str, filename: str
    ) -> None:
        """Download enrolled students

        Args:
            course_id (str): The course id
            filename (str): The filename
        """
        enrolled_users: list = self.api_controller.get_course_enrolled_users(course_id)

        if self.debug:
            os.makedirs(self.test_data_dir, exist_ok=True)

            JsonUtility.save_json_to_file(
                enrolled_users,
                Path(
                    self.test_data_dir, f"enrolled-users-{course_name.lower()}.json"
                ).absolute(),
            )

        enrolled_users: list = MoodleDataUtility.preprocess_enrolled_users(
            enrolled_users
        )
        if enrolled_users:
            CsvUtility.save_json_fields_list_to_csv(
                enrolled_users, EnrolledUsersFields.get_field_order(), filename
            )
            print(f"Enrolled users saved to {filename}")
        else:
            print("No enrolled users found.")
