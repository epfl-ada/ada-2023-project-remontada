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
    """Clean the advocate users dataset
    Args:
        df_advocate_users (DataFrame): DataFrame containing the advocate users dataset
    Returns:
        df_advocate_users (DataFrame): DataFrame containing the cleaned advocate users dataset
    """
    
    #drop duplicates user_id
    df_advocate_users.drop_duplicates(subset = 'user_id', inplace = True)
    #convert joined to datetime
    if df_advocate_users['joined'].dtype != 'datetime64[ns]':
        df_advocate_users['joined'] = pd.to_datetime(pd.to_numeric(df_advocate_users['joined']),unit='s')

    #rename columns
    column_to_rename = {'user_id': 'ba_user_id', 
                            'user_name': 'ba_user_name',
                            'joined': 'ba_joined',
                            'location': 'ba_location'}
    df_advocate_users.rename(columns = column_to_rename, inplace=True)
    return df_advocate_users

def clean_advocate_ratings(df_advocate_ratings, df_all_beers):
    """Clean the advocate ratings dataset
    Args:
        df_advocate_ratings (DataFrame): DataFrame containing the advocate ratings dataset
        df_all_beers (DataFrame): DataFrame containing the beers dataset
    Returns:
        merged_df (DataFrame): DataFrame containing the cleaned advocate ratings dataset
    """
    #drop rows where beer_id or user_id is missing
    df_advocate_ratings.dropna(subset=['beer_id','user_id'], inplace=True)

    # Type conversion
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
    df_advocate_ratings['date'] = pd.to_datetime(pd.to_numeric(df_advocate_ratings['date']),unit='s')

    # Replace beer_id with unique_id from df_all_beers
    merged_df = df_advocate_ratings.merge(df_all_beers[['ba_beer_id', 'beer_unique_id']], 
                                          left_on='beer_id', right_on='ba_beer_id', how='left')
    
    # Replace the 'beer_id' column with the 'unique_id' column
    merged_df['beer_id'] = merged_df['beer_unique_id']
    
    # Drop the 'ba_beer_id' and 'unique_id' columns
    merged_df = merged_df.drop(columns=['ba_beer_id', 'beer_unique_id'])
    merged_df.dropna(subset=['beer_id','user_id'], inplace=True)
    return merged_df

def clean_advocate_beers(df_advocate_beers):
    """Clean the advocate beers dataset
    Args:
        df_advocate_beers (DataFrame): DataFrame containing the advocate beers dataset
    Returns:
        df_advocate_beers (DataFrame): DataFrame containing the cleaned advocate beers dataset
    """
    #rename columns
    df_advocate_beers = df_advocate_beers.add_prefix('ba_')

    # Convert id columns to obtain unique id
    cols_to_convert_name = ['ba_beer_id','ba_brewery_id']
    df_advocate_beers[cols_to_convert_name] = df_advocate_beers[cols_to_convert_name].astype(str).apply(lambda x: 'ba_' + x)

    #drop duplicates
    df_advocate_beers.drop_duplicates(subset=['ba_beer_id','ba_brewery_id'],inplace=True)
    df_advocate_beers.dropna(subset=['ba_beer_id','ba_brewery_id'],inplace=True)
    return df_advocate_beers