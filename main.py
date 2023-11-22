"""
    Main module, contains main function defining the workflow and
    a couple of general functions
"""
from partition import partition_to_files
from utils import check_paths_exist, timer
from disaster_recovery import check_consistency
from analytics import top_names, top_most_active

# Source filenames with relative path
FRIENDS_FILE = "./social_network/friends_table.csv"
POSTS_FILE = "./social_network/posts_table.csv"
REACTIONS_FILE = "./social_network/reactions_table.csv"
USERS_FILE = "./social_network/user_table.csv"

# Destination folder paths for partitions
REACTIONS_FOLDER = "./social_network/partitioned/reactions/"
POSTS_FOLDER = "./social_network/partitioned/posts/"


def do_partitioning() -> None:
    """
    Runs partitioning functions for posts and reactions files
    :return:
    """
    print("Starting partitioning...")

    partition_to_files(
        src_filename=REACTIONS_FILE,
        partition_column_id=1,
        dst_folder_path=REACTIONS_FOLDER
    )

    print("- Partitioning of the reactions table is done")

    partition_to_files(
        src_filename=POSTS_FILE,
        partition_column_id=1,
        dst_folder_path=POSTS_FOLDER
    )

    print("- Partitioning of the posts table is done")
    print("Partitioning completed successfully\n")


def do_dr_check() -> None:
    """
    Runs consistency check of source files with its partitions
    :return: None
    """
    print("Starting disaster recovery check...")

    check_consistency(REACTIONS_FILE, REACTIONS_FOLDER)

    print("- The Reactions table and its partitions are consistent")

    check_consistency(POSTS_FILE, POSTS_FOLDER)

    print("- The Posts table and its partitions are consistent")
    print("Disaster recovery check completed successfully\n")


@timer("Running time of the main function:")
def main():
    """
    Main function
    :return: None
    """
    # Checking existence of source files and partition destination folders
    check_paths_exist(
        FRIENDS_FILE,
        POSTS_FILE,
        REACTIONS_FILE,
        USERS_FILE,
        REACTIONS_FOLDER,
        POSTS_FOLDER
    )
    # Partitioning posts and reactions files into the corresponding folders
    do_partitioning()

    # Checking consistency source files with partitioned ones
    do_dr_check()

    # Creates and prints a list of top 10 most common names on the social network
    top_names(USERS_FILE, 10)

    # Creates and prints a list of top 5 most active users on the social network
    top_most_active(REACTIONS_FOLDER, POSTS_FOLDER, USERS_FILE, 5)


if __name__ == '__main__':
    main()
