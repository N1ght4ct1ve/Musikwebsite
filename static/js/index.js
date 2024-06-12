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
var theme = "light";


/* LIGHT/DARK MODE toggle */

const toggle = document.getElementById("toggleDark");
const body = document.querySelector("body");

toggle.addEventListener("click", function(){
    this.classList.toggle("bi-moon");
    if(this.classList.toggle("bi-brightness-high-fill")){

        body.style.background = "#D7DFE2";
        body.style.color ="black";
        body.style.transition = "2s";

    }else{
        body.style.background ="#030303" ;
        body.style.color = "white";
        body.style.transition = "2s";

    };
});

