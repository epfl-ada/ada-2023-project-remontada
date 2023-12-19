# -*- coding: utf-8 -*-
# -*- author : Vincent Roduit -*-
# -*- date : 2023-11-14 -*-
# -*- Last revision: 2023-11-14 -*-
# -*- python version : 3.12.0 -*-
# -*- Description: Functions to clean datasets from matched_beer -*-

# Import libraries
import pandas as pd
import numpy as np
from copy import deepcopy


def clean_mb_users(df_matched_beer_users):
    """Function to clean the users dataset from matched_beer

    Args:
        df_matched_beer_users (pandas dataframe): dataframe to clean

    """
    # keep first row as index reference
    df_matched_beer_users_index = deepcopy(df_matched_beer_users.iloc[0, :])
    # drop first row
    df_matched_beer_users.drop(df_matched_beer_users.index[0], axis=0, inplace=True)

    # convert column names
    column_names = [
        "ba_joined",
        "ba_location",
        "ba_nbr_ratings",
        "ba_nb_reviews",
        "ba_user_id",
        "ba_user_name",
        "ba_user_name_lower",
        "rb_joined",
        "rb_location",
        "rb_nbr_ratings",
        "rb_user_id",
        "rb_user_name",
        "rb_user_name_lower",
    ]
    df_matched_beer_users.columns = column_names
    # convert column joined to datetime
    if df_matched_beer_users["ba_joined"].dtype == "object":
        df_matched_beer_users["ba_joined"] = pd.to_datetime(
            pd.to_numeric(df_matched_beer_users["ba_joined"]), unit="s"
        )

    if df_matched_beer_users["rb_joined"].dtype == "object":
        df_matched_beer_users["rb_joined"] = pd.to_datetime(
            pd.to_numeric(df_matched_beer_users["rb_joined"]), unit="s"
        )

    return df_matched_beer_users, df_matched_beer_users_index


def clean_mb_beers(matched_beer_beers):
    """Function to clean the beers dataset from matched_beer
    Args:
        matched_beer_beers (pandas dataframe): dataframe to clean
    Returns:
        matched_beer_beers (pandas dataframe): cleaned dataframe
    """
    # change column names
    column_names = {
        "abv": "ba_abv",
        "avg": "ba_avg",
        "avg_computed": "ba_avg_computed",
        "avg_matched_valid_ratings": "ba_avg_matched_valid_ratings",
        "ba_score": "ba_ba_score",
        "beer_id": "ba_beer_id",
        "beer_name": "ba_beer_name",
        "beer_wout_brewery_name": "ba_beer_wout_brewery_name",
        "brewery_id": "ba_brewery_id",
        "brewery_name": "ba_brewery_name",
        "bros_score": "ba_bros_score",
        "nbr_matched_valid_ratings": "ba_nbr_matched_valid_ratings",
        "nbr_ratings": "ba_nbr_ratings",
        "nbr_reviews": "ba_nbr_reviews",
        "style": "ba_style",
        "zscore": "ba_zscore",
        "abv.1": "rb_abv",
        "avg.1": "rb_avg",
        "avg_computed.1": "rb_avg_computed",
        "avg_matched_valid_ratings.1": "rb_avg_matched_valid_ratings",
        "beer_id.1": "rb_beer_id",
        "beer_name.1": "rb_beer_name",
        "beer_wout_brewery_name.1": "rb_beer_wout_brewery_name",
        "brewery_id.1": "rb_brewery_id",
        "brewery_name.1": "rb_brewery_name",
        "nbr_matched_valid_ratings.1": "rb_nbr_matched_valid_ratings",
        "nbr_ratings.1": "rb_nbr_ratings",
        "overall_score": "rb_overall_score",
        "style.1": "rb_style",
        "style_score": "rb_style_score",
        "zscore.1": "rb_zscore",
        "diff": "diff",
        "sim": "sim",
    }
    matched_beer_beers = matched_beer_beers.rename(columns=column_names)

    # Convert ids columns to obtain unique ids
    cols_to_convert_name_ba = ["ba_beer_id", "ba_brewery_id"]
    cols_to_convert_name_rb = ["rb_beer_id", "rb_brewery_id"]
    matched_beer_beers[cols_to_convert_name_ba] = (
        matched_beer_beers[cols_to_convert_name_ba]
        .astype(str)
        .apply(lambda x: "ba_" + x)
    )
    matched_beer_beers[cols_to_convert_name_rb] = (
        matched_beer_beers[cols_to_convert_name_rb]
        .astype(str)
        .apply(lambda x: "rb_" + x)
    )

    return matched_beer_beers
