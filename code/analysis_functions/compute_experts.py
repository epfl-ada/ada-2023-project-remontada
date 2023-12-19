# -*- coding: utf-8 -*-
# -*- author : Yannis Laaroussi -*-
# -*- date : 2023-11-04 -*-
# -*- Last revision: 2023-11-14 -*-
# -*- python version : 3.12.0 -*-
# -*- Description: Create table of experts-*-

# Import libraries
import numpy as np
import pandas as pd

def compute_expert_score(row,weight_y=2,weight_y_1=0.5,weight_y_2=0.25,weight_y_3=0.1):
    """Compute the expert score for a given user
    Args:
        row (Series): Series containing the number of ratings per year for a given user
        weight_y (int): weight of the current year
        weight_y_1 (int): weight of the year - 1
        weight_y_2 (int): weight of the year - 2
        weight_y_3 (int): weight of the year - 3
    Returns:
        row (Series): Series containing the expert score for a given user
    """

    #create copy of the row
    row_copy=row.copy()

    #compute the average norm
    average_norm=weight_y+weight_y_1+weight_y_2+weight_y_3

    #compute the expert score
    for j in range(1996 + 3, 2017 + 1):
        row[j] = (weight_y * row_copy[j] 
                    + weight_y_1 * row_copy[j-1] 
                    + weight_y_2 * row_copy[j-2] 
                    + weight_y_3 * row_copy[j-3]) / average_norm
        
    return row



def compute_experts_table(df_ratings,quantile_score_expert=0.995):
    """Compute the table of experts
    Args:
        df_ratings (pandas dataframe): dataframe containing the ratings
        quantile_score_expert (float): quantile to define the threshold to be an expert
    Returns:
        df_ratings_stat_expert (pandas dataframe): dataframe containing the number of ratings per user and per year
        df_ratings_stat_pivot_expert (pandas dataframe): dataframe containing the expert score per user and per year
    """
    # Compute the number of ratings per user and per year
    df_user_ratings_per_year = df_ratings.groupby(['user_id', 'year']).size().reset_index(name='nb_ratings')
    df_ratings_stat_pivot = df_user_ratings_per_year.pivot(index='user_id', columns='year', values='nb_ratings')
    df_ratings_stat_pivot.fillna(0, inplace=True)
    
    # Add the year 1997 to avoid errors(no ratings in 1997)
    df_ratings_stat_pivot[1997]=np.zeros(df_ratings_stat_pivot.shape[0])
    
    # Reorder the columns and compute the expert score
    df_ratings_stat_pivot = df_ratings_stat_pivot.reindex(columns=[df_ratings_stat_pivot.columns[0]] + [1997] + list(df_ratings_stat_pivot.columns[1:-1]))
    df_ratings_stat_pivot_score = df_ratings_stat_pivot.apply(compute_expert_score, axis=1)

#     # Compute the threshold to be an expert
    df_ratings_stat_pivot_expert = df_ratings_stat_pivot_score.gt(df_ratings_stat_pivot_score[df_ratings_stat_pivot_score.gt(0)].quantile(quantile_score_expert))

    # Reshape the dataframe so that it can be easily used later
    df_reset = df_ratings_stat_pivot_expert.reset_index()
    df_melted = pd.melt(df_reset, id_vars=['user_id'], var_name='year', value_name='is_expert')
    df_ratings_stat_expert = df_user_ratings_per_year.merge(df_melted)
    
    return df_ratings_stat_expert, df_ratings_stat_pivot_expert


def filter_year_and_add_is_expert(df,YEAR,experts_table):

    """Filter the dataframe by year and add the column is_expert
    Args:
        df (pandas dataframe): dataframe containing the ratings
        YEAR (int): year to filter the dataframe
        experts_table (pandas dataframe): dataframe containing the experts
    Returns:
        df_this_year (pandas dataframe): dataframe containing the ratings for the given year
        experts_year (pandas dataframe): dataframe containing the experts for the given year
    """

    # compute experts for the given year
    experts_year=experts_table[(experts_table["year"]==YEAR) & (experts_table["is_expert"]==True)].user_id.values.astype(str).tolist()
    
    # filter the dataframe by year
    df_this_year=df[df["year"]==YEAR]
    
    # add the column is_expert
    df_this_year["is_expert"] = df_this_year["user_id"].isin(experts_year).astype(int)
    
    return df_this_year,experts_year