### Extension Overview

The Chrome extension is structured around three principal components: the background worker, the extension's HTML and JavaScript (JS), and the content JS that is injected into every webpage where the extension is active.

The background worker operates continuously, monitoring for communications from the popup—the user interface element visible on the toolbar. When the popup issues a command, the background worker relays this instruction to the content.js script running within the current webpage. This script is pivotal for initiating the data retrieval process, where it requests predictions from a server. At present, the server is hosted locally (localhost), but plans are in place to transition it to an online server, making it accessible over the internet.

Content.js plays a vital role as it is dynamically injected into each webpage the user navigates to. Its primary function is to await instructions from the background worker. Absent any directives, content.js remains idle, ensuring it does not interfere with the webpage unless required.

Upon receiving a command from the background worker, content.js springs into action, aggregating the webpage's entire HTML content to dispatch to the server. Following the submission, it awaits the server's response. Once the prediction data is received, content.js conveys this information back to the background worker. Subsequently, the background worker forwards this data to popup.js, which resides within the extension's user interface on the toolbar.

The entire process is initiated by popup.js when a user interacts with the extension. It sends a request to the background worker to engage with content.js and, upon receiving the processed information, updates the extension's popup display to present the results to the user. This seamless interaction between the components ensures a fluid and responsive user experience, providing valuable insights directly derived from the webpage content.