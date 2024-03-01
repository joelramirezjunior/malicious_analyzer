"# Improving the Analysis of Malicious Websites using Machine Learning

## Objectives

This browser extension leverages a machine learning model to enhance web browsing safety by analyzing and identifying potentially malicious websites in real-time. Here's what it aims to achieve:

- **Identify Malicious Websites**: Automatically assesses each visited website to determine if it poses any threat, such as phishing attempts, malware presence, or unwanted adware.

- **Inform the User**: Provides detailed feedback on the nature of the threat, including the type of malicious activity detected and possible reasons why the site was flagged.

- **Transparency**: Clarifies the reasoning behind the model's decision by highlighting specific factors or indicators that contributed to the website's evaluation.

- **Intelligent Redirection**: Offers the option to navigate away from potential threats by redirecting users to their intended or safer alternative websites.

- **Enhanced Privacy**: Ensures user privacy by blocking tracking requests from suspicious sites, maintaining user anonymity and data protection.

## What Makes This Different?

### Conventional Solutions
1. Depend mainly on static databases for URL threat assessment.
2. Provide limited or no explanation for the security assessment.
3. Lack features for redirecting users to safe alternatives.

### Our Approach
1. **Comprehensive Identification**: Utilizes a dynamic machine learning model to analyze and identify a broad spectrum of online threats in real time.
2. **Descriptive Analysis**: Offers a detailed breakdown of why a website is considered unsafe, providing users with context and understanding.
3. **User-Centric Information**: Delivers insights about potential tracking and the website's background, enhancing user awareness and decision-making.
4. **Intelligent Redirection**: Proactively assists users by suggesting safer navigational options.
5. **Enhanced Privacy Features**: Actively blocks tracking mechanisms on suspicious websites, reinforcing user privacy.

Our extension is designed to be a proactive web safety tool that not only detects threats but also educates users, offering a more informed and secure browsing experience.

## Extension Architecture and Message Passing Model

### Architecture Overview

The extension consists of several components working in harmony to analyze and respond to web content:

- **Content Script (`content.js`)**: Directly interacts with the web page's content, extracting HTML and other relevant information for analysis.

- **Background Script (`background.js`)**: Serves as the central hub for message coordination between the content script, popup, and potentially external servers for model prediction.

- **Popup Script (`popup.js`)**: Provides a user interface for real-time feedback and allows users to interact with the extension's features.

### Message Passing Model

1. **From Popup to Background**: When the user opens the extension popup, `popup.js` sends a message to `background.js` requesting the latest analysis or prediction for the current tab.

2. **From Background to Content**: `background.js` forwards this request to `content.js`, prompting it to fetch and send the current webpage content or trigger a new analysis.

3. **From Content to API and Back**: `content.js` performs an API call to a machine learning model server with the extracted webpage content, receives the prediction, and sends this information back to `background.js`.

4. **From Background to Popup**: Finally, `background.js` relays the received prediction data to `popup.js`, which then updates the popup UI to display the analysis results to the user.

## Notes on Feature Extraction

During the initial phase, feature extraction relies on identifying key terms and elements within the webpage content. This process is currently guided by predefined criteria but is expected to evolve. Future iterations will aim to refine these extraction methods based on model feedback and learning, optimizing the relevance and accuracy of the features used for analysis (see `feature_extractor.py` for the current methodology)."