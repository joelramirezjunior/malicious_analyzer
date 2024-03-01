// This code will be executed in the context of the webpage

const htmlContent = document.documentElement.innerHTML;

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
  chrome.runtime.sendMessage({action: "showPrediction", prediction: data.prediction});
});

