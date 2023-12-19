# -*- coding: utf-8 -*-
# -*- author : Vincent Roduit -*-
# -*- date : 2023-11-12 -*-
# -*- Last revision: 2023-11-14 -*-
# -*- python version : 3.12.0 -*-
# -*- Description: Create the dataset of all users -*-

# import libraries
import pandas as pd
import ftfy


def read_txt(file_path):
    """Reads a text file and returns a DataFrame with the extracted parameters
    Args:
        file_path (str): Path to the text file
    Returns:
        DataFrame: DataFrame with the extracted parameters
    """
    with open(file_path, "rb") as file:
        raw_data = file.read()

    sections = raw_data.split(b"\n\n")

    extracted_data = []

    for section in sections:
        # Extract parameters
        parameters = {}
        for line in section.decode("utf-8").split("\n"):
            if ":" in line:
                key, value = map(str.strip, line.split(":", 1))

                parameters[key] = ftfy.fix_text(value)

        extracted_data.append(parameters)

    return pd.DataFrame(extracted_data)
