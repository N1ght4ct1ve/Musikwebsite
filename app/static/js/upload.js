const actionButton = document.getElementById('actionButton');
        const urlField = document.getElementById('urlField');
        const fileInput = document.getElementById('fileInput');

        function updateButton() {
            const urlValue = urlField.value.trim();
            const fileCount = fileInput.files.length;

            if (urlValue) {
                actionButton.innerText = 'Download from YouTube';
                actionButton.onclick = () => {
                    fetch('/download', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json' // Setze den Content-Type auf application/json
                        },
                        body: JSON.stringify({string:true,url: urlValue }) // Sende die URL als JSON
                    })
                    .then(response => response.json())
                    .then(data => {
                        console.log('Success:', data);
                    })
                    .catch((error) => {
                        console.error('Error:', error);
                    });
                };
            } else if (fileCount > 0) {
                actionButton.innerText = 'Upload MP3';
                actionButton.onclick = () => {
                    const formData = new FormData();
                    formData.append('file', fileInput.files[0]);

                    fetch('/upload', {
                        method: 'POST',
                        body: formData // Sende das FormData-Objekt
                    })
                    .then(response => response.json())
                    .then(data => {
                        console.log('Success:', data);
                    })
                    .catch((error) => {
                        console.error('Error:', error);
                    });
                };
            } else {
                actionButton.innerText = 'Select File or Enter URL';
                actionButton.onclick = () => { /* No action */ };
            }
        }

        document.addEventListener('DOMContentLoaded', () => {
            urlField.addEventListener('input', updateButton);
            fileInput.addEventListener('change', updateButton);
        });