# -*- coding: utf-8 -*-
# -*- author : Vincent Roduit -*-
# -*- date : 2023-12-08 -*-
# -*- Last revision: 2023-11-14 -*-
# -*- python version : 3.12.0 -*-
# -*- Description: Function used for textual analysis -*-

# import libraries
from langdetect import detect
from langdetect import DetectorFactory
DetectorFactory.seed = 0

def detect_language(text):
    try:
        # Add a check for non-empty and sufficiently long text
        if text and len(text) > 3:
            return detect(text)
        else:
            return None
    except Exception as e:
        print(f"Error detecting language for text: {text}. Error: {str(e)}")
        return None