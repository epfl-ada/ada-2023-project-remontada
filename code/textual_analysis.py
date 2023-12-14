# -*- coding: utf-8 -*-
# -*- author : Vincent Roduit -*-
# -*- date : 2023-12-08 -*-
# -*- Last revision: 2023-12-10 (Vincent) -*-
# -*- python version : 3.12.0 -*-
# -*- Description: Function used for textual analysis -*-

# import libraries
from langdetect import detect
from langdetect import DetectorFactory
DetectorFactory.seed = 0
import pandas as pd
import os
from copy import deepcopy
from string import punctuation
import spacy
from collections import Counter 
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import concurrent.futures
from tqdm import tqdm
from nltk import bigrams

#import files
from read.pickle_functions import load_pickle

EXCLUDE_CHARS = set(punctuation).union(set('’'))


def create_text_dataset(df_advocate_reviews,df_rate_beer_reviews, df_all_users,experts_dict):
    """Create the dataset of rating statistic of all users
    Args:
        df_advocate_ratings (dataframe): dataframe of advocate ratings
        df_rate_beer_ratings (dataframe): dataframe of rate beer ratings
        df_all_users (dataframe): dataframe of all users
    Returns:
        ratings_stats (dataframe): dataframe of rating statistic of all users
    """
    path = '../datas/processed/'
    file = 'df_text_stats.pkl'
    if os.path.exists(path+file):
        print('Loading the dataframe in pickle format from ',path)
        ratings_stats = load_pickle(path+file)
    else:
        #Create a copy of the dataframes
        print('Creating copies...')
        df_advocate_reviews_stats = deepcopy(df_advocate_reviews)
        df_rate_beer_reviews_stats = deepcopy(df_rate_beer_reviews)

        #process the dataframes
        print('processing dataframes...')
        df_advocate_reviews_stats.rename(columns={'user_name':'ba_user_name'}, inplace=True)
        df_rate_beer_reviews_stats.rename(columns={'user_name':'rb_user_name'}, inplace=True)

        #Merge the dataframes
        print('Merging dataframes...')
        ratings_stats = deepcopy(df_advocate_reviews_stats.merge(df_all_users, how='inner'))
        ratings_stats['user_id'] = ratings_stats['user_id'].rename('ba_user_id')
        df_rate_beer_reviews_stats.user_id = df_rate_beer_reviews_stats.user_id.astype(int)
        df_rate_beer_reviews_stats.user_id = df_rate_beer_reviews_stats.user_id.astype(object)
        ratings_stats2 = deepcopy(df_rate_beer_reviews_stats.merge(df_all_users, how='inner', on='rb_user_name'))
        ratings_stats2['user_id'] = ratings_stats2['user_id_y'].fillna(ratings_stats2['user_id_x'])
        ratings_stats2.drop(columns=['user_id_x','user_id_y'], inplace=True)

        #Concatenate the dataframes
        print('Concatenating dataframes...')
        ratings_stats = pd.concat([ratings_stats,ratings_stats2],axis=0)

        #compute year where the review was written
        ratings_stats["year"]=ratings_stats["date"].dt.year
            
        ratings_stats["is_expert"]=ratings_stats[["user_id","year"]].apply(
            lambda x: 1 if x["user_id"] in experts_dict[x["year"]] else 0,axis=1)

        #Order the columns
        ordered_cols = [
            'year',
            'location',
            'user_id',
            'text',
            'is_expert'
        ]
        ratings_stats = ratings_stats[ordered_cols]

    return ratings_stats

def detect_language(text):
    """ Detect the language of a text
    Args:
        text (str): Text to analyze
    Returns:
        str: Language of the text
    """
    try:
        # Add a check for non-empty and sufficiently long text
        if text and len(text) > 10:
            return detect(text)
        else:
            return None
    except Exception as e:
        print(f"Error detecting language for text: {text}. Error: {str(e)}")
        return None
    
def calculate_nb_words(text):
    """ Calculate the length of a text
    Args:
        text (str): Text to analyze
    Returns:
        int: Length of the text
    """
    try:
        return len(text.split())
    except Exception as e:
        print(f"Error calculating length for text: {text}. Error: {str(e)}")
        return None

