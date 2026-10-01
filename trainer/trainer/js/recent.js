let recentButton = document.getElementById("recent-only");
recentButton.addEventListener('change', (e) => {
    let url = `/toggle_recent/`;
    fetch(url, {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json',
        "X-CSRFToken": csrf_token
    },
    })
        .then(response => response.json())
        .catch(error => console.error(error));
});
