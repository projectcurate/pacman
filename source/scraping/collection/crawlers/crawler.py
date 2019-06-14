#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 16:31:28 2019

@author: alutes
"""

from abc import ABC, abstractmethod
 
"""Crawler will iterate through some set of pre-defined parameters

This class will be an abstract defined by implementations of a few functions.
It will include some form of contract with Scraper() object in order to loop
through a parameter set.

Example:
    See foursquare.py for implementations

Attributes:
    DEFAULT_PARAMS (dict): Defines a set of parameters which will always be
    passed along to the other
    
    scraperObj (scraper): Defines the actions which will be performed for each
    parameter set. Allows you to pass the next set of params.
    
"""
class Crawler(scraperObj):
 
    def __init__(self, value):
        self.value = value
        super().__init__()
    
    @abstractmethod
    def iter(self):
        pass