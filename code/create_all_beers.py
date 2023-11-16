# -*- coding: utf-8 -*-
# -*- author : Vincent Roduit -*-
# -*- date : 2023-11-03 -*-
# -*- Last revision: 2023-11-03 -*-
# -*- python version : 3.9.13 -*-
# -*- Description: Functions used to create a DataFrame of all beers -*-

# import libraries
import os
import pandas as pd
import numpy as np

def create_all_beers(df_adv_beers, df_rb_beers, df_mb_beers):
    columns_to_keep = ['beer_id','beer_name','brewery_id','brewery_name','style']
    columns_to_keep_adv = ['ba_' + col for col in columns_to_keep]
    columns_to_keep_rb = ['rb_' + col for col in columns_to_keep]
    columns_to_keep_mb = np.concatenate((columns_to_keep_adv, columns_to_keep_rb))
    df_adv_beers = df_adv_beers[columns_to_keep_adv]
    df_rb_beers = df_rb_beers[columns_to_keep_rb]
    df_mb_beers = df_mb_beers[columns_to_keep_mb]
    df_adv_merged = df_adv_beers.merge(df_mb_beers, how='left')
    df_rb_merged = df_rb_beers.merge(df_mb_beers, how='left')
    df_all_beers = pd.concat([df_adv_merged, df_rb_merged])
    df_all_beers['beer_unique_id'] = df_all_beers['ba_beer_id'].fillna(df_all_beers['rb_beer_id'])
    df_all_beers['brewery'] = df_all_beers['ba_brewery_name'].fillna(df_all_beers['rb_brewery_name'])
    df_all_beers['style'] = df_all_beers['ba_style'].fillna(df_all_beers['rb_style'])
    df_all_beers['beer_name'] = df_all_beers['ba_beer_name'].fillna(df_all_beers['rb_beer_name'])
    df_all_beers.drop(columns=['ba_brewery_name','ba_style','ba_beer_name'
                               ,'rb_brewery_name','rb_style','rb_beer_name'], inplace=True)
    df_all_beers.drop_duplicates(subset=['beer_unique_id'], inplace=True)
    return df_all_beers
