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
def plot_top_words(top_words_expert, top_words_casual):
    fig, axs = plt.subplots(1, 2, figsize=(10,7))

    sns.barplot(x="count", hue="Common_words", data=top_words_expert, ax=axs[0], palette="coolwarm")
    axs[0].set_title('Most Common Words for Experts')

    sns.barplot(x="count", hue="Common_words", data=top_words_casual, ax=axs[1], palette="coolwarm")
    axs[1].set_title('Most Common Words for Casual')

    plt.tight_layout()
    plt.show()

def plot_top_bigrams(top_bigrams_expert, top_bigrams_casual):
    # Convert the Counter objects to DataFrames
    top_bigrams_expert_df = pd.DataFrame(top_bigrams_expert.most_common(20), columns=['Common_bigrams', 'count'])
    top_bigrams_casual_df = pd.DataFrame(top_bigrams_casual.most_common(20), columns=['Common_bigrams', 'count'])

    # Convert the tuples to strings
    top_bigrams_expert_df['Common_bigrams'] = top_bigrams_expert_df['Common_bigrams'].apply(lambda x: ', '.join(x))
    top_bigrams_casual_df['Common_bigrams'] = top_bigrams_casual_df['Common_bigrams'].apply(lambda x: ', '.join(x))

    fig, axs = plt.subplots(1, 2, figsize=(10,7))

    sns.barplot(x="count", hue="Common_bigrams", data=top_bigrams_expert_df, ax=axs[0], palette="coolwarm")
    axs[0].set_title('Most Common Bigrams for Experts')

    sns.barplot(x="count", hue="Common_bigrams", data=top_bigrams_casual_df, ax=axs[1], palette="coolwarm")
    axs[1].set_title('Most Common Bigrams for Casual')

    plt.tight_layout()
    plt.show()