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
    #Create a copy of the dataframes
    print('Creating copies...')
    df_advocate_ratings_stats = deepcopy(df_advocate_ratings[['date','user_name','user_id']])
    df_rate_beer_ratings_stats = deepcopy(df_rate_beer_ratings[['date','user_name','user_id']])
    df_advocate_ratings_stats.rename(columns={'user_name':'ba_user_name','user_id':'ba_user_id'}, inplace=True)
    df_rate_beer_ratings_stats.rename(columns={'user_name':'rb_user_name','user_id':'rb_user_id'}, inplace=True)

    #drop rows with missing values for user_id
    df_advocate_ratings_stats.drop(df_advocate_ratings_stats[df_advocate_ratings_stats.ba_user_id.isna()].index, inplace=True)
    df_rate_beer_ratings_stats.drop(df_rate_beer_ratings_stats[df_rate_beer_ratings_stats.rb_user_id.isna()].index, inplace=True)

    #Merging with Advocate users
    print('Merge with advocate users...')
    ratings_stats = deepcopy(df_advocate_ratings_stats.merge(df_all_users, how='inner'))
    #Converting type of user_id
    df_rate_beer_ratings_stats.rb_user_id = df_rate_beer_ratings_stats.rb_user_id.astype(float)
    df_all_users.rb_user_id = df_all_users.rb_user_id.astype(float)

    #Merging with Rate Beer users
    print('Merge with rate beer users...')
    ratings_stats2 = deepcopy(df_rate_beer_ratings_stats.merge(df_all_users, how='inner'))
    #Concatenate the two dataframes
    print('Concatenate the two dataframes...')
    ratings_stats = pd.concat([ratings_stats, ratings_stats2], ignore_index=True)
    #Change date format
    print('Change date format...')
    ratings_stats.date = pd.to_datetime(ratings_stats.date,unit='s')
    #Add year column
    ratings_stats['year'] = ratings_stats['date'].dt.year
    #Keeping only one user name
    ratings_stats['user_name'] = ratings_stats['ba_user_name'].combine_first(ratings_stats['rb_user_name'])
    #Drop useless columns
    ratings_stats.drop(columns=['ba_user_name','rb_user_name','ba_user_id','rb_user_id','date'], inplace=True)
    #Calculate the number of ratings per year
    ratings_stats['nb_ratings'] = ratings_stats.groupby(['year','user_name'])['user_name'].transform('count')
    ratings_stats.drop_duplicates(subset=['year','user_name'],inplace=True)
    return ratings_stats