# -*- coding: utf-8 -*-
# -*- author : Vincent Roduit -*-
# -*- date : 2023-11-14 -*-
# -*- Last revision: 2023-11-14 -*-
# -*- python version : 3.12.0 -*-
# -*- Description: Functions to clean datasets from matched_beer -*-

# Import libraries
import pandas as pd
import numpy as np

def clean_advocate_users(df_advocate_users):
    if df_advocate_users['joined'].dtype == np.int64:
        df_advocate_users['joined'] = pd.to_datetime(pd.to_numeric(df_advocate_users['joined']),unit='s')
    df_advocate_users.drop_duplicates(subset = 'user_id', inplace = True)
    df_advocate_users.rename(columns={'user_id': 'ba_user_id', 
                            'user_name': 'ba_user_name',
                            'joined': 'ba_joined',
                            'location': 'ba_location'},
                            inplace=True)
    return df_advocate_users

def clean_advocate_ratings(df_advocate_ratings):
    cols_to_clean = ['rating', 'appearance', 'aroma', 'palate', 'taste', 'overall', 'abv']
    df_advocate_ratings[cols_to_clean] = df_advocate_ratings[cols_to_clean].apply(pd.to_numeric, errors='coerce')
    return df_advocate_ratings