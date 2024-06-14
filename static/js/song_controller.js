//ADD TO QUEUE

const songOverview = document.getElementById('songs');

if (songOverview) {
    // Event Listener für die Buttons
    document.querySelectorAll('.song-button').forEach(button => {
        button.addEventListener('click', (event) => {
            const songTitle = event.target.getAttribute('data-title');
            
            console.log(songTitle);
            fetch('/enqueue', {
                method: 'POST',
                headers: {
                    'Content-Type': 'text/plain' // Setze den Content-Type auf text/plain
                },
                body: songTitle // Sende den Songtitel im Klartext
            })
            .then(response => response.json())
            .then(data => {
                console.log('Success:', data);
            })
            .catch((error) => {
                console.error('Error:', error);
            });
        });
    });
} else {
    console.error('Element with id "songs" not found.');
}

//SKIP QUEUE

function sendCommand(command) {
    const queue = document.getElementById('queue');
    const songs = queue.getElementsByTagName('li');
    if (command === 'resume') {
        fetch('/resume', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            // Optionale Aktion nach erfolgreichem POST-Request
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    } else if (command === 'pause') {
        fetch('/pause', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            // Optionale Aktion nach erfolgreichem POST-Request
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    } else if (songs.length > 0 && command === 'skip') {
        fetch('/skip', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            // Optionale Aktion nach erfolgreichem POST-Request
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    } else {
        console.log('Keine Songs in der Warteschlange');
    }
}