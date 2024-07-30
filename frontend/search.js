function search() {
    var searchTerm = document.getElementById('search_bar').value;
    return fetch('fetchingdata.php?searchTerm=' +  encodeURIComponent(searchTerm), {
        method: 'GET',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
    })
    .then(response => response.text())  // convert to plain text
    .then(text => {
        window.titles = JSON.parse(text);  // parse text into array and assign to window.titles
        console.log(window.titles);  // Log the response data to the console
    })
    .catch(error => console.error('Error:', error));
}