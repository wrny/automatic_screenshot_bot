import os
import re
import datetime
import time
import tld
import pyautogui

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

import argparse

# argument parsing
parser = argparse.ArgumentParser(description="Set additional parameters" + \
                                 "for automatic screenshot bot.")

headless_help = """Enter True / False to set program to run headlessly 
                    (i.e. without the screen showing). The program will run 
                    with less memory but also will reduce quality of the 
                    screenshots and some companies will block headless browsers
                    from loading page content, or block ads from appearing. If
                    you are using this program to view ads / ad placements, 
                    headless mode is not recommended."""
                    
time_help = """As an integer (1,2,3) enter the number of seconds needed before 
                scrolling downt the page and taking the next screenshot. 
                Default is 5, for slower internet connections, you may want to 
                increase it."""

screenshot_help = """As an integer (1,2,3) enter the number of screenshots you 
                    want to take / number of scrolls down the page you want the 
                    program to do. Default is 5."""

parser.add_argument('-H', '--headless', metavar='', type=bool, 
                    help=headless_help)

parser.add_argument('-t', '--time', metavar='', type=int, 
                    help=time_help)

parser.add_argument('-s', '--screenshots', metavar='', type=int, 
                    help=screenshot_help)

args = parser.parse_args()

def is_valid_url(url):
    # Regular Expression to determine valid URL.
    # Found here: https://stackoverflow.com/questions/7160737/python-how-to-validate-a-url-in-python-malformed-or-not/7160778
    regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    return re.match(regex, url)

def clean_url_file():
    """
    Removes blank paces, duplicate urls, and urls that are incompatable 
    with selenium.
    """
    # put lines in text file into a list
    with open('urls.txt') as file:
        url_list = [l.strip() for l in file.readlines()]

    # Remove blank spaces from list
    url_list = [u for u in url_list if u != ""]

    # removing duplicates while keeping original order
    unduplicated_url_list = []

    for url in url_list:
        if url not in unduplicated_url_list:
            unduplicated_url_list.append(url)

    # removing urls (via regex) incompatible with selenium
    cleaned_list = []
    failed_urls = []
    for url in unduplicated_url_list:
        if is_valid_url(url):
            cleaned_list.append(url)
        else:
            failed_urls.append(url)

    # urls not in proper format written to a text file
    if len(failed_urls) > 0:
        with open('failed_urls.txt', 'w') as file:
            for url in failed_urls:
                file.write(url+"\n")

    return cleaned_list

def launch_chrome(headless=False):
    options = Options()       
    
    screen_width, screen_height = pyautogui.size() 
    
    if headless:
        options.add_argument("--headless")
    
    options.add_argument(f"--window-size={screen_width}x{screen_height}")

    # Return driver object
    driver = webdriver.Chrome(executable_path='chromedriver.exe', 
                              options=options)
    return driver

def automatic_screenshot_bot(driver_object, unduplicated_url_list, 
                             time_to_wait=5, screenshots=5):
    """
    Visits URLs via Chrome Selenium webdriver, takes screenshots/saves 
    them in the "screenshots" folder. If the program breaks, it will
    write the urls to a file called "failed_urls.txt" where users can
    take this list and try again.
    """
    if time_to_wait is None:
        time_to_wait = 5
        
    if screenshots is None:
        screenshots = 5 
        
    driver = driver_object
    
    if len(unduplicated_url_list) > 0:
        driver.maximize_window()
        for url in unduplicated_url_list:
            print(f"Taking screenshots of {url}...")
            with open('completed_urls.txt') as file:
                completed_url_list = [l.strip() for l in file.readlines()]

            if url not in completed_url_list:
                screenshot_count = 1
                try:
                    driver.get(url)
                    for _ in range(screenshots):        
                        now = datetime.datetime.now()
                        date = now.strftime('%Y-%m-%d-%H-%M-%S')
    
                        # Files can't be saved with the \ / : * ? " < > | symbols. 
                        # So we save the file with the top-level domain
                        top_level_domain = tld.get_fld(url)
                        
                        # Creates our filename format
                        filename = ("_").join([top_level_domain, date, 
                                   str(screenshot_count), ".png"])
    
                        full_path = os.path.join('screenshots', filename)
                        print(f"Saving screenshot: {filename}...")
                        page_body = driver.find_element_by_css_selector('body')
                        driver.save_screenshot(full_path)
                        time.sleep(time_to_wait)
                        page_body.send_keys(Keys.PAGE_DOWN)
                        screenshot_count += 1
    
                    with open('completed_urls.txt', 'a') as file:
                        file.write(url+"\n")

                # Catch all exception in case something goes wrong
                # then the program won't break.
                
                except Exception as e:
                    print(f"Exception is: {e}")
                    if os.path.exists('failed_urls.txt'):
                        with open('failed_urls.txt', 'a') as file:
                            file.write(url+"\n")
    
                    else:
                        with open('failed_urls.txt', 'w') as file:
                            file.write(url+"\n")
    
                    continue

            else:
                print(f"{url} already done. Continuing...")
                continue

    driver.close()
    
if __name__ == '__main__':
    # Check to see if urls.txt exists        
    if not os.path.exists('urls.txt'):
        print("please have a list of page urls " + \
              "(that start with http:// + https:// ), seperated by line. " + \
              "Closing program.")
        
    else:
        if not os.path.exists('completed_urls.txt'):
            with open('completed_urls.txt', 'w') as file:
                file.write("")
            
        unduplicated_url_list = clean_url_file()
        driver = launch_chrome(args.headless)
        automatic_screenshot_bot(driver, unduplicated_url_list, 
                                 time_to_wait=args.time, 
                                 screenshots=args.screenshots)
        
        print("All done gathering screenshots!")