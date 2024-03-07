import logging
from threading import Lock
from typing import Dict, List, Union, cast

import pandas as pd


class Lognostic:
    """
    Lognostic is a logging utility class designed to record, store, and analyze logging data.
    It captures logging information such as logger names, message sizes, and timestamps,
    providing functionalities to analyze this data for monitoring and debugging purposes.

    Attributes:
        _lock (Lock): A threading lock to ensure thread-safe operations on records.
        _records (List[Dict[str, pd.Timestamp | str | int]]): A list to store logging records.
    """

    def __init__(self) -> None:
        """
        Initializes the Lognostic class by setting up the threading lock and initializing the list of records.
        """
        self._lock: Lock = Lock()
        self._records: List[Dict[str, Union[pd.Timestamp, str, int]]] = []

    def record(self, log_record: logging.LogRecord) -> None:
        """
        Records a new logging event by appending it to the list of records.

        Args:
            log_record (logging.LogRecord): The log record to be recorded, containing the logger's name,
            the log message, and other metadata.
        """
        logger_name: str = log_record.name
        message_size: int = len(log_record.getMessage())
        with self._lock:
            now = pd.Timestamp.now()
            self._records.append(
                {
                    "logger_name": logger_name,
                    "message_size": message_size,
                    "timestamp": now,
                }
            )

    def _dataframe(self) -> pd.DataFrame:
        """
        Converts internal records from a list of dictionaries to a pandas DataFrame.

        Returns:
            pd.DataFrame: A DataFrame containing all logging records.
        """
        return pd.DataFrame(self._records)

    def _get_recent_records(self, lookback_period: int) -> pd.DataFrame:
        """
        Retrieves records within the specified lookback period.

        Parameters:
            lookback_period (int): The lookback period in seconds.

        Returns:
            pd.DataFrame: A DataFrame containing recent logging records.
        """
        df = self._dataframe()
        time_window = pd.Timestamp.now() - pd.Timedelta(seconds=lookback_period)
        recent = df[df["timestamp"] > time_window]
        return recent

    def total_size(self) -> int:
        """
        Calculates the total size of all logged messages.

        Returns:
            int: The total size of all messages.
        """
        df = self._dataframe()
        total_size = df["message_size"].sum()
        return cast(int, total_size)

    def total_size_per_logger(self) -> Dict[str, int]:
        """
        Calculates the total size of logged messages per logger.

        Returns:
            Dict[str, int]: A dictionary mapping logger names to their total message size.
        """
        df = self._dataframe()
        return df.groupby("logger_name")["message_size"].sum().to_dict()

    def total_logging_rate(self, lookback_period: int = 60) -> float:
        """
        Calculates the total logging rate over a specified lookback period.

        Parameters:
            lookback_period (int, optional): The lookback period in seconds. Defaults to 60.

        Returns:
            float: The average logging rate (message size per second).
        """
        recent_records = self._get_recent_records(lookback_period)
        total_rate = recent_records["message_size"].sum() / lookback_period
        return cast(float, total_rate)

    def logging_rate_per_logger(self, lookback_period: int = 60) -> Dict[str, float]:
        """
        Calculates the logging rate per logger over a specified lookback period.

        Parameters:
            lookback_period (int, optional): The lookback period in seconds. Defaults to 60.

        Returns:
            Dict[str, float]: A dictionary mapping logger names to their average logging rate (message size per second).
        """
        recent_records = self._get_recent_records(lookback_period)
        return (
            recent_records.groupby("logger_name")["message_size"].sum()
            / lookback_period
        ).to_dict()
