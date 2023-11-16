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
    df_advocate_ratings.dropna(subset=['beer_id','user_id'], inplace=True)
    cols_to_convert_float = [
        'date',
        'rating', 
        'appearance', 
        'aroma', 
        'palate', 
        'taste', 
        'overall', 
        'abv',
    ]
    cols_to_convert_str = [
        'beer_name',
        'style',
        'brewery_name',
        'text',
    ]
    cols_to_convert_name = ['beer_id','brewery_id']
    df_advocate_ratings[cols_to_convert_float] = df_advocate_ratings[cols_to_convert_float].apply(pd.to_numeric, errors='coerce')
    df_advocate_ratings[cols_to_convert_str] = df_advocate_ratings[cols_to_convert_str].astype(str)
    df_advocate_ratings[cols_to_convert_name] = df_advocate_ratings[cols_to_convert_name].astype(str).apply(lambda x: x.radd('ba_'))
    return df_advocate_ratings

def clean_adocate_beers(df_advocate_beers):
    df_advocate_beers = df_advocate_beers.add_prefix('ba_')
    df_advocate_beers.drop_duplicates(subset=['ba_beer_id','ba_brewery_id'],inplace=True)
    df_advocate_beers.dropna(subset=['ba_beer_id','ba_brewery_id'],inplace=True)
    return df_advocate_beers