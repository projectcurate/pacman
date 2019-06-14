#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 15:18:18 2019

@author: alutes
"""

class API_Scraper(Scraper):
    
    @abstractmethod
    def fetch_data(self):
        pass
    
     @abstractmethod
    def concat_data(self):
        pass
    
    @abstractmethod
    def max_size(self):
        pass

    @abstractmethod
    def write_data(self):
        pass