"""
Checker module for the EDA package.

This module contains the following class:
- Checker: a class for checking file paths for DataFrames

"""
import os


class Checker:
    """
    A utility class for checking file paths for DataFrames.
    """

    @staticmethod
    def check_df_path(df_path: str):
        """
        Check if the given file path is valid for a DataFrame.

        Args:
            df_path (str): The file path to be checked.

        Raises:
            ValueError: If `df_path` is not a string, does not end with ".csv" or ".xlsx",
                        or does not exist.

        """
        if not isinstance(df_path, str):
            raise ValueError("df_path must be a string")
        if not (df_path.endswith(".csv") or df_path.endswith(".xlsx")):
            raise ValueError("df_path must be a csv or xlsx file")
        if not os.path.exists(df_path):
            raise ValueError("df_path does not exist")