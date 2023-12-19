# -*- coding: utf-8 -*-
# -*- author : Vincent Roduit -*-
# -*- date : 2023-11-12 -*-
# -*- Last revision: 2023-11-14 -*-
# -*- python version : 3.12.0 -*-
# -*- Description: Create the dataset of all users -*-

#import libraries
import numpy as np
import os
from copy import deepcopy
import pandas as pd
from read.pickle_functions import load_pickle

def create_all_users(df_advocate_users, df_matched_beer_users, df_rate_beer_users):
    """Create the dataset of all users
    Args:
        df_advocate_users (dataframe): dataframe of advocate users
        df_matched_beer_users (dataframe): dataframe of matched beer users
        df_rate_beer_users (dataframe): dataframe of rate beer users
    Returns:
        df_datasets_users (dataframe): dataframe of all users
    """

    #check if the dataframe already exists
    path = '../datas/results/'
    file = 'df_all_users.pkl'
    if os.path.exists(path+file):
        print('Loading the dataframe in pickle format from ',path)
        df_datasets_users = load_pickle(path+file)
    else:
        #Create a copy of the dataframes
        advocate = deepcopy(df_advocate_users)
        matched = deepcopy(df_matched_beer_users)
        rate_beer = deepcopy(df_rate_beer_users)
        #Drop the columns that are not needed
        advocate = advocate[['ba_user_id','ba_user_name','ba_joined','ba_location']]
        rate_beer = rate_beer[['rb_user_id','rb_user_name','rb_joined','rb_location']]
        matched = matched[['ba_joined',
                           'ba_location',
                           'ba_user_id',
                           'ba_user_name',
                           'rb_joined',
                           'rb_location',
                           'rb_user_id',
                           'rb_user_name'
                           ]]

        #Merge the dataframes
        df_dataset_users_advocate = pd.merge(advocate,matched,how='left')
        matched.rb_user_id = matched.rb_user_id.astype('int64')
        df_dataset_users_rate_beer = pd.merge(rate_beer,matched,how='left')

        #Concatenate the dataframes
        df_datasets_users = pd.concat([df_dataset_users_advocate,df_dataset_users_rate_beer],axis=0)

        #Wrap duplicate values to a single column
        df_datasets_users['user_id'] = df_datasets_users['ba_user_id'].fillna(df_datasets_users['rb_user_id'])
        df_datasets_users['location'] = df_datasets_users['ba_location'].fillna(df_datasets_users['rb_location'])
        df_datasets_users['joined'] = df_datasets_users['ba_joined'].fillna(df_datasets_users['rb_joined'])

        #drop unnecessary columns
        df_datasets_users.drop(columns=['ba_user_id','ba_location','ba_joined','rb_user_id','rb_location','rb_joined'], inplace=True)

        #drop duplicate users
        df_datasets_users.drop_duplicates(subset = 'user_id', inplace = True)
    return df_datasets_users