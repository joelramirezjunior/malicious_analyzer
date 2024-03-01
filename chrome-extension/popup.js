// In popup.js
chrome.runtime.sendMessage({action: "requestClass"}, (response) => {
  console.log(response)
  if (response.action === "predictionResponse") {
    const prediction = response.reply;
    document.getElementById('prediction').textContent = prediction || "No prediction available...";
  }

});
