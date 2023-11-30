from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.request
import re


def init_browser(URL):
    print("Initializing webdriver")
    driver = webdriver.Chrome()
    driver.get(URL)
    return driver


file_path = "./dataset/labeled_correct.csv"

# Count mentions of various keywords
# we sorta choose them willy nilly 
keywords = ["Scam", "scam", "McAfee", "bank", "password", "SSN", "Address", "Virus", "virus", "immediate", "credit card", "Credit Card", "Credit card", "Name", "Download", "Free", "free", "Hacked", "hack", "hacked", "malware", "Malware", "phishing", "Phishing", "affiliate", "afid", "extension", "Extension", "safe", "Form", "Survey"]
mentions = {}

#this is going to just open the file, but we need to loop per line in the file

counter = 0

with open(file_path, "r") as file:

    for line in file: 
                    # "www.google.com, good"
        _url, _label = line.split("\\")
            
        # if _label is None or _label is list:
        #     continue
        print(_url)
        driver = init_browser(f"http://{_url}")
        time.sleep(2)
        with open(f"./dataset/{counter}_{_label}.html", "w", encoding='utf-8') as f:
             f.write(driver.page_source)
             counter+=1
        
        # entire_page = html_page.read()
        # soup = BeautifulSoup(entire_page, 'html.parser')

        # for keyword in keywords:
        #     # Using \b for word boundaries
        #     mentions[keyword] = len(re.findall(r'\b' + re.escape(keyword) + r'\b', entire_page, re.IGNORECASE))

# print(mentions)

# # Count divs and scripts within divs
# divs = soup.find_all('div')
# number_of_divs = len(divs)
# number_of_scripts_in_divs = sum(len(div.find_all('script', recursive=False)) for div in divs)
# number_of_scripts = len(soup.find_all('script', recursive=True))
# number_of_links = len(soup.find_all("link"))
# # Count forms
# number_of_forms = len(soup.find_all('form'))

# # Print the results
# print(f"This the number of divs: {number_of_divs}")
# print(f"This the number of scripts in divs: {number_of_scripts_in_divs}")
# print(f"This the number of scripts: {number_of_scripts}")
# print(f"This the number of forms: {number_of_forms}")
# print(f"This is the number of links: {number_of_links}")

# for keyword, count in mentions.items():
#     print(f"This the number of {keyword} mentioned: {count}")
