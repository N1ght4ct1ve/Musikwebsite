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

function detectColorScheme() {
    // Default to light

    // Local storage is used to override OS theme settings
    if (localStorage.getItem("theme")) {
        theme = localStorage.getItem("theme");
    } else if (window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches) {
        theme = "dark";
    }

    // Dark theme preferred, set document with a `data-theme` attribute
    if (theme === "dark") {
        document.documentElement.setAttribute("data-theme", "dark");
    } else {
        document.documentElement.setAttribute("data-theme", "light");
    }
}
detectColorScheme();

/* LIGHT/DARK MODE toggle */

const toggle = document.getElementById("toggleDark");
const body = document.querySelector("main");
document.getElementById("toggleDark").onclick = function () {
    if (theme === "light") {
        this.classList.toggle("bi-moon");
        document.documentElement.setAttribute("data-theme", "dark");
        theme = "dark";
        localStorage.setItem("theme", "dark");
    } else {
        this.classList.toggle("bi-brightness-high-fill")
        document.documentElement.setAttribute("data-theme", "light");
        theme = "light";
        localStorage.setItem("theme", "light");
    }
}
