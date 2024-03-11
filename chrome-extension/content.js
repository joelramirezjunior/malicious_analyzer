chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === "fetchData") {
    // Execute the API call to get the prediction
    const htmlContent = document.documentElement.innerHTML;
    console.log("Fetching data for the extension...");
    fetch('http://localhost:5000/predict', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({html: htmlContent}),
    })
    .then(response => response.json())
    .then(data => {
      console.log('Prediction:', data.prediction);
      // Send the prediction back to the background script
      sendResponse({prediction: data.prediction});
    })
    .catch(error => {
      console.error('Error fetching prediction:', error);
      sendResponse({error: 'Failed to fetch prediction'});
    });

    return true; // Indicates that the response is sent asynchronously
  }
});
