#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 16:47:37 2019

@author: alutes
"""

from abc import ABC, abstractmethod
import pandas as pd
 
class Scraper():
    
"""Scraper will define the necessary methods for processing data 
    from heterogeneous sources.

This class will be an abstract defined by implementations of a few functions.
It will include some form of contract with the Crawler() object in order to loop
through a parameter set and scrape data along the way.

Example:
    See foursquare.py for implementations

Attributes:
    DEFAULT_PARAMS (dict): Defines a set of parameters which will always be
    passed along to the other
    
    scraperObj (scraper): Defines the actions which will be performed for each
    parameter set. Allows you to pass the next set of params.
    
"""
    def __init__(self, crawler: Crawler, serializer: Serializer, initParams):
        self.crawler = crawler(initParams)
        self.serializer = serializer()
        self.initialize_serialization(initParams)
        self.initialize_dataset()
        super().__init__()

    def initialize_dataset(self):
        self.dataset = pd.DataFrame()

    def initialize_serialization(self):
        self.output_path = initParams['output_path']
        self.max_size = initParams['max_size']

    def append_rows(self):
        self.dataset = pd.concat()

    def serialize(self):
        self.serializer.serialize(self.dataset)

    def truncate(self):
        self.dataset.truncate()

    @abstractmethod
    def fetch_new_rows(self, params):
        pass
    
    def run(self):
        for params in self.crawler.iter():
            new_rows = self.fetch_new_rows(params)
            self.append_rows(new_rows)
            if len(self.dataset) > max_size:
                self.serialize()
                self.truncate()
        self.serialize()