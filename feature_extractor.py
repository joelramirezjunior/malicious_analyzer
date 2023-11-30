from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.request
import re
import os


file_path = "./dataset"

# Count mentions of various keywords
# we sorta choose them willy nilly 
keywords = ["Scam", "scam", "McAfee", "bank", "password", "SSN", "Address", "Virus", "virus", "immediate", "credit card", "Credit Card", "Credit card", "Name", "Download", "Free", "free", "Hacked", "hack", "hacked", "malware", "Malware", "phishing", "Phishing", "affiliate", "afid", "extension", "Extension", "safe", "Form", "Survey"]
mentions = {}


for filename in os.listdir(file_path):
    if "chase" in filename:
        print("Looking at: ", filename)

        # this here, returns a SOUP OBJECT  A
        with open("./dataset/"+filename) as file:
            
            soup = BeautifulSoup(file, 'html.parser')

            for keyword in keywords:
                # Using \b for word boundaries
                file.seek(0)
                mentions[keyword] = len(re.findall(r'\b' + re.escape(keyword) + r'\b', file.read(), re.IGNORECASE))

            print(mentions)
    
            # Count divs and scripts within divs
            #we use the soup to find all of the elements that we are interested in.
            divs = soup.find_all('div')
            number_of_divs = len(divs)
            number_of_scripts_in_divs = sum(len(div.find_all('script', recursive=False)) for div in divs)
            number_of_scripts = len(soup.find_all('script', recursive=True))
            number_of_links = len(soup.find_all("link"))
            # Count forms
            number_of_forms = len(soup.find_all('form'))

            # Print the results
            print(f"This the number of divs: {number_of_divs}")
            print(f"This the number of scripts in divs: {number_of_scripts_in_divs}")
            print(f"This the number of scripts: {number_of_scripts}")
            print(f"This the number of forms: {number_of_forms}")
            print(f"This is the number of links: {number_of_links}")
