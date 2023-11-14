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
    return ratings_stats