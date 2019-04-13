#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 16:47:37 2019

@author: alutes
"""

from abc import ABC, abstractmethod
 
class Scraper(scraper):
 
    def __init__(self, value):
        self.value = value
        super().__init__()
    
    @abstractmethod
    def do_something(self):
        pass