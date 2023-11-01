from bs4 import BeautifulSoup
import re

file_path = "./example/html_scam.html"

# Count mentions of various keywords
keywords = ['scam', 'McAfee', 'bank', 'password', 'SSN', 'Address', 'Virus', 'immediate']
mentions = {}

with open(file_path, "r") as html_page:
    entire_page = html_page.read()
    soup = BeautifulSoup(entire_page, 'html.parser')

    for keyword in keywords:
        mentions[keyword] = len(re.findall(keyword, entire_page))

# Count divs and scripts within divs
divs = soup.find_all('div')
number_of_divs = len(divs)
number_of_scripts_in_divs = sum(len(div.find_all('script', recursive=False)) for div in divs)

# Count forms
number_of_forms = len(soup.find_all('form'))

# Print the results
print(f"This the number of divs: {number_of_divs}")
print(f"This the number of scripts in divs: {number_of_scripts_in_divs}")
print(f"This the number of forms: {number_of_forms}")

for keyword, count in mentions.items():
    print(f"This the number of {keyword} mentioned: {count}")
