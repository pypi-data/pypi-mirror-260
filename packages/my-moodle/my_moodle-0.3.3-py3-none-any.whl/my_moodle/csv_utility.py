"""
Copyright © 2024 Mark Crowe <https://github.com/marcocrowe>. All rights reserved.
CSV utility Class
"""
import csv


class CsvUtility:
    """CSV utility functions"""

    @staticmethod
    def save_json_list_to_csv(json_list: list, filename: str) -> None:
        """Save data to a CSV file.

        Args:
            data (list): List of dictionaries containing data to be saved.
            filename (str): Name of the CSV file to save.
        """
        if not json_list:
            print("No data to save.")
            return

        fieldnames = set().union(*(d.keys() for d in json_list))

        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            dict_writer = csv.DictWriter(file, fieldnames=fieldnames)
            dict_writer.writeheader()
            dict_writer.writerows(json_list)

    @staticmethod
    def save_json_fields_list_to_csv(
        json_list: list, fieldnames: set, filename: str
    ) -> None:
        """Save data to a CSV file.

        Args:
            data (list): List of JSON dictionaries containing data to be saved.
            filename (str): Name of the CSV file to save.
        """
        if not json_list:
            print("No data to save.")
            return

        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            dict_writer = csv.DictWriter(file, fieldnames=fieldnames)
            dict_writer.writeheader()
            for json_item in json_list:
                filtered_row = {
                    key: value for key, value in json_item.items() if key in fieldnames
                }
                dict_writer.writerow(filtered_row)
