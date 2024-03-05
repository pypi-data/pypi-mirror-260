"""
This module provides a Profiler class for profiling data.

It imports the ProfileReport class from the ydata_profiling library,
the Checker class from the checker module, and the Reader class from the reader module.
"""

from ydata_profiling import ProfileReport
from .checker import Checker
from .reader import Reader


class Profiler(ProfileReport):
    """
    The Profiler class inherits from the ProfileReport class of the ydata_profiling library.
    It is used to create a profile report for a given DataFrame.

    Attributes:
        df_path (str): The path to the DataFrame to be profiled.
    """

    def __init__(self, df_path=None, **kwargs):
        """
        The constructor for the Profiler class.

        Parameters:
            df_path (str): The path to the DataFrame to be profiled. Default is None.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(**kwargs)
        if df_path is not None:
            Checker.check_df_path(df_path)
        self.df_path = df_path
        self.report_description = None

    def profile(self):
        """
        Profiles the data by reading the CSV file specified in `df_path` and 
        generating a report description.

        Raises:
            ValueError: If `df_path` is not provided.
        """
        if self.df_path is None:
            raise ValueError("df_path is required")
        self.df = Reader.read_csv(self.df_path)
        super().__init__(self.df)
        self.report_description = super().get_description()