# -*- coding: utf-8 -*-
# -*- author : Vincent Roduit -*-
# -*- date : 2023-11-12 -*-
# -*- Last revision: 2023-11-12 -*-
# -*- python version : 3.12.0 -*-
# -*- Description: Create the dataset of all users -*-

#import libraries
import numpy as np
from copy import deepcopy
import pandas as pd

def create_all_users(df_advocate_users, df_matched_beer_users, df_rate_beer_users,debug=False):

    #Create a copy of the dataframes
    advocate = deepcopy(df_advocate_users)
    matched = deepcopy(df_matched_beer_users)
    rate_beer = deepcopy(df_rate_beer_users)

    #convert columns to right type
    # -*- matched -*-
    string_columns = ['ba.1','ba.4','ba.5','ba.6','rb.1','rb.3','rb.4','rb.5']
    matched[string_columns] = matched[string_columns].astype(str)
    int_columns = ['ba.2','ba.3','rb.2']
    matched[int_columns] = matched[int_columns].astype(int)

    ########################################################
                # -*-  Merging with advocate -*-
    ########################################################
    #Change matched columns names to match Beer Advocate
    matched = matched.rename(columns={'ba.2': 'nbr_ratings', 'ba.3': 'nbr_reviews', 'ba.4': 'user_id', 'ba.5': 'user_name', 'ba': 'joined', 'ba.1': 'location'})
    #Index where to merge with Beer Advocate
    index_merge = ['nbr_ratings', 'nbr_reviews', 'user_id', 'user_name', 'joined','location']
    #Merging with Beer Advocate
    df_dataset_users = pd.merge(
        advocate, 
        matched, how='left', 
        on=index_merge,
    )
    #verify that all the users are matched
    if(debug):
        df_dataset_users.shape[0] - df_dataset_users.rb.isna().sum() == matched.shape[0]

    ########################################################
                # -*-  Merging with Rate Beer -*-
    ########################################################
    #Format column name to perform merge on Rate Beer
    df_dataset_users = df_dataset_users.rename(columns={'nbr_ratings': 'ba_nbr_ratings', 'nbr_reviews': 'ba_nbr_reviews', 'user_id': 'ba_user_id', 'user_name': 'ba_user_name', 'joined': 'ba_joined', 'location': 'ba_location'})
    df_dataset_users = df_dataset_users.rename(columns={'rb':'joined','rb.1':'location','rb.2':'nbr_ratings','rb.3':'user_id','rb.4':'user_name','rb.5':'user_name_lower'})
    index_merge = ['joined', 'location', 'nbr_ratings', 'user_id', 'user_name']
    #Convert user_id type for merging
    df_dataset_users.user_id = df_dataset_users.user_id.astype(float)
    rate_beer.user_id = rate_beer.user_id.astype(float)
    #Merging with Rate Beer
    df_dataset_users = df_dataset_users.merge(rate_beer, how='outer', on=index_merge)
    #Keep only columns of interest
    df_dataset_users = df_dataset_users[['ba_user_id','location','joined','user_id','user_name']]
    if(debug):
        #verify the result
        df_dataset_users.shape[0] == df_advocate_users.shape[0] + rate_beer.shape[0] - matched.shape[0]
    df_dataset_users.rename(columns={'user_id':'rb_user_id','user_name':'rb_user_name'}, inplace=True)
    return df_dataset_users