import numpy as np
import pandas as pd

def compute_expert_score(row,weight_y=2,weight_y_1=0.5,weight_y_2=0.25,weight_y_3=0.1):
    min_year = int(row.index[0])
    max_year = int(row.index[-1])
    for j in range(min_year + 3, max_year + 1):
        try:
            row[j] = weight_y * row[j] + weight_y_1 * row[j-1] + weight_y_2 * row[j-2] + weight_y_3 * row[j-3]
        except:
            continue
    return row

def normalized_score(col):
    # Min-Max Scaling
    max_score = np.max(col)
    min_score = np.min(col)
    col = (col - min_score) / (max_score - min_score)
    return col

def is_expert(score, threshold=0.4):
    return score >= threshold

def compute_experts_table(df_ratings):
    df_user_ratings_per_year = df_ratings.groupby(['user_id', 'year']).size().reset_index(name='nb_ratings')
    df_ratings_stat_pivot = df_user_ratings_per_year.pivot(index='user_id', columns='year', values='nb_ratings')
    df_ratings_stat_pivot.fillna(0, inplace=True)
    df_ratings_stat_pivot_score = df_ratings_stat_pivot.apply(compute_expert_score, axis=1)
    df_ratings_stat_pivot_score_norm = df_ratings_stat_pivot_score.apply(normalized_score, axis=0)
    df_ratings_stat_pivot_expert = is_expert(df_ratings_stat_pivot_score_norm)
    df_reset = df_ratings_stat_pivot_expert.reset_index()
    df_melted = pd.melt(df_reset, id_vars=['user_id'], var_name='year', value_name='is_expert')
    df_ratings_stat_expert = df_user_ratings_per_year.merge(df_melted)
    return df_ratings_stat_expert, df_ratings_stat_pivot_expert


def filter_year_and_add_is_expert(df,YEAR,experts_table):
    experts_year=experts_table[experts_table[YEAR]==True].index
    df_this_year=df[df["year"]==YEAR]
    df_this_year["is_expert"] = df_this_year["user_id"].isin(experts_year).astype(int)
    return df,experts_year