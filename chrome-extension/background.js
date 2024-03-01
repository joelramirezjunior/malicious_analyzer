// Variable to store the prediction data

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === "popupOpened") {
      console.log("Popup was opened - handle in background.js");
      // You can perform other background tasks here
      sendResponse({ result: "Message received in background" });
  }
});

let currentPrediction = '';  // Variable to store the current prediction

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  
  // Listening for the prediction from the content script
  if (message.action === "showPrediction") {
    currentPrediction = message.prediction;
    console.log("Stored prediction: ", currentPrediction);
  }
});
