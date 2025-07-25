// main.js
console.log("Frontdesk AI Supervisor UI loaded");

function checkUnresolved() {
    fetch('/api/stats')
        .then(response => response.json())
        .then(data => {
            if (data.unresolved > 0) {
                alert(`Notification: ${data.unresolved} query(s) unresolved after 1 minute at ${new Date().toLocaleString('en-US', { timeZone: 'Asia/Kolkata', hour12: true })}`);
            }
        })
        .catch(error => console.error('Error checking unresolved requests:', error));
}

// Poll every 10 seconds
setInterval(checkUnresolved, 10000);