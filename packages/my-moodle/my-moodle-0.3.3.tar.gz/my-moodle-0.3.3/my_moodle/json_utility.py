"""
Copyright © 2024 Mark Crowe <https://github.com/marcocrowe>. All rights reserved.
JSON utility Class
"""

import json


class JsonUtility:
    """JSON Utility functions"""

    @staticmethod
    def save_json_to_file(json_dict: dict, file_path: str) -> None:
        """Save

        Args:
            json_dict (dict): _description_
            file_path (str): _description_
        """
        with open(file_path, "w", encoding="utf-8") as json_file:
            json_file.write(json.dumps(json_dict, indent=2))
        print(f"JSON data saved to {file_path}")
