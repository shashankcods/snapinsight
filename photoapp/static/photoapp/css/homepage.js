function handleFileUpload(event) {
    const file = event.target.files[0]; // Get the file from the input field
    if (file) {
        let reader = new FileReader();

        // Event listener for when the file is successfully loaded
        reader.onload = function(e) {
            const imagePreview = document.createElement('img');
            imagePreview.src = e.target.result;  // Set the image preview to the file's data URL
            imagePreview.alt = "Uploaded Image"; // Add an alt tag for accessibility
            imagePreview.style.maxWidth = "200px"; // Optional: Set max width for preview

            // Display the uploaded image
            const previewContainer = document.querySelector('.image_preview');
            previewContainer.innerHTML = '';  // Clear any previous content in the preview container
            previewContainer.appendChild(imagePreview); // Append the image to the preview section
        };

        reader.readAsDataURL(file); // Read the image as a data URL to preview it
    }
}

function sendImageToBackend(file) {
    const formData = new FormData();
    formData.append('photo', file); // Append the file to FormData

    // Send the file using Fetch API (assuming the backend is set up to accept this)
    fetch('/upload/', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())  // Assuming the backend responds with JSON
    .then(data => {
        console.log('File uploaded successfully:', data);
        // You can also display results or a message from the backend here
    })
    .catch(error => {
        console.error('Error uploading file:', error);
    });
}
