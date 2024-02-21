import os
import pandas as pd
import re
import threading
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Constants
filterd_urls = "./labeled_correct.csv"
MAX_THREADS = 10
PRINT_PRETTY = 0
file_path = "./dataset"

lock = threading.Lock()

# Initialize WebDriver
def init_browser(URL):
    print("Initializing webdriver")
    print(URL)
    driver = webdriver.Chrome()
    driver.get(URL)
    return driver


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
    dataframe.to_csv("new_processed_dataset.csv")

def html_download(url, label, counter):

    driver = init_browser(url)
    print(f"Checking this URL: {url}")
    time.sleep(3)
    with open(f"{file_path}/{counter}_{label}.html", "w", encoding='utf-8') as f:
        f.write(driver.page_source)
    driver.quit()

# Download HTML documents from reachable URLs
def html_downld_schd(filted_urls_filena):
    counter = 156
    with open(filted_urls_filena) as fp: 

        # threads = []
        for line in fp:
            url, label = line.split('\\')
            html_download(url, label, counter)
            counter += 1
            # thread = threading.Thread(target = html_download, args=(url, label, counter))
            # threads.append(thread)
            # thread.start()
            # counter+=
            # if len(threads) == MAX_THREADS: 
            #     for thread in threads:
            #         thread.join()
            
# Main execution
def main():
    
    # html_downld_schd(filterd_urls)
    extract_features()

if __name__ == "__main__":
    main()
