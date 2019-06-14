#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 15:07:15 2019

@author: alutes
"""

class Location_Scraper(Scraper):
    
    @abstractmethod
    def build_params(self):
        pass
    
     @abstractmethod
    def capacity(self):
        pass
    
    @abstractmethod
    def response_size(self):
        pass
    

    def build_bounding_box(size, lat, lon, r_earth = 3958.8):
    """ Converts a location and mile radius to a bounding box"""
    dx = (size / r_earth) * (180 / math.pi) / math.cos(lat * math.pi / 180)
    dy = (size / r_earth) * (180 / math.pi)
    return {
       'lon_min' : lon - dx / 2,
       'lon_max' : lon + dx / 2,
       'lat_min' : lat - dy / 2,
       'lat_max' : lat + dy / 2
       }


    # Defined in terms of the given functions
    def scrape_all_locations(min_lat, max_lat, min_lon, max_lon):
        
        # Scrape Each location
        
        # If its too big split it up and repeat
        
        # Go until complete
        
        return data