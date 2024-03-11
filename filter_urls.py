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
FILE_NAME = "./metadata/march-9-additions.csv"
MAX_THREADS = 10

lock = threading.Lock()

# Check if a URL is reachable
def check_protocol_reachability(url, protocol):
    print(f"Checking reachability for {protocol}://{url}")
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
    print("Starting to find reachable links...")
    list_of_links = [] 
    #opens a new file called "labeled_correct"
    with open("labeled_correct.csv", 'a') as good_csv:
        print("Opened the file where we will write good links")
        #we open the file with the "url", "label"
        #before we have even filtered for the ones that are even available.
        with open(name, 'r') as url_csv: 
            lines = url_csv.readlines()
            threads = []
            print(len(lines))
            for line in lines:
                print(line)
                result = line.split(',')
                if len(result) != 2:
                    continue
                url = result[0]
                if url == 'URL': 
                    continue
                label = result[1].strip()
                print(f"Processing URL: {url} with label: {label}")
                thread = threading.Thread(target=reachable, args=(url, good_csv, label, list_of_links))
                threads.append(thread)
                thread.start()
                if len(threads) == MAX_THREADS:
                    print("Maximum threads reached, waiting for threads to complete...")
                    for thread in threads:
                        thread.join()
                    print("All threads completed, continuing...")
                    threads = []
            for thread in threads:
                thread.join()
    print("Completed finding reachable links.")
    return list_of_links

# Function to determine if URL is reachable
def reachable(url, good_csv, label, list_of_links):
    protocols = ["https", "http"]
    for protocol in protocols:
        if check_protocol_reachability(url, protocol):
            with lock: 
                print(f"Reachable URL found: {protocol}://{url} | {label}")
                good_csv.write(f"{protocol}://{url},{label}\n")
                list_of_links.append([url, label])
                return
        
# Main execution
def main():
    print("Starting main execution...")
    find_reachable_links(FILE_NAME)
    print("Main execution completed.")

if __name__ == "__main__":
    main()
