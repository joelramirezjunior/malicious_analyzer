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
FILE_NAME = "metadata/dataset.csv"
MAX_THREADS = 10
PRINT_PRETTY = 0
file_path = "./dataset"

# Initialize WebDriver
def init_browser(URL):
    print("Initializing webdriver")
    driver = webdriver.Chrome()
    driver.get(URL)
    return driver

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
    with open("labeled_correct.csv", 'a') as good_csv:
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
                thread = threading.Thread(target=reachable, args=(url, good_csv, label))
                threads.append(thread)
                thread.start()
                if len(threads) == MAX_THREADS:
                    for thread in threads:
                        thread.join()
                    threads = []
            for thread in threads:
                thread.join()

# Function to determine if URL is reachable
def reachable(url, good_csv, label):
    protocols = ["https", "http"]
    for protocol in protocols:
        if check_protocol_reachability(url, protocol):
            with lock: 
                good_csv.write(f"{protocol}://{url} \ {label}")

# Extract features from HTML files
def extract_features():
    dataset = []
    keywords = ["Scam", "scam", "McAfee", "bank", "password", "SSN", "Address", "Virus", "virus", \
                "immediate", "credit card", "Credit Card", "Credit card", "Name", "Download", "Free", \
                "free", "Hacked", "hack", "hacked", "malware", "Malware", "phishing", "Phishing", "affiliate", \
                "afid", "extension", "Extension", "safe", "Form", "Survey"]
    for filename in os.listdir(file_path):
        features = {}
        y = 0 if "good" in filename else 1
        with open(os.path.join(file_path, filename)) as file:
            soup = BeautifulSoup(file, 'html.parser')
            for keyword in keywords:
                file.seek(0)
                features[keyword] = len(re.findall(r'\b' + re.escape(keyword) + r'\b', file.read(), re.IGNORECASE))
            divs = soup.find_all('div')
            features["number_of_divs"] = len(divs)
            features["number_of_scripts_in_divs"] = sum(len(div.find_all('script', recursive=False)) for div in divs)
            features["number_of_scripts"] = len(soup.find_all('script', recursive=True))
            features["number_of_links"] = len(soup.find_all("link"))
            features["number_of_forms"] = len(soup.find_all('form'))
            features_list = list(features.values())
            features_list.append(y)
            dataset.append(features_list)
    dataframe = pd.DataFrame(dataset, columns=list(features.keys()) + ["y"])
    dataframe.to_csv("processed_dataset.csv")

# Main execution
def main():
    find_reachable_links(FILE_NAME)
    extract_features()

if __name__ == "__main__":
    main()
