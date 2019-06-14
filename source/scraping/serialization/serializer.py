#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 16:31:28 2019

@author: alutes
"""

from abc import ABC, abstractmethod
 
"""Serializer will serialize data to a file or database

This class will be an abstract defined by implementations of a few functions.
It will include some form of contract with Scraper() object in order to write
data as it is scraped.

Example:
    See foursquare.py for implementations

Attributes:
    DEFAULT_PARAMS (dict): Defines a set of parameters which will always be
    passed along to the other
    
    scraperObj (scraper): Defines the actions which will be performed for each
    parameter set. Allows you to pass the next set of params.
    
"""
class Serializer(scraperObj):
 
    def __init__(self, value):
        self.value = value
        super().__init__()
    
    @abstractmethod
    def serialize(self):
        pass