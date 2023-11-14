# -*- coding: utf-8 -*-
# -*- author : Vincent Roduit -*-
# -*- date : 2023-11-12 -*-
# -*- Last revision: 2023-11-14 -*-
# -*- python version : 3.12.0 -*-
# -*- Description: Create the dataset of all users -*-

#import libraries
import pandas as pd

def read_txt(file_path):
    data_list = []
    with open(file_path, 'r') as file:
        file_content = file.read()

    entries = file_content.split('\n\n')

    for entry in entries:

        entry_dict = {}
        entry_lines = entry.strip().split('\n')
        
        for line in entry_lines:

            parts = line.strip().split(':')
            if len(parts) == 2:
                column, value = parts[0].strip(), parts[1].strip()
                entry_dict[column] = value

        data_list.append(entry_dict)

    df = pd.DataFrame(data_list)
    
    return df
