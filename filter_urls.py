import csv
import os
import pandas as pd
import re
import requests
import threading
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Constants
FILE_NAME = "metadata/new_websites_to_add.csv"
MAX_THREADS = 10
PRINT_PRETTY = 0
file_path = "./new_dataset"


lock = threading.Lock()

# Check if a URL is reachable
def check_protocol_reachability(url, protocol):
    try:
        response = requests.get(f"{protocol}://{url}", timeout=3, verify=False)
        return True
    except requests.exceptions.ConnectionError:
        pass
    except requests.exceptions.RequestException as e:
        pass
    return False

# Find reachable links
def find_reachable_links(name):
    list_of_links = [] 
    #opens a new file called "labeled_correct"
    with open("labeled_correct.csv", 'a') as good_csv:

        #we open the file with the "url", "label"
        #before we have even filtered for the ones that are even available.
        with open(name, 'r') as url_csv: 
            lines = url_csv.readlines()
            threads = []
            for line in lines:
                result = line.split(',')
                if len(result) != 2:
                    continue
                url = result[0]
                if url == 'URL': 
                    continue
                label = result[1]
                thread = threading.Thread(target=reachable, args=(url, good_csv, label, list_of_links))
                threads.append(thread)
                thread.start()
                if len(threads) == MAX_THREADS:
                    for thread in threads:
                        thread.join()
                    threads = []
            for thread in threads:
                thread.join()
    return list_of_links

# Function to determine if URL is reachable
def reachable(url, good_csv, label, list_of_links):
    protocols = ["https", "http"]
    for protocol in protocols:
        if check_protocol_reachability(url, protocol):
            with lock: 
                good_csv.write(f"{protocol}://{url} \ {label}")
                list_of_links.append([url, label])
                return
        
# Main execution
def main():
    find_reachable_links(FILE_NAME)

if __name__ == "__main__":
    main()
