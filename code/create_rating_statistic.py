# -*- coding: utf-8 -*-
# -*- author : Vincent Roduit -*-
# -*- date : 2023-11-12 -*-
# -*- Last revision: 2023-11-12 -*-
# -*- python version : 3.12.0 -*-
# -*- Description: Create the dataset of rating statistic of all users-*-

#import libraries
import numpy as np
from copy import deepcopy
import pandas as pd

def create_ratings_stat(df_advocate_ratings,df_rate_beer_ratings, df_all_users,debug=False):
    print('Creating copies...')
    df_advocate_ratings_stats = deepcopy(df_advocate_ratings)
    df_rate_beer_ratings_stats = deepcopy(df_rate_beer_ratings)
    df_advocate_ratings_stats.drop(columns=['review','text'], inplace=True)
    df_rate_beer_ratings_stats.drop(columns=['text'], inplace=True)
    df_advocate_ratings_stats.drop(df_advocate_ratings_stats[df_advocate_ratings_stats.user_id.isna()].index, inplace=True)
    df_rate_beer_ratings_stats.drop(df_rate_beer_ratings_stats[df_rate_beer_ratings_stats.user_id.isna()].index, inplace=True)
    df_advocate_ratings_stats.rename(columns={'user_name':'ba_user_name'}, inplace=True)
    df_rate_beer_ratings_stats.rename(columns={'user_name':'rb_user_name'}, inplace=True)
    ratings_stats = deepcopy(df_advocate_ratings_stats.merge(df_all_users, how='inner'))
    ratings_stats2 = deepcopy(df_rate_beer_ratings_stats.merge(df_all_users, how='inner'))
    ratings_stats = pd.concat([ratings_stats,ratings_stats2],axis=0)
    df_rate_beer_ratings_stats.user_id = df_rate_beer_ratings_stats.user_id.astype(int)
    df_rate_beer_ratings_stats.user_id = df_rate_beer_ratings_stats.user_id.astype(object)
    ratings_stats2 = deepcopy(df_rate_beer_ratings_stats.merge(df_all_users, how='inner'))
    ratings_stats = pd.concat([ratings_stats,ratings_stats2],axis=0)
    return ratings_stats