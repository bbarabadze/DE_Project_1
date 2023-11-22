"""
    This module contains the function by which partitioning to be done
"""
import pandas as pd
from utils import log_error


def partition_to_files(*, src_filename: str, partition_column_id: int, dst_folder_path: str) -> None:
    """
    Creates files containing partitioned tables of the table from source file by column ID
    :param src_filename: File containing the source table
    :param partition_column_id: Column ID from the source table, by which partitioning has to be done
    :param dst_folder_path: Folder for save partitioned files
    :return: None
    """

    # Checks if source file is readable
    try:
        # Loads the table from the source file into a pandas dataframe
        source_df = pd.read_csv(src_filename)
    except Exception as ex:
        log_error(str(ex))
        raise

    # Gets partition column name bu ID
    partition_column_name = source_df.columns[partition_column_id]

    # Iterating over unique values of the partition column
    for value in source_df[partition_column_name].unique():

        # Filter dataframe by unique value from the partition column
        selected_value_df = source_df[source_df[partition_column_name] == value]
        # Drop the partition column
        selected_value_df = selected_value_df.drop(partition_column_name, axis=1)

        # Checks if there is any problem with saving
        try:
            # Saves partition table to a file named with unique value from the partition column
            selected_value_df.to_csv(f"{dst_folder_path}{value}.csv", index=False)
        except Exception as ex:
            log_error(str(ex))
            raise
