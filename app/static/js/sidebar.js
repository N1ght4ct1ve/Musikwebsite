function toggleNav() {
    var sidebar = document.getElementById("sidebar");
    var root = document.getElementById("root");
    var button = document.querySelector(".openbtn");

    if (sidebar.style.width === "250px") {
        sidebar.style.width = "0";
        root.style.marginLeft = "0";
        button.innerHTML = "&#9776;"; // Hamburger icon
    } else {
        sidebar.style.width = "250px";
        root.style.marginLeft = "250px";
        button.innerHTML = "&times;"; // Close icon
    }
}
