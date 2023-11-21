class PartitionInconsistencyError(Exception):
    """
    Raises when partitioned files are inconsistent with source file
    """
    def __init__(self, message):
        super().__init__(message)
