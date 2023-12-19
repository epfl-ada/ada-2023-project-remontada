# -*- coding: utf-8 -*-
# -*- author : Vincent Roduit -*-
# -*- date : 2023-11-12 -*-
# -*- Last revision: 2023-11-14 -*-
# -*- python version : 3.12.0 -*-
# -*- Description: Create the dataset of rating statistic of all users-*-

#import libraries
import numpy as np
import os
from copy import deepcopy
import pandas as pd
from read.pickle_functions import load_pickle

def create_ratings_stat(df_advocate_ratings,df_rate_beer_ratings, df_all_users,read_pickle_if_exists=True):
    """Create the dataset of rating statistic of all users
    Args:
        df_advocate_ratings (dataframe): dataframe of advocate ratings
        df_rate_beer_ratings (dataframe): dataframe of rate beer ratings
        df_all_users (dataframe): dataframe of all users
    Returns:
        ratings_stats (dataframe): dataframe of rating statistic of all users
    """
    path = '../datas/results/'
    file = 'df_ratings_stat.pkl'
    if os.path.exists(path+file) and read_pickle_if_exists:
        print('Loading the dataframe in pickle format from ',path)
        ratings_stats = load_pickle(path+file)
    else:
        #Create a copy of the dataframes
        print('Creating copies...')
        df_advocate_ratings_stats = deepcopy(df_advocate_ratings)
        df_rate_beer_ratings_stats = deepcopy(df_rate_beer_ratings)

        #process the dataframes
        print('processing dataframes...')
        df_advocate_ratings_stats.drop(columns=['review','text'], inplace=True)
        df_rate_beer_ratings_stats.drop(columns=['text'], inplace=True)
        df_advocate_ratings_stats.drop(df_advocate_ratings_stats[df_advocate_ratings_stats.user_id.isna()].index, inplace=True)
        df_rate_beer_ratings_stats.drop(df_rate_beer_ratings_stats[df_rate_beer_ratings_stats.user_id.isna()].index, inplace=True)
        df_advocate_ratings_stats.rename(columns={'user_name':'ba_user_name'}, inplace=True)
        df_rate_beer_ratings_stats.rename(columns={'user_name':'rb_user_name'}, inplace=True)

        #Merge the dataframes
        print('Merging dataframes...')
        ratings_stats = deepcopy(df_advocate_ratings_stats.merge(df_all_users, how='inner'))
        df_rate_beer_ratings_stats.user_id = df_rate_beer_ratings_stats.user_id.astype(int)
        df_rate_beer_ratings_stats.user_id = df_rate_beer_ratings_stats.user_id.astype(object)
        ratings_stats2 = deepcopy(df_rate_beer_ratings_stats.merge(df_all_users, how='inner'))

        #Concatenate the dataframes
        print('Concatenating dataframes...')
        ratings_stats = pd.concat([ratings_stats,ratings_stats2],axis=0,keys=['ba','rb'])
        ratings_stats.reset_index(level=0,inplace=True)
        ratings_stats.rename(columns={'level_0': 'source'}, inplace=True)

        ratings_stats["year"]=ratings_stats["date"].dt.year
    return ratings_stats