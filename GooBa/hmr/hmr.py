javascript = """
// Function to reload the page
function reloadPage() {
    window.location.reload();
}

// Function to watch for changes
function watchForChanges() {
var xhr = new XMLHttpRequest();
xhr.onreadystatechange = function() {
    if (xhr.readyState === XMLHttpRequest.DONE) {
        if (xhr.status === 200) {
            // Check if the response has changed
            if (xhr.responseText !== localStorage.getItem('lastResponse')) {
                localStorage.setItem('lastResponse', xhr.responseText);
                reloadPage();
            }
        }
    }
}
xhr.open('GET', window.location.href + '?reload=' + new Date().getTime(), true);
xhr.send();
}

// Call the watchForChanges function periodically
setInterval(watchForChanges, 1000);

        """