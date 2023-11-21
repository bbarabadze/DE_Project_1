import os
import pandas as pd
from pandas import Series, DataFrame
import numpy as np


def top10_names(users_file: str) -> None:

    users_df = pd.read_csv(users_file)
    gb_obj = users_df.groupby("Name")
    top10 = gb_obj["Name"].count().sort_values(ascending=False).head(10)
    top10_df = pd.DataFrame({"Name": top10.index, "Occurrences": top10.values}, index=np.arange(1, 11))

    print("Listing top 10 most common names on the social network:\n")
    print(top10_df)
    print("\n")


def count_activity(folder_name: str) -> Series:

    for file in os.listdir(folder_name):

        dataframe = pd.read_csv(folder_name + file)
        dataframe["User"] %= 1000
        df_group_by_user = dataframe.groupby("User")
        users_activity_count = df_group_by_user["User"].count()
        users_activity_count = users_activity_count + pd.Series(np.zeros(1000), index=np.arange(1, 1001))
        users_activity_count = users_activity_count.fillna(0)
        yield users_activity_count.astype(pd.Int64Dtype())


def get_indexed_users(users_file: str) -> DataFrame:

    users_df = pd.read_csv(users_file)
    users_idx = pd.Index(np.arange(1, 1001), name="User ID")
    return users_df.set_index(users_idx)


def get_top_users(users_df: DataFrame, users_count: Series, top_number: int) -> DataFrame:

    top_user_activity = users_count.sort_values(ascending=False).head(top_number)

    top_user_indexes = pd.Index(top_user_activity.index, name="User ID")

    top_list = users_df.loc[top_user_indexes][["Name", "Surname"]]

    top_list["Overall"] = top_user_activity

    top_list.insert(0, "User ID", top_user_indexes)

    top_list.insert(0, "Rating", pd.Series(np.arange(1, top_number + 1)).values)

    top_list.set_index("Rating", inplace=True)

    return top_list


def top5_most_active(reactions_folder: str, posts_folder: str, users_file: str) -> None:

    user_activity_count = pd.Series(np.zeros(1000), index=np.arange(1, 1001), dtype=pd.Int64Dtype())

    for partial_user_act_count in count_activity(posts_folder):
        user_activity_count = user_activity_count + partial_user_act_count
    for partial_user_act_count in count_activity(reactions_folder):
        user_activity_count = user_activity_count + partial_user_act_count

    users_df = get_indexed_users(users_file)

    top5_users = get_top_users(users_df, user_activity_count, 5)

    print("Listing top five people with the most posts and reactions:\n")
    print(top5_users)
