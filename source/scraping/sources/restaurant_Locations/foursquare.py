#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 31 20:54:23 2019

@author: alutes
"""
import requests
import json
import datetime
import copy

class FourSquareScraper(API_Scraper, Location_Scraper):
    BASE_URL = "https://api.foursquare.com/v2/venues/search"

    # THESE ARE MY CREDENTIALS
    BASE_PARAMS = {
                'intent' : 'browse',
                'categoryId' : '4d4b7105d754a06374d81259',
                'client_id' : 'BEZFQBVCXWN0MSFXUSS5QZGUPDSMGUDAO3GA2PGR3DY24ZNL',
                'client_secret' : 'UITWDQUFSOQ3HBOZYLDHLKMBB2IAJ35MN0RRFOR0GXQ0LOYU',
                'v' : datetime.datetime.now().strftime("%Y%m%d") # '20190404'
                }
    
    # Build Parameters based on location
    def build_params(lat_min, lat_max, lon_min, lon_max, size):
        params = copy.copy(self.BASE_PARAMS)
        params['ne'] = f"{np.round(lat_max, 2)}, {np.round(lon_max, 2)}"
        params['sw'] = f"{np.round(lat_min, 2)}, {np.round(lon_min, 2)}"
        return params
    
    # Extract data from the api
    def api_request(params):
        
        # Get the result from the api endpoint
        result = requests.get(self.BASE_URL, params = params)
        
        # Determine if we've exceeded our capacity
        if exceeded_capacity_error(result):
            raise ExceededCapicityError

        raw = json.loads(result.content.decode('utf-8'))
        data = pd.DataFrame(raw['response']['venues'])
        return data
    
    # Figure out the length of data returned
    def response_size(params):
        return len(api_request(params))

    # Capacity for a single query
    def capacity(): return 30        