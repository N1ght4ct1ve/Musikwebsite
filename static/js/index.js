document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM fully loaded and parsed');
    document.querySelectorAll('img').forEach(function(img){
        img.onerror = function(){
            // this.style.display='none';
            this.style.backgroundImage = 'static/temp/default.png'
        };
     })

    // Function to refresh queue data
    function refreshQueue() {
        fetch('/queue')
            .then(response => response.json())
            .then(data => {
                document.getElementById('queue').innerHTML = data.queue.map(song => '<li>' + song + '</li>').join('');
                document.getElementById('current_song').innerHTML = data.current_song.title;
                document.getElementById('cover').src = data.current_song.cover;
            })
            .catch(error => {
                console.error('Error fetching queue data:', error);
            });
    }

    // Call refreshQueue initially and every 5 seconds
    refreshQueue();
    setInterval(refreshQueue, 5000);


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

    const songOverview = document.getElementById('queue_box');
    if (songOverview) {
        // Setze die ursprüngliche Höhe des songOverview-Elements
        const originalHeight = "50px";
    
        songOverview.addEventListener('click', () => {
            const numberOfSongs = songOverview.getElementsByClassName('song-item').length;
            const heightPerSong = 60; // Höhe eines einzelnen Liedes in Pixeln (anpassen nach Bedarf)
            const maxHeight = 80 * window.innerHeight / 100; // 80vh in Pixel umgerechnet
            // const newHeight = Math.min(numberOfSongs * heightPerSong, maxHeight);
            var newHeight = numberOfSongs * heightPerSong;
            songOverview.style.height = `${newHeight}px`;
            songOverview.style.transition = ".5s";
        });
    
        // window.addEventListener('scroll', () => {
        //     // Setze die Höhe zurück auf die ursprüngliche Höhe, wenn die Seite scrollt
        //     songOverview.style.height = originalHeight;
        // });
    } else {
        console.error('File input with id "fileInput" not found.');
    }



    // Theme toggle functionality (already present in your code)

});


const checkbox = document.querySelector(".theme-switch__checkbox");

    checkbox.addEventListener('change', function() {
        if(this.checked) {
            // Dark mode
            localStorage.setItem("mode", "dark");
            document.documentElement.setAttribute('data-theme', 'dark');
        } else {
            // Light mode
            localStorage.setItem("mode", "light");
            document.documentElement.setAttribute('data-theme', 'light');
        }
    });

     // On page load or refresh, check localStorage to set the theme
     const currentMode = localStorage.getItem("mode");
     if(currentMode === "dark") {
         checkbox.checked = true;
         document.documentElement.setAttribute('data-theme', 'dark');
     } else {
         checkbox.checked = false;
         document.documentElement.setAttribute('data-theme', 'light');
     }