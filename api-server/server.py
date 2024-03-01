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


@app.route('/predict', methods=['POST'])
def predict():
    data = request.json['html'] #this will grab the HTML sent over by the chrome content.js
    print("Recieved the information from the extension.")
    # print(data)
    if data is None:
        print("Data was empty.")

    prediction = "Good"
    features_df = extract_features(data)
    prediction = model.predict(features_df)[0]
    predicted_class = 'Good' if prediction < 0.5 else 'Bad'  # Assuming a binary classification: 0 is 'Good', 1 is 'Bad'
    return jsonify({'prediction': predicted_class})

    #what the server returns as a response to the request made by the content.js



if __name__ == '__main__':
    app.run(debug=True, port=5000)

