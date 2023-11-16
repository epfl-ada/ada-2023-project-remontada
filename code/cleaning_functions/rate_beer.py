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
    """Clean the rate beer users dataset
    Args:
        df_rate_beer_users (DataFrame): DataFrame containing the rate beer users dataset
    Returns:
        df_rate_beer_users (DataFrame): DataFrame containing the cleaned rate beer users dataset
    """
    #convert joined to datetime
    if df_rate_beer_users['joined'].dtype != 'datetime64[ns]':
        df_rate_beer_users['joined'] = pd.to_datetime(pd.to_numeric(df_rate_beer_users['joined']),unit='s')
    #drop duplicates user_id
    df_rate_beer_users.drop_duplicates(subset = 'user_id', inplace = True)
    #rename columns
    cols_to_rename = {
        'user_id': 'rb_user_id', 
        'user_name': 'rb_user_name',
        'joined': 'rb_joined',
        'location': 'rb_location'}
    df_rate_beer_users.rename(columns=cols_to_rename,inplace=True)
    return df_rate_beer_users

def clean_rb_ratings(df_rate_beer_ratings, df_all_beers):
    """Clean the rate beer ratings dataset
    Args:
        df_rate_beer_ratings (DataFrame): DataFrame containing the rate beer ratings dataset
        df_all_beers (DataFrame): DataFrame containing the beers dataset
    Returns:
        merged_df (DataFrame): DataFrame containing the cleaned rate beer ratings dataset
    """
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
    df_rate_beer_ratings[cols_to_convert_float] = df_rate_beer_ratings[cols_to_convert_float].apply(pd.to_numeric, errors='coerce')
    df_rate_beer_ratings[cols_to_convert_str] = df_rate_beer_ratings[cols_to_convert_str].astype(str)
    df_rate_beer_ratings[cols_to_convert_name] = df_rate_beer_ratings[cols_to_convert_name].astype(str).apply(lambda x: x.radd('rb_'))

    # Convert the 'date' column to datetime
    if df_rate_beer_ratings['date'].dtype != 'datetime64[ns]':
        df_rate_beer_ratings['date'] = pd.to_datetime(pd.to_numeric(df_rate_beer_ratings['date']),unit='s')

    # Replace the 'beer_id' column with the 'unique_id' column from the 'df_all_beers' DataFrame
    merged_df = df_rate_beer_ratings.merge(df_all_beers[['rb_beer_id', 'beer_unique_id']], 
                                           left_on='beer_id', right_on='rb_beer_id', how='left')

    # Replace the 'beer_id' column with the 'unique_id' column
    merged_df['beer_id'] = merged_df['beer_unique_id']

    # Drop the 'ba_beer_id' and 'unique_id' columns
    merged_df = merged_df.drop(columns=['rb_beer_id', 'beer_unique_id'])
    merged_df.dropna(subset=['beer_id','user_id'], inplace=True)
    return merged_df

def clean_rb_beers(df_rate_beer_beers):
    """Clean the rate beer beers dataset
    Args:
        df_rate_beer_beers (DataFrame): DataFrame containing the rate beer beers dataset
    Returns:
        df_rate_beer_beers (DataFrame): DataFrame containing the cleaned rate beer beers dataset
    """
    #rename columns
    df_rate_beer_beers = df_rate_beer_beers.add_prefix('rb_')

    # Convert id columns to obtain unique id
    cols_to_convert_name = ['rb_beer_id','rb_brewery_id']
    df_rate_beer_beers[cols_to_convert_name] = df_rate_beer_beers[cols_to_convert_name].astype(str).apply(lambda x: x.radd('rb_'))   
   
    # Drop duplicates
    df_rate_beer_beers.dropna(subset=['rb_beer_id','rb_brewery_id'],inplace=True)
    df_rate_beer_beers.drop_duplicates(subset=['rb_beer_id','rb_brewery_id'],inplace=True)
     
    return df_rate_beer_beers