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

/////
var theme = "light";


/* LIGHT/DARK MODE toggle */

const toggle = document.getElementById("toggleDark");
const body = document.querySelector("body");
const main = document.querySelector("main");

toggle.addEventListener("click", function(){
    this.classList.toggle("bi-moon");
    if(this.classList.toggle("bi-brightness-high-fill")){

        body.style.background = "#D7DFE2";
        body.style.color = "black";
        body.style.transition = "2s";

        main.style.background = "#b5b5b5";
        main.style.color = "white";
        main.style.transition = "2s";

    }else{
        body.style.background ="#030303" ;
        body.style.color = "white";
        body.style.transition = "2s";

        main.style.background = "#3c3c3c";
        main.style.color = "black";
        main.style.transition = "2s"

    };
});

