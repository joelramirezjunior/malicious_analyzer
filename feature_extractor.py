from bs4 import BeautifulSoup
import re

# . -> this directory where the code lives
file_path = "./example/html_scam.html"

#how can we find the toasts? 
scam_mentions = 0

html_page = open(file_path, "r")
entire_page = "".join([x for x in html_page])

soup = BeautifulSoup(entire_page, 'html.parser')
scam_mentions = len(re.findall("scam", entire_page))
mcaffe_mentions = len(re.findall("McAfee", entire_page))
bank_mentions = len(re.findall("bank", entire_page))
password_mentions = len(re.findall("password", entire_page))
social_security_mentions = len(re.findall("SSN", entire_page))
address_mentions = len(re.findall("Address", entire_page))
virus_mentions = len(re.findall("Virus", entire_page))
immediate_mentions = len(re.findall("immediate", entire_page))


divs = soup.find_all('div')
number_of_divs = 0 
number_of_scripts_in_divs = 0


for div in divs: 
    number_of_divs += 1
    scripts = div.find_all('script', recursive=False)
    for script in scripts:
        number_of_scripts_in_divs += 1


number_of_forms = len(soup.find_all('form'))


print("This the number of divs: ", number_of_divs)
print("This the number of scripts in divs: ", number_of_scripts_in_divs)
print("This the number of forms: ", number_of_forms)
print("This the number of scam mentioned: ", scam_mentions)
print("This the number of mcafee mentioned: ", mcaffe_mentions)
print(scam_mentions, mcaffe_mentions, bank_mentions, password_mentions, social_security_mentions, address_mentions, virus_mentions, immediate_mentions)
