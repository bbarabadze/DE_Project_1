"""
    This module contains some functions for analyse users activity
"""

import os
import pandas as pd
import numpy as np
from pandas import Series, DataFrame


def top_names(users_file: str, top_number: int) -> DataFrame:
    """
    Creates and prints a list of top most common names from users file
    :param users_file: File containing all users from the social network
    :param top_number: Number of top names to be listed
    :return: Dataframe containing the top most common names from users file
    """

    # Loads the table from users file into the pandas dataframe
    users_df = pd.read_csv(users_file)

    # Groups the dataframe by name
    gb_obj = users_df.groupby("Name")

    # Counts numbers of each unique name
    name_count = gb_obj["Name"].count()

    # Sorts names by number descending order and gets top names
    top_name = name_count.sort_values(ascending=False).head(top_number)

    # Creates dataframe of top names with proper column names and indexing
    top_names_df = pd.DataFrame({"Name": top_name.index, "Occurrences": top_name.values},
                                index=np.arange(1, len(top_name) + 1))

    print(f"Listing top {top_number} most common names on the social network:\n")
    print(top_names_df)
    print("\n")

    return top_names_df


def count_activity(folder_name: str) -> Series:
    """
    Yields user activity count object from each file from the passed folder
    :param folder_name: Path to the folder
    :return: Generator object
    """
    for file in os.listdir(folder_name):

        # Filtering for .csv files
        if file.endswith(".csv"):
            # Loads the table from partition file into the pandas dataframe
            dataframe = pd.read_csv(folder_name + file)

            # User IDs in reactions file is more than 1000, so need to reduce them to range [1, 1000)
            dataframe["User"] %= 1000

            # Counting user activities
            df_group_by_user = dataframe.groupby("User")
            users_activity_count = df_group_by_user["User"].count()

            # Some users are not present into files, so need to set a zero value to their activities
            users_activity_count = users_activity_count + pd.Series(np.zeros(1000), index=np.arange(1, 1001))
            users_activity_count = users_activity_count.fillna(0)

            yield users_activity_count.astype(pd.Int64Dtype())


def get_indexed_users(users_file: str) -> DataFrame:
    """
    Adds User ID as an index to the file
    :param users_file: Name of users file
    :return: Dataframe containing indexed users data
    """
    # Reads original file
    users_df = pd.read_csv(users_file)
    # Creates index object to map them to the users as User IDs
    users_idx = pd.Index(np.arange(1, len(users_df) + 1), name="User ID")

    return users_df.set_index(users_idx)


def get_top_users(users_df: DataFrame, users_act_count_total: Series, top_number: int) -> DataFrame:
    """
    Creates top active users table
    :param users_df: Dataframe containing all indexed users
    :param users_act_count_total: Series object containing user IDs as indexes and their activity
    counts as values
    :param top_number: Number of top active users to be listed
    :return: Top active users as a dataframe
    """

    # Sorts total user activity series descending order, takes passed number of top elements
    top_user_activity = users_act_count_total.sort_values(ascending=False).head(top_number)

    # Takes IDs of top active users
    top_user_ids = pd.Index(top_user_activity.index, name="User ID")

    # Querying users' names and users' surnames by IDs of top active users
    top_list = users_df.loc[top_user_ids][["Name", "Surname"]]

    # Adds new column of activities to a resulting dataframe
    top_list["Activities"] = top_user_activity

    # Inserts user ID column to the dataframe
    top_list.insert(0, "User ID", top_user_ids)

    # Enumerating top list by inserting rating column
    top_list.insert(0, "Rating", pd.Series(np.arange(1, top_number + 1)).values)

    # Making rating column a row index
    top_list.set_index("Rating", inplace=True)

    return top_list


def top_most_active(reactions_folder: str, posts_folder: str, users_file: str, top_number: int) -> DataFrame:
    """
    Creates and prints a list of top most active users
    depending on reactions and posts files
    :param reactions_folder: Path to the partitioned reactions' folder
    :param posts_folder: Path to the partitioned posts' folder
    :param users_file: File containing users list
    :param top_number: Number of top active users to be listed
    :return: A dataframe containing the top most active users
    """

    # Gets users table indexed by user ID
    users_df = get_indexed_users(users_file)

    number_of_users = len(users_df)

    # Initializes the series object, by which user activities have to be summarized
    user_activity_count_total = pd.Series(np.zeros(number_of_users), index=np.arange(1, number_of_users + 1),
                                          dtype=pd.Int64Dtype())

    # On each iteration, gets user activity count object and sums them up
    for partial_user_act_count in count_activity(posts_folder):
        user_activity_count_total = user_activity_count_total + partial_user_act_count

    # On each iteration, gets user activity count object and sums them up
    for partial_user_act_count in count_activity(reactions_folder):
        user_activity_count_total = user_activity_count_total + partial_user_act_count

    # Creates a final table containing top active users
    top_users = get_top_users(users_df, user_activity_count_total, top_number)

    print(f"Listing top {top_number} people with the most posts and reactions:\n")
    print(top_users)

    return top_users
