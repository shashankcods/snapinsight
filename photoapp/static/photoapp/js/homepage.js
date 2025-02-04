function handleFileUpload(event) {
    const file = event.target.files[0]; 
    if (file) {
        let reader = new FileReader();

        reader.onload = function(e) {
            const previewContainer = document.querySelector('.image_preview');
            previewContainer.innerHTML = '';

            const imagePreview = document.createElement('img');
            imagePreview.src = e.target.result;
            imagePreview.style.opacity = "0"; 
            imagePreview.style.transition = "opacity 1s ease-in"; 

            previewContainer.appendChild(imagePreview);

            setTimeout(() => {
                imagePreview.style.opacity = "1"; 
            }, 50);

            previewContainer.style.transition = "border-color 1s ease-out"; 
            setTimeout(() => {
                previewContainer.style.borderColor = "transparent"; 
            }, 50); 
        };

        reader.readAsDataURL(file); 
    }
}
