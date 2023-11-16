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
    df_matched_beer_users_index = deepcopy(df_matched_beer_users.iloc[0,:])
    # drop first row
    df_matched_beer_users.drop(df_matched_beer_users.index[0], axis=0, inplace=True)

    # convert column names
    column_names = [
        'ba_joined',
        'ba_location',
        'ba_nbr_ratings',
        'ba_nb_reviews',
        'ba_user_id',
        'ba_user_name',
        'ba_user_name_lower',
        'rb_joined',
        'rb_location',
        'rb_nbr_ratings',
        'rb_user_id',
        'rb_user_name',
        'rb_user_name_lower',
    ]
    df_matched_beer_users.columns = column_names
    # convert column joined to datetime
    df_matched_beer_users['ba_joined'] = pd.to_datetime(
        pd.to_numeric(df_matched_beer_users['ba_joined']),
        unit='s'
    )
    df_matched_beer_users['rb_joined'] = pd.to_datetime(
        pd.to_numeric(df_matched_beer_users['rb_joined']),
        unit='s'
    )
    return df_matched_beer_users, df_matched_beer_users_index

def clean_mb_beers(matched_beer_beers):
    return matched_beer_beers