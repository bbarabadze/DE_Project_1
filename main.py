from partition import partition_to_files
from utils import check_paths_exist, timer
from disaster_recovery import check_consistency
from analytics import top10_names, top5_most_active

FRIENDS_FILE = "./social_network/friends_table.csv"
POSTS_FILE = "./social_network/posts_table.csv"
REACTIONS_FILE = "./social_network/reactions_table.csv"
USERS_FILE = "./social_network/user_table.csv"

REACTIONS_FOLDER = "./social_network/partitioned/reactions/"
POSTS_FOLDER = "./social_network/partitioned/posts/"


def do_partitioning() -> None:

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

    print("Starting disaster recovery check...")

    check_consistency(REACTIONS_FILE, REACTIONS_FOLDER)

    print("- The Reactions table and its partitions are consistent")

    check_consistency(POSTS_FILE, POSTS_FOLDER)

    print("- The Posts table and its partitions are consistent")
    print("Disaster recovery check completed successfully\n")


@timer("Running time of the main function:")
def main():

    check_paths_exist(
        FRIENDS_FILE,
        POSTS_FILE,
        REACTIONS_FILE,
        USERS_FILE,
        REACTIONS_FOLDER,
        POSTS_FOLDER
    )
    do_partitioning()
    do_dr_check()
    top10_names(USERS_FILE)
    top5_most_active(REACTIONS_FOLDER, POSTS_FOLDER, USERS_FILE)


if __name__ == '__main__':
    main()
