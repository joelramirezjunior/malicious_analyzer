from bs4 import BeautifulSoup
import re

file_path = "./example/amazon.html"

# Count mentions of various keywords
# we sorta choose them willy nilly 
keywords = ["Scam", "scam", "McAfee", "bank", "password", "SSN", "Address", "Virus", "virus", "immediate", "credit card", "Credit Card", "Credit card", "Name", "Download", "Free", "free", "Hacked", "hack", "hacked", "malware", "Malware", "phishing", "Phishing", "affiliate", "afid", "extension", "Extension", "safe", "Form", "Survey"]
mentions = {}

with open(file_path, "r") as html_page:
    entire_page = html_page.read()
    soup = BeautifulSoup(entire_page, 'html.parser')

    for keyword in keywords:
        # Using \b for word boundaries
        mentions[keyword] = len(re.findall(r'\b' + re.escape(keyword) + r'\b', entire_page, re.IGNORECASE))

print(mentions)

# Count divs and scripts within divs
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

for keyword, count in mentions.items():
    print(f"This the number of {keyword} mentioned: {count}")
