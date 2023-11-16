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
    df_rate_beer_ratings[cols_to_convert_float] = df_rate_beer_ratings[cols_to_convert_float].apply(pd.to_numeric, errors='coerce')
    df_rate_beer_ratings[cols_to_convert_str] = df_rate_beer_ratings[cols_to_convert_str].astype(str)
    df_rate_beer_ratings[cols_to_convert_name] = df_rate_beer_ratings[cols_to_convert_name].astype(str).apply(lambda x: x.radd('rb_'))
    df_rate_beer_ratings['date'] = pd.to_datetime(pd.to_numeric(df_rate_beer_ratings['date']),unit='s')
    return df_rate_beer_ratings

def clean_rb_beers(df_rate_beer_beers):
    df_rate_beer_beers.add_prefix('rb_')
    df_rate_beer_beers.drop_duplicates(subset=['rb_beer_id','rb_brewery_id'],inplace=True)
    df_rate_beer_beers.dropna(subset=['rb_beer_id','rb_brewery_id'],inplace=True)
    return df_rate_beer_beers