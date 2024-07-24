document.addEventListener('DOMContentLoaded', () => {
    const toggleDarkMode = (enable) => {
        if (enable) {
            document.body.classList.add('dark-mode');
            document.querySelector('.header-bar').classList.add('dark-mode');
        } else {
            document.body.classList.remove('dark-mode');
            document.querySelector('.header-bar').classList.remove('dark-mode');
        }
    };

    const prefersDarkScheme = window.matchMedia("(prefers-color-scheme: dark)").matches;
    toggleDarkMode(prefersDarkScheme);

    window.matchMedia("(prefers-color-scheme: dark)").addEventListener('change', (e) => {
        toggleDarkMode(e.matches);
    });
});

function toggleDarkMode() {
    const isDarkMode = document.body.classList.toggle('dark-mode');
    document.querySelector('.header-bar').classList.toggle('dark-mode', isDarkMode);
}