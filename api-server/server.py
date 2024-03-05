from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import pandas as pd
import re
from bs4 import BeautifulSoup
from tensorflow.keras.models import load_model

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

model = load_model('./best_model.h5')

keywords = ["Scam", "scam", "McAfee", "bank", "password", "SSN", "Address", "Virus", "virus", \
                "immediate", "credit card", "Credit Card", "Credit card", "Name", "Download", "Free", \
                "free", "Hacked", "hack", "hacked", "malware", "Malware", "phishing", "Phishing", "affiliate", \
                "afid", "extension", "Extension", "safe", "Form", "Survey"]

def extract_features(html_content):

    print(type(html_content))
    soup = BeautifulSoup(html_content, 'html.parser')  

    features = {}
    for keyword in keywords:
        features[keyword] = len(re.findall(r'\b' + re.escape(keyword) + r'\b', html_content, re.IGNORECASE))
    
    divs = soup.find_all('div')
    features["number_of_divs"] = len(divs)
    features["number_of_scripts_in_divs"] = sum(len(div.find_all('script', recursive=False)) for div in divs)
    features["number_of_scripts"] = len(soup.find_all('script', recursive=True))
    features["number_of_links"] = len(soup.find_all("link"))
    features["number_of_forms"] = len(soup.find_all('form'))

    dataframe = pd.DataFrame([features], columns=list(features.keys()))
    print(list(features.keys()))        
    print(dataframe)
    return dataframe


'''
Disclaimer: These explanations are for a student of mine.

app.route -> will tell the app this is a "route" or path' that it will be listening on for a request. 
The only thing that should be asking for a request is the extension itself as this point. It might not make sense that the 
extension has the ability to send a request (as if it were on the internet). But, something that you should know is that your computer is 
"local host". This means that any browser running on your computer can send and recieves requests from the 'localhost'/your machine itself. 

This program runs on your machine, and will respond to requests from the extension on the chrome broswer.
'''

#This tells you what will function will be called when local host (on port 5000) recieves a request with path predict and method "post"
#If you'd like, review and see what Post, Get, Delete, Etc mean in the context of HTTPS.
@app.route('/predict', methods=['POST'])
def predict():
    #request, although not declared here, is a global object that allows you to see the contents of the request 
    #sent from the extension.

    data = request.json['html'] #this will grab the HTML sent over by the chrome content.js
    print("Recieved the information from the extension.")

    if data is None:
        print("Data was empty.")
        return jsonify({'error': "Request body was empty. No HTML sent."})

                   #this is where were preprocess the HTML to format it to be inserted into the model. 
    features_df = extract_features(data)
    prediction = model.predict(features_df)[0]  #We will change this to be logistic regression. For the sake of brevity, I didn't refactor the code. 
    predicted_class = 'Good' if prediction < 0.5 else 'Bad'  # Assuming a binary classification: 0 is 'Good', 1 is 'Bad'
    return jsonify({'prediction': predicted_class}) #This is what is sent back to the chrome extension. 


if __name__ == '__main__':
    app.run(debug=True, port=5000)

