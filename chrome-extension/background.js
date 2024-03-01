// In background.js
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === "requestClass") {
    // Relay this request to the content script
    chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
      chrome.tabs.sendMessage(tabs[0].id, {action: "fetchData"}, (response) => {
        // Relay content script's response back to popup.js
        console.log("Prediction recieved from api:", response.prediction);
        sendResponse({action: "predictionResponse", reply: response.prediction});
      });
    });
    return true; // Indicates that the response is asynchronous
  }
});
