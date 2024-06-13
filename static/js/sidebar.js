function openNav() {
    var sidebar = document.getElementById("sidebar")
    var root = document.getElementById("root")
    sidebar.style.width = "250px";
    root.style.marginLeft = "250px";
    sidebar.style.transition = "2s";
  }
  
/* Set the width of the sidebar to 0 and the left margin of the page content to 0 */
function closeNav() {
    var sidebar = document.getElementById("sidebar")
    var root = document.getElementById("root")
    sidebar.style.width = "0";
    root.style.marginLeft = "0";
    sidebar.style.transition = "2s";
} 