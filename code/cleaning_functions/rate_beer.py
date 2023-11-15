# -*- coding: utf-8 -*-
# -*- author : Vincent Roduit -*-
# -*- date : 2023-11-14 -*-
# -*- Last revision: 2023-11-14 -*-
# -*- python version : 3.12.0 -*-
# -*- Description: Functions to clean datasets from matched_beer -*-

# Import libraries
import pandas as pd
import numpy as np

def clean_rb_users(df_rate_beer_users):
    df_rate_beer_users['joined'] = pd.to_datetime(pd.to_numeric(df_rate_beer_users['joined']),unit='s')
    df_rate_beer_users.drop_duplicates(subset = 'user_id', inplace = True)
    df_rate_beer_users.rename(columns={'user_id': 'rb_user_id', 
                            'user_name': 'rb_user_name',
                            'joined': 'rb_joined',
                            'location': 'rb_location'},
                            inplace=True)
    return df_rate_beer_users

def clean_rb_ratings(df_rate_beer_ratings):
    cols_to_clean = ['rating', 'appearance', 'aroma', 'palate', 'taste', 'overall', 'abv']
    df_rate_beer_ratings[cols_to_clean] = df_rate_beer_ratings[cols_to_clean].apply(pd.to_numeric, errors='coerce')
    return df_rate_beer_ratings