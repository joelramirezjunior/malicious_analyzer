# Web Content Analysis Extension: Readme

## Overview
This document outlines the setup and functionality of a Flask-based server designed to interact with a Chrome extension for the purpose of web content analysis. The server employs a machine learning model to evaluate the safety or potential risks associated with the content of webpages.

## Prerequisites
- Python
- Flask
- Flask-CORS
- Pandas
- BeautifulSoup
- TensorFlow

Ensure you have the above libraries and frameworks installed in your Python environment to seamlessly run the server.

## Server Setup
The Flask application is instantiated with CORS (Cross-Origin Resource Sharing) enabled, allowing it to accept requests from the Chrome extension irrespective of the origin. This is crucial for local testing and future deployment scenarios where the extension and server might not share the same origin.

A pre-trained TensorFlow model (`best_model.h5`) is loaded at server initialization. This model is integral to the analysis process, providing the classification of webpage content based on learned patterns.

## Functionality
### Feature Extraction
The `extract_features` function parses the HTML content received from the webpage via the Chrome extension. It utilizes BeautifulSoup to navigate the HTML structure and extract relevant features such as the presence of specific keywords, the number of `div` elements, script tags, links, and forms. These features are then formatted into a Pandas DataFrame, serving as the input for the prediction model.

### Prediction Endpoint
The server defines a `/predict` endpoint, accepting POST requests containing the webpage's HTML content. Upon receiving a request, the server:
1. Extracts the features from the HTML.
2. Feeds the feature data into the machine learning model.
3. Interprets the model's output to classify the webpage as 'Good' or 'Bad'.

The classification result is then returned to the Chrome extension in JSON format.

### Running the Server
To start the server, execute the script. By default, the server will run in debug mode on port 5000, listening for incoming prediction requests from the extension.

```
if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

## Disclaimer
This readme provides an understanding of the server's role within the context of the Chrome extension for web content analysis. The server is designed to run locally (localhost), facilitating communication with the Chrome browser extension during development and testing phases. Future updates may include deploying the server to handle requests over the internet.