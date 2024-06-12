function refreshQueue() {
    fetch('/queue')
    .then(response => response.json())
    .then(data => {
        document.getElementById('queue').innerHTML = data.queue.map(song => '<li>' + song + '</li>').join('');
        document.getElementById('current_song').innerHTML = 'Current song: ' + data.current_song.title;
        document.getElementById('cover').src = data.current_song.cover;
    });
}
setInterval(refreshQueue, 5000);
window.onload = refreshQueue;

function sendCommand(command) {
    fetch('/' + command, {method: 'POST'})
    .then(() => refreshQueue());
}

/////