"""
Copyright © 2024 Mark Crowe <https://github.com/marcocrowe>. All rights reserved.
Moodle data utility Class
"""

import html
import re
import time
from my_moodle.course_status import CourseStatus
from my_moodle.enrolled_users_fields import EnrolledUsersFields


class MoodleDataUtility:
    """Moodle data utility functions"""

    @staticmethod
    def get_course_status(course: dict) -> CourseStatus:
        """Get the status of the course.

        Args:
            course (dict): Dictionary containing the course's details.

        Returns:
            str: The status of the course.
        """
        current_time = time.time()

        if current_time < course["startdate"]:
            return CourseStatus.UPCOMING
        elif course["startdate"] <= current_time <= course["enddate"]:
            return CourseStatus.ACTIVE

        return CourseStatus.PAST_FINISHED

    @staticmethod
    def get_courses_favoured(courses: list) -> list:
        """Get courses that are favoured.

        Args:
            courses (list): List of courses.

        Returns:
            list: List of favoured courses.
        """
        return [
            course for course in courses if course.get("isfavourite", False)
        ]

    @staticmethod
    def get_courses_by_status(courses: list, status: CourseStatus) -> list:
        """Get courses by status.

        Args:
            courses (list): List of courses.
            status (CourseStatus): The status of the course to filter by.

        Returns:
            list: List of courses with the status.
        """
        return [
            course
            for course in courses
            if MoodleDataUtility.get_course_status(course) == status
        ]

    @staticmethod
    def is_student(enrolled_user: dict) -> bool:
        """Check if the enrolled user is a student.

        Args:
            enrolled_user (dict): Dictionary containing the enrolled user's details.

        Returns:
            bool: True if the user is a student, False otherwise.
        """
        roles = enrolled_user.get(EnrolledUsersFields.ROLES, [])
        if roles:
            role_names = [role[EnrolledUsersFields.ROLE_SHORTNAME] for role in roles]
            return "student" in role_names
        return False

    @staticmethod
    def parse_course_name(course: dict) -> str:
        """Parse the course name from the course details.

        Args:
            course (dict): Dictionary containing the course's details.

        Returns:
            str: The course name.
        """
        full_name: str = course.get("fullname", "")
        course_id: str = course.get("id", "")
        return f"{MoodleDataUtility.convert_to_slug(full_name)}-id-{course_id}"

    @staticmethod
    def convert_to_slug(input_string: str) -> str:
        """Convert a string to a slug

        Args:
            input_string (str): The input string

        Returns:
            str: The slug
        """
        input_string = html.unescape(input_string).replace("&", "and")
        # Extract year "(23-24)"
        match = re.search(r"\(\d+-\d+\)", input_string)
        if match:
            extracted = match.group(0)
            input_string = input_string.replace(
                extracted, ""
            ).strip()  # Remove extracted substring
            extracted = "-year-" + re.sub(r"[^\w\s-]", "", extracted)
        else:
            extracted = ""

        # Remove non-alphanumeric characters except spaces and dashes
        slug = re.sub(r"[^\w\s-]", "", input_string)
        # Replace spaces with '-'
        slug = slug.replace(" ", "-")
        # Replace multiple dashes with one
        slug = re.sub(r"-+", "-", slug)
        # Convert to lowercase
        # slug = slug.lower()

        return f"{slug}{extracted}"

    @staticmethod
    def preprocess_enrolled_users(enrolled_users: list) -> list:
        """Preprocess enrolled users data before saving to CSV.

        Args:
            enrolled_users (list): List of enrolled users' details.

        Returns:
            list: Preprocessed enrolled users data.
        """
        if not enrolled_users:
            return []

        preprocessed_users = []
        for user in enrolled_users:
            if MoodleDataUtility.is_student(user):

                # Remove unwanted fields
                preprocessed_user = {
                    key: value
                    for key, value in user.items()
                    if key not in EnrolledUsersFields.get_unwanted_fields()
                }

                # Set profile image url to blank if it matches the specified value
                profile_image_url = preprocessed_user.get(
                    EnrolledUsersFields.PROFILE_IMAGE_URL
                )
                if profile_image_url.endswith(
                    EnrolledUsersFields.DEFAULT_PROFILE_IMAGE_URL
                ):
                    preprocessed_user[EnrolledUsersFields.PROFILE_IMAGE_URL] = ""

                preprocessed_users.append(preprocessed_user)

        return preprocessed_users

    @staticmethod
    def process_courses(courses_data: dict) -> dict:
        """process courses data.

        Args:
            courses (dict): Courses data.

        Returns:
            dict: Processed courses data.
        """
        if not courses_data:
            return {}

        if "courses" in courses_data:
            for course in courses_data["courses"]:
                if course["courseimage"].startswith("data:image/"):
                    course["courseimage"] = ""

        return courses_data

    @staticmethod
    def process_course_contents_to_file_list(course_contents: list) -> list:  # #NOSONAR
        # function Cognitive Complexity from 22
        """process course contents to a list of files.

        Args:
            course_contents (list): List of course contents.

        Returns:
            list: List of course content files.
        """
        if not course_contents:
            return []

        files = []

        file_number = 0
        for module in course_contents:
            if "modules" in module:
                for module_item in module["modules"]:
                    if "contents" in module_item:
                        for file_item in module_item["contents"]:
                            if "fileurl" in file_item:
                                file_number += 1
                                files.append(
                                    {
                                        "filenumber": file_number,
                                        "id": module_item["id"],
                                        "name": file_item["filename"],
                                        "url": file_item["fileurl"],
                                    }
                                )
        return files
