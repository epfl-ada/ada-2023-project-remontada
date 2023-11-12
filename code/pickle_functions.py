# -*- coding: utf-8 -*-
# -*- author : Vincent Roduit -*-
# -*- date : 2023-11-03 -*-
# -*- Last revision: 2023-11-03 -*-
# -*- python version : 3.12.0 -*-
# -*- Description: Functions used to save and load pickle datas -*-

#import libraries
import os
import pickle


def save_pickle(result, file_path = 'pickle'):
    """ Save a variable in a binary format

    Args:
        result: dataFrame
        file_path: file path where to store this variable

    Returns:
    """
    with open(file_path, 'wb') as file:
        pickle.dump(result, file)

def load_pickle(file_path):
    """ Load a variable from a binary format path

    Args:
        file_path: the file path where the file is stored

    Returns:
        return the content of the file, generally a dataFrame here.
    """
    with open(file_path, 'rb') as file:
        return pickle.load(file)
    
def save_datas(dataset_name,datas, datas_names):
    """ Save a list of datas in a binary format
    Args:
        dataset_name: str, name of the dataset
        datas: list of datas to save
        datas_names: list of datas names
    """
    path = '../datas/' + dataset_name + '/pickles/'
    if not os.path.exists(path):
        os.makedirs(path)
    for data, data_name in zip(datas, datas_names):
        print(f'Saving {data_name}...')
        file_name = data_name + '.pkl'
        save_pickle(data, path + file_name)

def load_datas(dataset_name, datas_names):
    """ Load a list of datas from a binary format path
    Args:
        dataset_name: str, name of the dataset
        datas_names: list of datas names
    Returns:
        datas: list of datas
    """
    path = '../datas/' + dataset_name + '/pickles/'
    datas = []
    for data_name in datas_names:
        print(f'Loading {data_name}...')
        file_name = data_name + '.pkl'
        datas.append(load_pickle(path + file_name))
    return (*datas,)
