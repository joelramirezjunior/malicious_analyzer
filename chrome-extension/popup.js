
document.addEventListener('DOMContentLoaded', () => {
    chrome.runtime.sendMessage({ action: "getPrediction" }, function(response) {
        document.getElementById('prediction').textContent = response.prediction || "No prediction available";
    });
});
