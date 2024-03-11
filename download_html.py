import os
import pandas as pd
import re
import argparse
from bs4 import BeautifulSoup
from selenium import webdriver
from sklearn.feature_extraction.text import CountVectorizer
import time
import joblib


# Constants
FILTERED_URLS = "./labeled_correct.csv"
FILE_PATH = "./dataset"

# Initialize WebDriver
def init_browser(url):
    print("Initializing webdriver for URL:", url)
    driver = webdriver.Chrome()
    driver.get(url)
    return driver

# Extract features from HTML files
def extract_features():
    print("Extracting features...")
    dataset = []
    keywords = ["Scam", "scam", "McAfee", "bank", "password", "SSN", "Address", "Virus", "virus",
                "immediate", "credit card", "Name", "Download", "Free", "Hacked", "malware",
                "Phishing", "affiliate", "afid", "extension", "safe", "Form", "Survey"]
    vectorizer = CountVectorizer()
    corpus = []
    html_files = [filename for filename in os.listdir(FILE_PATH) if filename.endswith('.html')]

    # Prepare corpus for CountVectorizer
    for filename in html_files:
        with open(os.path.join(FILE_PATH, filename), 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')
            text = soup.get_text()
            corpus.append(text)

    # Fit and transform the corpus
    X = vectorizer.fit_transform(corpus)
    
    # joblib.dump(vectorizer, 'vectorizer.pkl')
    # return
    
    for i, filename in enumerate(html_files):
        features = {}
        y = 0 if "good" in filename else 1
        with open(os.path.join(FILE_PATH, filename), 'r', encoding='utf-8') as file:
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

            # Add BOW features
            bow_features = X.toarray()[i]
            for j, feature in enumerate(vectorizer.get_feature_names_out()):
                features[f"bow_{feature}"] = bow_features[j]

            dataset.append([features[key] for key in sorted(features)] + [y])

    columns = sorted(features.keys()) + ["y"]
    dataframe = pd.DataFrame(dataset, columns=columns)
    dataframe.to_csv("processed_dataset.csv", index=False)

# Download HTML files
def html_download(url, label, counter):
    driver = init_browser(url)
    print(f"Downloading HTML for: {url}")
    time.sleep(3)
    with open(f"{FILE_PATH}/{counter}_{label}.html", "w", encoding='utf-8') as f:
        f.write(driver.page_source)
    driver.quit()

# Schedule HTML downloads
def html_download_schedule(filtered_urls_filename):
    print("Downloading HTML files...")
    counter = 629  # Starting point for file naming
    with open(filtered_urls_filename, 'r') as fp:
        for line in fp:
            url, label = line.strip().split('\\')
            html_download(url, label.strip(), counter)
            counter += 1

# Parse arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description="Download HTMLs, extract features, or do both.")
    parser.add_argument("--download", help="Download HTML files", action="store_true")
    parser.add_argument("--extract", help="Extract features from HTML files", action="store_true")
    return parser.parse_args()

# Main execution
def main():
    args = parse_arguments()
    
    if args.download:
        html_download_schedule(FILTERED_URLS)
    
    if args.extract:
        extract_features()

if __name__ == "__main__":
    main()
