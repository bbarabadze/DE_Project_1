import os
import pandas as pd
from utils import log_error
from custom_errors import PartitionInconsistencyError


def get_row_count(filename: str) -> int:
    try:
        dataframe = pd.read_csv(filename)
    except Exception as ex:
        log_error(f'Can\'t read file "{filename}", {ex}')
        raise PartitionInconsistencyError(f'Can\'t read file "{filename}", check error log')

    return len(dataframe)


def check_consistency(src_filename: str, partitions_folder: str) -> None:

    partitions_row_count = 0

    for file in os.listdir(partitions_folder):
        partitions_row_count += get_row_count(partitions_folder + file)

    src_row_count = get_row_count(src_filename)

    if partitions_row_count != src_row_count:
        log_error(f"The total number of rows of partitioned files ({partitions_row_count}) \
does not equal the number of rows of the source file ({src_row_count})")
        raise PartitionInconsistencyError("Row number mismatch detected, check error log")
