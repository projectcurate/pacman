#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 22:00:20 2019

@author: alutes
"""

""" Scratch code with snippets used to thread process. Turns out this just gets us blocked faster
"""
def threading_selenium():
    # Threaded Scraping    
    NUM_DRIVERS = 5
    pool = multiprocessing.Pool(NUM_DRIVERS)
    drivers = [webdriver.Chrome("Downloads/chromedriver", chrome_options=chrome_options) for i in range(0, NUM_DRIVERS)]
    pages_info = pool.map(parse_article_page, range(0, 1000))
     
    # Close Windows
    for i in range(0, NUM_DRIVERS):
        drivers[i].close()
 
       
def add_sneaky_cookies(driver, 
                       newSession=False, 
                       dummy_url="https://www.google.com/webhp?hl=en"):
    
    # Send the browser somewhere to get a session going
    if newSession:
        driver.get(dummy_url)
    
    # Add cookies to pretend to be human
    sneaky_cookies = [{'domain': 'https://www.yelp.com/',
          'expiry': time.time()-1,
          'httpOnly': False,
          'name': 'machine_cookie',
          'path': '/',
          'secure': False,
          'value': '4559516168363'},
         {'domain': 'seekingalpha.com',
          'expiry': time.time(),
          'httpOnly': True,
          'name': 'pxvid',
          'path': '/',
          'secure': True,
          'value': 'e3584090-3523-11e9-b639-a9539ba43fbd'}]
    
    for cookie in sneaky_cookies:
            driver.add_cookie(cookie)


def start_chrome(path):
    # Get Drivers
    chrome_options = Options()
    chrome_options.add_experimental_option( "prefs",{'profile.managed_default_content_settings.javascript': 2,
                                                     'profile.default_content_settings.cookies': 1})
        
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--profile-directory=Default')
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-plugins-discovery");
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("test-type=browser")
    driver = webdriver.Chrome(path, chrome_options=chrome_options)
    driver.delete_all_cookies()
    driver.set_window_size(800,800)
    driver.set_window_position(0,0)
    add_sneaky_cookies(driver, newSession = True)
    return driver



def fault_tolerant_parse_serialize(file_path, filename, urlList, print_every=100, batch_size = 2000):
    
    # Set up driver
    chrome_path = os.path.join(file_path, "browser_drivers", "chromedriver")
    driver = start_chrome(chrome_path)    
    
    # Basic Params
    batch = 0
    pages = []
    
    # Parsing
    for url in urlList:
        if i%print_every==0:
            print(i)
        if len(pages) >= batch_size:
            batch += 1
            page_df = pd.DataFrame(pages)
            page_df.to_csv(os.path.join(file_path,filename+"_%s.csv"%batch))
            pages = []
        
        ### SET THE URL
        result = parse_article_page(url, driver, parse_fn)
        if result:
            pages.append(result)