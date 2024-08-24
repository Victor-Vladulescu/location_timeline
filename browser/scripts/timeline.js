function listener(details) {
    // Check if the request is from the extension
    if (details.initiator && details.initiator.startsWith("chrome-extension://")) {
      return; // Ignore requests initiated by the extension itself
    }

    // now send the response body to your own app
    fetch(details.url)
      .then(response => response.text())
      .then(response => {
        fetch("http://localhost:8000/timeline_api/update_gm", {
            method: "POST",
            body: JSON.stringify({
                data: response
            }),
            headers: {
                "Content-type": "application/json; charset=UTF-8"
            }
        });

        // and fulfill the original request 
        return response;
      })
      .catch(error => {
        console.error("Error fetching response body:", error);

        return {};
      });
}

// listen for requests matching this URL
chrome.webRequest.onBeforeRequest.addListener(
    listener,
    {urls: ["https://www.google.com/maps/rpc/locationsharing/*"]},
    ["blocking"]
);

// reload the page after 10 minutes
setInterval(() => { 
  chrome.tabs.query({active: true, currentWindow: true}, function (arrayOfTabs) {
    var code = 'window.location.reload();';
    chrome.tabs.executeScript(arrayOfTabs[0].id, {code: code});
  });
}, 600000);