def compute_text_stats(df_texts):
    """ Compute the statitics of a text column
    Args:
        texts (Series): Texts to analyze
    Returns:
        DataFrame: DataFrame containing the statistics of the texts
    """
    df_texts_expert,df_texts_casual = None, None
    if os.path.exists('../datas/processed/df_texts_expert.pkl'):
        print('Loading the dataframe in pickle format from ../datas/processed/')
        df_texts_expert = load_pickle('../datas/processed/df_texts_expert.pkl')
    if os.path.exists('../datas/processed/df_texts_casual.pkl'):
        print('Loading the dataframe in pickle format from ../datas/processed/')
        df_texts_casual = load_pickle('../datas/processed/df_texts_casual.pkl')
    if df_texts_casual is None or df_texts_expert is None:
        # Detect the language of the texts
        df_texts.text = df_texts.text.str.lower()
        print('Detecting language and count the number of words...')
        with concurrent.futures.ThreadPoolExecutor() as executor:
            df_texts['language'] = list(tqdm(executor.map(detect_language_wrapper, df_texts['text']), total=len(df_texts)))

            df_texts['nb_words'] = list(tqdm(executor.map(calculate_nb_words_wrapper, df_texts['text']), total=len(df_texts)))

        # Only keep the English texts
        df_texts = df_texts[df_texts['language'] == 'en']

        # Separate the experts from the others
        df_texts_expert = df_texts[df_texts['is_expert'] == 1]
        df_texts_casual = df_texts[df_texts['is_expert'] == 0]

        df_texts_casual = df_texts_casual.sample(len(df_texts_expert), random_state=42)

        # Add number of reviews
        df_texts_expert['nb_reviews'] = df_texts_expert.groupby('user_id')['user_id'].transform('size')
        df_texts_casual['nb_reviews'] = df_texts_casual.groupby('user_id')['user_id'].transform('size')

        df_texts_expert = tokenize(df_texts_expert)
        df_texts_casual = tokenize(df_texts_casual)

        df_texts_expert = add_bigrams(df_texts_expert)
        df_texts_casual = add_bigrams(df_texts_casual)
    
    return df_texts_expert, df_texts_expert

def compute_top_words_adjectives(df):
    nlp = spacy.load('en_core_web_sm')
    words = Counter([item for sublist in tqdm(df['tokens'], desc="Processing tokens") for item in sublist])
    top_words = pd.DataFrame(words.most_common())
    top_words.columns=['common_words','count_words']
    top_words['count_words'] = top_words['count_words'] / df['nb_reviews'].sum()
    top_words.sort_values(by=['count_words'], inplace=True, ascending=False)

    adj = []
    count_adj = []
    for top_word,count_word in zip(top_words['common_words'],top_words['count_words']):
        if nlp(top_word)[0].pos_ == 'ADJ':
            adj.append(top_word)
            count_adj.append(count_word)
        if len(adj) == 20:
            break
    top_words = top_words[:20]
    top_words['common_adj'] = adj
    top_words['count_adj'] = count_adj
    return top_words

def analyze_sentiment(text, analyzer):
    """ Analyze the sentiment of a text
    Args:
        text (str): Text to analyze
        analyzer (SentimentIntensityAnalyzer): Analyzer to use
    Returns:
        dict: Dictionary containing the sentiment scores
    """
    try:
        return analyzer.polarity_scores(text)
    except Exception as e:
        print(f"Error analyzing sentiment for text: {text}. Error: {str(e)}")
        return None
    

def detect_language_wrapper(x):
    return detect_language(x)

def calculate_nb_words_wrapper(x):
    return calculate_nb_words(x)

def analyze_sentiment_wrapper(x):
    analyzer = SentimentIntensityAnalyzer()
    return analyze_sentiment(x, analyzer)

def tokenize_texts(text, nlp):
    doc = nlp(text)
    
    # Extract each token and filter out stopwords and tokens in EXCLUDE_CHARS
    filtered_tokens = [token.lemma_ for token in doc if not token.is_punct and not token.is_stop]    
    # Remove empty strings or tokens consisting only of whitespace characters
    filtered_tokens = [token for token in filtered_tokens if token.strip() != '']

    return filtered_tokens

def tokenize(df_texts):
    # Compute the statistics
    print('Tokenizing...')
    nlp = spacy.load('en_core_web_sm')
    with concurrent.futures.ThreadPoolExecutor() as executor:
        df_texts['tokens'] = list(tqdm(executor.map(tokenize_texts, df_texts['text'], [nlp]*len(df_texts)), total=len(df_texts)))
    return df_texts

def compute_bigrams(text):
    return list(bigrams(text))

def add_bigrams(df_texts):
    print('Computing bigrams...')
    with concurrent.futures.ThreadPoolExecutor() as executor:
        df_texts['bigrams'] = list(tqdm(executor.map(compute_bigrams, df_texts['tokens']), total=len(df_texts)))
    return df_texts

def compute_top_bigrams(df_texts):
    all_bigrams = [bigram for bigrams in df_texts['bigrams'] for bigram in bigrams]
    bigram_counts = Counter(all_bigrams)
    return bigram_counts

def sentiment(df_texts):
    # Compute the statistics
    print('Analyzing sentiment...')
    with concurrent.futures.ThreadPoolExecutor() as executor:
        df_texts['sentiment'] = list(tqdm(executor.map(analyze_sentiment_wrapper, df_texts['text']), total=len(df_texts)))
        # Extract sentiment scores into separate columns
        df_texts[['Neg_sentiment', 'Neu_sentiment', 'Pos_sentiment', 'Comp_sentiment']] = pd.DataFrame(df_texts['sentiment'].tolist(), index=df_texts.index)
    return df_texts