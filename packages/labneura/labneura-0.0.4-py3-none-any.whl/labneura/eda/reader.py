"""
Reader module for reading data from various file formats.

This module contains the following class:

- Reader: a class for reading data from various file formats
"""
import pandas as pd


class Reader:
    """
    A class for reading data from various file formats.
    """

    @staticmethod
    def read_csv(path: str):
        """
        Read a CSV file and return a pandas DataFrame.

        Parameters:
        path (str): The path to the CSV file.

        Returns:
        pandas.DataFrame: The DataFrame containing the data from the CSV file.
        """
        return pd.read_csv(path)
