from bs4 import BeautifulSoup
import re
import os
import pandas as pd

PRINT_PRETTY = 0

file_path = "./dataset"

# Count mentions of various keywords
# we sorta choose them willy nilly 

keywords = ["Scam", "scam", "McAfee", "bank", "password", "SSN", "Address", "Virus", "virus", \
                "immediate", "credit card", "Credit Card", "Credit card", "Name", "Download", "Free", \
                    "free", "Hacked", "hack", "hacked", "malware", "Malware", "phishing", "Phishing", "affiliate", \
                        "afid", "extension", "Extension", "safe", "Form", "Survey"]


dataset = []
for filename in os.listdir(file_path):
    features = {}
    if PRINT_PRETTY:
        print("Looking at: ", filename)
    y = 0 #good
    if "bad" in filename: y = 1

    # this here, returns a SOUP OBJECT  A
    with open("./dataset/"+filename) as file:
        
        soup = BeautifulSoup(file, 'html.parser')

        for keyword in keywords:
            # Using \b for word boundaries
            file.seek(0)
            features[keyword] = len(re.findall(r'\b' + re.escape(keyword) + r'\b', file.read(), re.IGNORECASE))

        # Count divs and scripts within divs
        #we use the soup to find all of the elements that we are interested in.
        divs = soup.find_all('div')
        features["number_of_divs"] = len(divs)
        features["number_of_scripts_in_divs"] = sum(len(div.find_all('script', recursive=False)) for div in divs)
        features["number_of_scripts"] = len(soup.find_all('script', recursive=True))
        features["number_of_links"] = len(soup.find_all("link"))
        # Count forms
        features["number_of_forms"] = len(soup.find_all('form'))
        features_list = list(features.values())
        features_list.append(y)
        dataset.append(features_list) 
        
        if PRINT_PRETTY:
            print(features)
            print("\n")


dataframe = pd.DataFrame(dataset, columns = list(features.keys())+ ["y"])
dataframe.to_csv("processed_dataset.csv")