import pandas as pd
from utils import log_error


def partition_to_files(*, src_filename: str, partition_column_id: int, dst_folder_path: str) -> None:

    try:
        source_df = pd.read_csv(src_filename)
    except Exception as ex:
        log_error(str(ex))
        raise

    partition_column_name = source_df.columns[partition_column_id]

    for value in source_df[partition_column_name].unique():

        selected_value_df = source_df[source_df[partition_column_name] == value]
        selected_value_df = selected_value_df.drop(partition_column_name, axis=1)

        try:
            selected_value_df.to_csv(f"{dst_folder_path}{value}.csv", index=False)
        except Exception as ex:
            log_error(str(ex))
            raise
