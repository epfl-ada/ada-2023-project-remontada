# -*- coding: utf-8 -*-
# -*- author : Vincent Roduit -*-
# -*- date : 2023-12-08 -*-
# -*- Last revision: 2023-12-10 -*-
# -*- python version : 3.12.0 -*-
# -*- Description: Function to visualize results -*-

# import libraries
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# import files
def plot_top_words(top_words, title):
    plt.figure(figsize=(5,5))
    sns.barplot(x="count", hue="Common_words", data=top_words, palette="viridis")
    plt.title(f'Most Common Words for {title}')
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.show()