import numpy as np
import pandas as pd

def compute_expert_score(row,weight_y=2,weight_y_1=0.5,weight_y_2=0.25,weight_y_3=0.1):
    row_copy=row.copy()
    average_norm=weight_y+weight_y_1+weight_y_2+weight_y_3
    for j in range(1996 + 3, 2017 + 1):
        row[j] = (weight_y * row_copy[j] + weight_y_1 * row_copy[j-1] + weight_y_2 * row_copy[j-2] + weight_y_3 * row_copy[j-3])/average_norm
        
    return row

def normalized_score(col):
    # Min-Max Scaling
    max_score = np.max(col)
    min_score = np.min(col)
    col = (col - min_score) / (max_score - min_score)
    return col

def is_expert(score, threshold=0.4):
    return score >= threshold

def compute_experts_table(df_ratings,quantile_score_expert=0.995):
    df_user_ratings_per_year = df_ratings.groupby(['user_id', 'year']).size().reset_index(name='nb_ratings')
    df_ratings_stat_pivot = df_user_ratings_per_year.pivot(index='user_id', columns='year', values='nb_ratings')
    df_ratings_stat_pivot.fillna(0, inplace=True)
    df_ratings_stat_pivot[1997]=np.zeros(df_ratings_stat_pivot.shape[0])
    df_ratings_stat_pivot = df_ratings_stat_pivot.reindex(columns=[df_ratings_stat_pivot.columns[0]] + [1997] + list(df_ratings_stat_pivot.columns[1:-1]))
    df_ratings_stat_pivot_score = df_ratings_stat_pivot.apply(compute_expert_score, axis=1)
    print("ok")
    df_ratings_stat_pivot_expert = df_ratings_stat_pivot_score.gt(df_ratings_stat_pivot_score[df_ratings_stat_pivot_score.gt(0)].quantile(quantile_score_expert))

    df_reset = df_ratings_stat_pivot_expert.reset_index()
    df_melted = pd.melt(df_reset, id_vars=['user_id'], var_name='year', value_name='is_expert')
    df_ratings_stat_expert = df_user_ratings_per_year.merge(df_melted)
    return df_ratings_stat_expert, df_ratings_stat_pivot_expert


def filter_year_and_add_is_expert(df,YEAR,experts_table):
    experts_year=experts_table[experts_table[YEAR]==True].index
    df_this_year=df[df["year"]==YEAR]
    df_this_year["is_expert"] = df_this_year["user_id"].isin(experts_year).astype(int)
    return df_this_year,experts_year