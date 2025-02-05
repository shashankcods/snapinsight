function handleFileUpload(event) {
    console.log("File upload triggered...")
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

        const formData = new FormData();
        formData.append("photo", file); 

        fetch("/api/upload/", {  
            method: "POST", 
            body: formData, 
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            fetchScores();
        })
        .catch(error => console.error('Error:', error));
    }
}

function fetchScores() {
    console.log('fetching scores.........');

    fetch("/api/images/?format=json")
        .then(response => {
            return response.json();
        })
        .then(data => {
            console.log('Fetched data:', data);

            const scores = {
                temperature: data.brightness_score,
                tint: data.contrast_score,
                exposure: data.saturation_score,
                contrast: data.sharpness_score,
                highlights: data.overall_score,
                shadows: 50, 
                whites: 50,
                blacks: 50,
                vibrance: 50,
                saturation: data.saturation_score
            };

            updateProgressBar('param1', scores.temperature);
            updateProgressBar('param2', scores.tint);
            updateProgressBar('param3', scores.exposure);
            updateProgressBar('param4', scores.contrast);
            updateProgressBar('param5', scores.highlights);
            updateProgressBar('param6', scores.shadows);
            updateProgressBar('param7', scores.whites);
            updateProgressBar('param8', scores.blacks);
            updateProgressBar('param9', scores.vibrance);
            updateProgressBar('param10', scores.saturation);
        })
        .catch(error => console.error('error fetching scores:', error));
}

function updateProgressBar(paramId, score) {
    console.log(`updating progress bar ${paramId} with score ${score}`);

    const bar = document.getElementById(`${paramId}-scale`);
    const value = document.getElementById(`${paramId}-value`);

    bar.style.transition = 'width 1s ease-in-out';
    bar.style.width = `${score}%`;
    value.innerText = Math.round(score); 
}

