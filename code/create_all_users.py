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
    advocate = advocate[['user_id','user_name','joined','location']]
    advocate.rename(columns={'user_id': 'ba_user_id', 
                            'user_name': 'ba_user_name',
                            'joined': 'ba_joined',
                            'location': 'ba_location'},
                            inplace=True)

    matched = deepcopy(df_matched_beer_users)
    matched = matched[['ba','ba.1','ba.4','ba.5','rb','rb.1','rb.3','rb.4']]
    matched.rename(columns={'ba': 'ba_joined',
                            'ba.1': 'ba_location',
                            'ba.4': 'ba_user_id',
                            'ba.5': 'ba_user_name',
                            'rb': 'rb_joined',
                            'rb.1': 'rb_location',
                            'rb.3': 'rb_user_id',
                            'rb.4': 'rb_user_name'},
                            inplace=True)
    rate_beer = deepcopy(df_rate_beer_users)
    rate_beer = rate_beer[['user_id','user_name','joined','location']]
    rate_beer.rename(columns={'user_id': 'rb_user_id', 
                            'user_name': 'rb_user_name',
                            'joined': 'rb_joined',
                            'location': 'rb_location'},
                            inplace=True)
    df_dataset_users_advocate = pd.merge(advocate,matched,how='left')
    matched.rb_user_id = matched.rb_user_id.astype('int64')
    df_dataset_users_rate_beer = pd.merge(rate_beer,matched,how='left')
    df_datasets_users = pd.concat([df_dataset_users_advocate,df_dataset_users_rate_beer],axis=0)
    df_datasets_users['user_id'] = df_datasets_users['ba_user_id'].fillna(df_datasets_users['rb_user_id'])
    df_datasets_users['location'] = df_datasets_users['ba_location'].fillna(df_datasets_users['rb_location'])
    df_datasets_users['joined'] = df_datasets_users['ba_joined'].fillna(df_datasets_users['rb_joined'])
    df_datasets_users.drop(columns=['ba_user_id','ba_location','ba_joined','rb_user_id','rb_location','rb_joined'], inplace=True)
    df_datasets_users.drop_duplicates(subset = 'user_id', inplace = True)
    return df_datasets_users