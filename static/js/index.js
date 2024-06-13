document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM fully loaded and parsed');

    // Function to refresh queue data
    function refreshQueue() {
        fetch('/queue')
            .then(response => response.json())
            .then(data => {
                document.getElementById('queue').innerHTML = data.queue.map(song => '<li>' + song + '</li>').join('');
                document.getElementById('current_song').innerHTML = 'Current song: ' + data.current_song.title;
                document.getElementById('cover').src = data.current_song.cover;
            })
            .catch(error => {
                console.error('Error fetching queue data:', error);
            });
    }

    // Call refreshQueue initially and every 5 seconds
    refreshQueue();
    setInterval(refreshQueue, 5000);

    // Function to send commands
    function sendCommand(command) {
        fetch('/' + command, { method: 'POST' })
            .then(() => refreshQueue())
            .catch(error => {
                console.error('Error sending command:', error);
            });
    }

    // Event listener for the "test" button
    const testButton = document.getElementById('test');
    if (testButton) {
        testButton.addEventListener('click', () => {
            console.log('Button with id "test" clicked!');
            // Perform any actions you want when the button is clicked
        });
    } else {
        console.error('Button with id "test" not found.');
    }

    // Event listener for the "dark" button
    const darkButton = document.getElementById('dark');
    if (darkButton) {
        darkButton.addEventListener('click', () => {
            console.log('Button with id "dark" clicked!');
            // Perform any actions you want when the button is clicked
            document.documentElement.setAttribute('data-theme', 'dark');
        });
    } else {
        console.error('Button with id "dark" not found.');
    }

    // Event listener for the "light" button
    const lightButton = document.getElementById('light');
    if (lightButton) {
        lightButton.addEventListener('click', () => {
            console.log('Button with id "light" clicked!');
            // Perform any actions you want when the button is clicked
            document.documentElement.setAttribute('data-theme', 'light');
        });
    } else {
        console.error('Button with id "light" not found.');
    }

    // Event listener for the file button to trigger file input
    const fileButton = document.getElementById('fileButton');
    if (fileButton) {
        fileButton.addEventListener('click', () => {
            document.getElementById('fileInput').click();
        });
    } else {
        console.error('Button with id "fileButton" not found.');
    }

    // Event listener for file input change
    const fileInput = document.getElementById('fileInput');
    if (fileInput) {
        fileInput.addEventListener('change', function () {
            if (this.files.length > 0) {
                const fileName = this.files[0].name;
                document.getElementById('fileButton').innerHTML = `Selected File: ${fileName}`;
            }
        });
    } else {
        console.error('File input with id "fileInput" not found.');
    }

    // Theme toggle functionality (already present in your code)

});
