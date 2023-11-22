"""
    In this module, there are a couple of functions for check consistency of
    partitioned files with original ones
"""

import os
import pandas as pd
from utils import log_error
from disaster_recovery.custom_errors import PartitionInconsistencyError


def get_row_count(filename: str) -> int:
    """
    Counts rows of the table into given csv file
    :param filename: Name of the file
    :return: Number of rows
    """

    # Checks if file is readable
    try:
        dataframe = pd.read_csv(filename)
    except Exception as ex:
        log_error(f'Can\'t read file "{filename}", {ex}')
        # Raises a custom error
        raise PartitionInconsistencyError(f'Can\'t read file "{filename}", check error log')

    return len(dataframe)


def check_consistency(src_filename: str, partitions_folder: str) -> None:
    """
    Checks if the total number of rows of partitioned files is equal to the
    number of rows of the source file
    :param src_filename: Name of source file
    :param partitions_folder: Path to the partitions' folder
    :return:  None
    """
    partitions_row_count = 0

    # Iterates over the files into the partitions' folder and sums up a number of rows
    for file in os.listdir(partitions_folder):
        # Filtering for .csv files
        if file.endswith(".csv"):
            partitions_row_count += get_row_count(partitions_folder + file)

    # Gets number of rows from the source file
    src_row_count = get_row_count(src_filename)

    # If number of rows mismatched, raises a custom error
    if partitions_row_count != src_row_count:
        log_error(f"The total number of rows of partitioned files ({partitions_row_count}) \
does not equal the number of rows of the source file ({src_row_count})")
        raise PartitionInconsistencyError("Row number mismatch detected, check error log")
