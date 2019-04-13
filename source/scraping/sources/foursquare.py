#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 31 20:54:23 2019

@author: alutes
"""
import requests
import os
import pandas as pd
import re
import json
import boto

BASE_URL = "https://api.foursquare.com/v2/venues/search"

# THESE ARE MY CREDENTIALS SO DON'T FUCK WITH IT -alutes
DEFAULT_PARAMS = {
            'intent' : 'browse',
            'categoryId' : '4d4b7105d754a06374d81259',
            'client_id' : 'BEZFQBVCXWN0MSFXUSS5QZGUPDSMGUDAO3GA2PGR3DY24ZNL',
            'client_secret' : 'UITWDQUFSOQ3HBOZYLDHLKMBB2IAJ35MN0RRFOR0GXQ0LOYU',
            'v' : '20190404'
            }

# Take in params and find 
def params_to_df(search_params = {'ne' : '38.92,-77.00', 'sw' : '38.88, -77.11'}):
    
    # Combine defaults and new search params
    params = DEFAULT_PARAMS
    params.update(search_params)
    
    # Hit the API
    result = requests.get(BASE_URL, params = params)
    
    # Convert to DF
    jsonData = json.loads(result.content.decode('utf-8'))
    data = pd.DataFrame(jsonData['response']['venues'])

    return data


