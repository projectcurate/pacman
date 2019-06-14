#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 10:14:13 2019

@author: alutes
"""
from bs4 import BeautifulSoup
import multiprocessing
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os
import pandas as pd
import argparse
import requests
import math
import re
from joblib import Parallel, delayed
import multiprocessing
NUM_CORES = multiprocessing.cpu_count()
BASE_URL = "https://www.yelp.com"  

# For Rotating Proxies
# Get more here: https://www.us-proxy.org/
proxies = {'http' : 'http://108.170.48.182:3128',
           'https' : 'http://108.170.48.182:3128'} 


""" Extract all links from a page result with the given identifier
"""    
def get_links(soup, identifier):
    links = []
    # Find any links of the right format
    for a in soup.find_all('a', href=True):
        link_text = a['href']
        if identifier in link_text:
            links.append(link_text)
    return links


""" Extracts content from a given url
"""  
def get_link_content(url, endpoint, params = None):
    result = requests.get(url + endpoint, params, proxies = proxies)
    soup = BeautifulSoup(result.content, "lxml")
    return soup


def get_text(content):
    if content.hasattr(a, 'text'):
        return clean_text(content.text)

def clean_text(text):
    return text.strip("[\n| ]")


""" Converts a location and mile radius to a bounding box
"""
def build_bounding_box(size, lat, lon, r_earth = 3958.8):
    dx = (size / r_earth) * (180 / math.pi) / math.cos(lat * math.pi / 180)
    dy = (size / r_earth) * (180 / math.pi)
    return {
       'lon_min' : lon - dx / 2,
       'lon_max' : lon + dx / 2,
       'lat_min' : lat - dy / 2,
       'lat_max' : lat + dy / 2
       }

def build_location_query(size, lat, lon):  
    box = build_bounding_box(size, lat, lon)
    return {'l' : 'g:{lon_max},{lat_max},{lon_min},{lat_min}'.format(**box)}

        
""" Parse Paginated Results from a Location Search to get Restaurant Links
"""    
def get_restaurant_links(params, start, end, results_per_page=10, threaded=False):
    def processInput(i):            
        print(i, end = '')
        proc_params = params.copy()
        proc_params['start'] = i
        soup = get_link_content(url = BASE_URL, endpoint = '/search', params = page_params)
        return get_links(soup, '/biz/')
        
    inputs = range(start, end, results_per_page) 
    if(threaded):            
        links = Parallel(n_jobs=NUM_CORES)(delayed(processInput)(i) for i in inputs)
    else:
        links = []
        for i in inputs:
            links += processInput(i)
    return set(links)

""" Just determine the number of results
"""  
def extract_result_length(soup):
    # Text showing number of results
    result_length = 0
    result_length_text = [p.text for p in soup.find_all('p') if 'Showing' in p.text]
    try:
        # Parse out the actual number
        result_length = int(re.sub('Showing \d+-\d+ of ', '', result_length_text[0]))
    
    # Most unhelpful thing ever 
    except:
        print("Failed to parse number of results for some reason")
        
    return result_length


""" Ugly-ASS search of all DC
    just mess with the lat/lon to get a different bounding box
    There is an effective search limit of 1000 as you cannot go beyond page 100
    So if you see >1000 results we zoom in and split up the search recursively
    Defaults to center of DC with a box of size 100 miles
"""
def search_location_restaurants(size = 100, lat = 38.897416, lon = -77.036496, max_length = 1000):
    
    # Search the given location and size
    query_params = build_location_query(size, lat, lon)
    soup = get_link_content(BASE_URL, endpoint = '/search', params = query_params)
    result_length = extract_result_length(soup)
    
    # If result is too big then split it up
    if result_length > max_length:
        new_centers = build_bounding_box(size / 2, lat, lon)
        return  search_location_restaurants(size / 2, new_centers['lat_min'], new_centers['lon_min']) | search_location_restaurants(size / 2, new_centers['lat_max'], new_centers['lon_min']) | search_location_restaurants(size / 2, new_centers['lat_min'], new_centers['lon_max']) | search_location_restaurants(size / 2, new_centers['lat_max'], new_centers['lon_max'])

    # Otherwise, parse this result
    else:
        print(f"searching {lat}, {lon} within {size} miles, and got {result_length} stores")
        links = set(get_links(soup, '/biz/'))
        return links | get_restaurant_links(params = query_params, start=10, end = results_length)

""" Parses restaurant homepage
"""    
def soup_to_dict_restaurant(soup):
    
    # Find the relevant parts of the web page
    num_review = get_text(soup.find("span", { "class" : "review-count rating-qualifier" }))
    tags = [get_text(c) for c in soup.find("span", {"class" : "category-str-list"}).find_all("a")]
    restaurant_name_content = soup.find_all("h1", { "class" : "biz-page-title embossed-text-white" })
    
    # Contact Info
    phone = get_text(soup.find("span", {"class" : "biz-phone"}))
    website_links = [get_text(c) for c in get_links(soup, '/biz_redir')]
    address = get_text(soup.find("address"))
    
    @todo: Finish this
     
    # Parse each and add to dictionary
    info_dict = {
        'url' : url,
        'time' : timestamp,
        'company' : company,
        'body' : body,
        'comments' : comments
        }
    return(info_dict)


""" Given a single restaurant link, get all its basic info and reviews
"""  
def get_all_restaurants_info(links, all_reviews = False):
    for link in links:
        # Get the page content
        soup = get_link_content(BASE_URL + link)
        
        # Parse it to find primary restaurant info
        restaurant_dict = soup_to_dict_restaurant(soup)
        
        # Get all the reviews on this page
        review_dicts = soup_to_dict_reviews(soup)
        
        @todo: Finish this      