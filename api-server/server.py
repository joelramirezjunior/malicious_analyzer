from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes




#We will use the html sent over, preprocess it to the correct format
#We will load in the model
#ask the model what it thinks
#then we send that response back to the extension


@app.route('/predict', methods=['POST'])
def predict():
    data = request.json['html'] #this will grab the HTML sent over by the chrome content.js
    print("Recieved the information from the extension.")
    print(data)
    if data is None:
        print("Data was empty.")

    prediction = "Good"
    #what the server returns as a response to the request made by the content.js
    return jsonify({'prediction': prediction})


if __name__ == '__main__':
    app.run(debug=True, port=5000)

