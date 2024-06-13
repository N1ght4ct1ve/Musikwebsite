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

document.getElementById('fileButton').addEventListener('click', function() {
    document.getElementById('fileInput').click();
});

document.getElementById('fileInput').addEventListener('change', function() {
    if (this.files.length > 0) {
        const fileName = this.files[0].name;
        document.getElementById('fileButton').innerHTML = `Ausgewählte Datei: ${fileName}`;
    }
});
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM fully loaded and parsed');

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
        fetch('/' + command, { method: 'POST' })
            .then(() => refreshQueue());
    }

    document.getElementById('fileButton').addEventListener('click', function () {
        document.getElementById('fileInput').click();
    });

    document.getElementById('fileInput').addEventListener('change', function () {
        if (this.files.length > 0) {
            const fileName = this.files[0].name;
            document.getElementById('fileButton').innerHTML = `Ausgewählte Datei: ${fileName}`;
        }
    });

    var theme = "light";

    /* LIGHT/DARK MODE toggle */
    const toggle = document.getElementById("toggleDark");
    const body = document.querySelector("body");
    const header = document.getElementById("header");
    const main2 = document.getElementById("main2")

    toggle.addEventListener("click", function () {
        this.classList.toggle("bi-brightness-high-fill");
        if (this.classList.toggle("bi-moon")) {
            body.style.background = "#D7DFE2";
            body.style.color = "white";
            body.style.transition = "2s";

            header.style.background = "#D7DFE2";
            header.style.color = "white";
            header.style.transition = "2s";

            main2.style.background = "#D7DFE2";
            main2.style.color = "white";
            main2.style.transition = "2s";

        } else {
            body.style.background = "#030303";
            body.style.color = "black";
            body.style.transition = "2s";

            header.style.background = "#030303";
            header.style.color = "black";
            header.style.transition = "2s";

            main2.style.background = "#030303";
            main2.style.color = "black";
            main2.style.transition = "2s";
        };
    });

    document.addEventListener('DOMContentLoaded', () => {
        console.log('DOM fully loaded and parsed');
    
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
            fetch('/' + command, { method: 'POST' })
                .then(() => refreshQueue());
        }
    
        document.getElementById('fileButton').addEventListener('click', function () {
            document.getElementById('fileInput').click();
        });
    
        document.getElementById('fileInput').addEventListener('change', function () {
            if (this.files.length > 0) {
                const fileName = this.files[0].name;
                document.getElementById('fileButton').innerHTML = `Ausgewählte Datei: ${fileName}`;
            }
        });
    
        var theme = "light";
    
        /* LIGHT/DARK MODE toggle */
        const toggle = document.getElementById("toggleDark");
        const body = document.querySelector("body");
        const header = document.getElementById("header");
        const main2 = document.getElementById("main2")
    
        toggle.addEventListener("click", function () {
            this.classList.toggle("bi-brightness-high-fill");
            if (this.classList.toggle("bi-moon")) {
                body.style.background = "#D7DFE2";
                body.style.color = "white";
                body.style.transition = "2s";
    
                header.style.background = "#D7DFE2";
                header.style.color = "white";
                header.style.transition = "2s";
    
                main2.style.background = "#D7DFE2";
                main2.style.color = "white";
                main2.style.transition = "2s";
    
            } else {
                body.style.background = "#030303";
                body.style.color = "black";
                body.style.transition = "2s";
    
                header.style.background = "#030303";
                header.style.color = "black";
                header.style.transition = "2s";
    
                main2.style.background = "#030303";
                main2.style.color = "black";
                main2.style.transition = "2s";
            };
        });
    
        // Select the dark theme button
        const themeButtonDark = document.getElementById('dark');
        console.log('Dark Button:', themeButtonDark); // Debugging line
    
        // Add a click event listener to the dark theme button
        if (themeButtonDark) {
            themeButtonDark.addEventListener('click', () => {
                // Set the data-theme attribute to 'dark'
                document.documentElement.setAttribute('data-theme', 'dark');
            });
        } else {
            console.error("Button with ID 'dark' not found");
        }
    
        // Select the light theme button
        const themeButtonLight = document.getElementById('light');
        console.log('Light Button:', themeButtonLight); // Debugging line
    
        // Add a click event listener to the light theme button
        if (themeButtonLight) {
            themeButtonLight.addEventListener('click', () => {
                // Set the data-theme attribute to 'light'
                document.documentElement.setAttribute('data-theme', 'light');
            });
        } else {
            console.error("Button with ID 'light' not found");
        }
    });


}) 

document.addEventListener('DOMContentLoaded', () => {
    // Add click event listener to the button with id "test"
    const testButton = document.getElementById('test');

    if (testButton) {
        testButton.addEventListener('click', () => {
            console.log('Button with id "test" clicked!');
            // Perform any actions you want when the button is clicked
        });
    } else {
        console.error('Button with id "test" not found.');
    }
});

document.addEventListener('DOMContentLoaded', () => {
    // Add click event listener to the button with id "test"
    const testButton = document.getElementById('test');

    if (testButton) {
        testButton.addEventListener('click', () => {
            console.log('Button with id "test" clicked!');
            // Perform any actions you want when the button is clicked
        });
    } else {
        console.error('Button with id "test" not found.');
    }
});


document.addEventListener('DOMContentLoaded', () => {
    // Add click event listener to the button with id "test"
    const testButton = document.getElementById('test');

    if (testButton) {
        testButton.addEventListener('click', () => {
            console.log('Button with id "test" clicked!');
            // Perform any actions you want when the button is clicked
        });
    } else {
        console.error('Button with id "test" not found.');
    }
});