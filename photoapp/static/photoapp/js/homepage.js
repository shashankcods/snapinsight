function handleFileUpload(event) {
    console.log("File upload triggered...");
    const file = event.target.files[0];
    if (file) {
        let reader = new FileReader();

        reader.onload = function (e) {
            const previewContainer = document.querySelector('.image_preview');
            const loadingContainer = document.querySelector('.loading_container');

            // clear previous image preview
            previewContainer.innerHTML = '';

            // create and fade in image preview
            const imagePreview = document.createElement('img');
            imagePreview.src = e.target.result;
            imagePreview.style.opacity = "0";
            imagePreview.style.transition = "opacity 1s ease-in";
            previewContainer.appendChild(imagePreview);

            setTimeout(() => imagePreview.style.opacity = "1", 50);

            // fade out border
            previewContainer.style.transition = "border-color 1s ease-out";
            setTimeout(() => previewContainer.style.borderColor = "transparent", 50);

            // show loading indicator
            if (loadingContainer) {
                loadingContainer.style.display = "block";
                loadingContainer.style.opacity = "1";
                loadingContainer.innerText = "loading...";
                loadingContainer.style.animation = "fadePulse 2s infinite ease-in-out";
            }
        };

        reader.readAsDataURL(file);

        // image upload
        const formData = new FormData();
        formData.append("photo", file);

        fetch("/api/upload/", { method: "POST", body: formData })
            .then(response => response.json())
            .then(data => {
                console.log('Success:', data);
                fetchScores();
            })
            .catch(error => {
                console.error('Error:', error);
                document.querySelector('.loading_container').innerText = "Error loading scores.";
            });
    }
}

function fetchScores() {
    console.log('Fetching scores...');
    const loadingContainer = document.querySelector('.loading_container');

    fetch("/api/images/?format=json")
        .then(response => response.json())
        .then(data => {
            console.log('Fetched data:', data);

            const scores = {
                temperature: data.temperature_score,
                tint: data.tint_score,
                exposure: data.exposure_score,
                contrast: data.contrast_score,
                highlights: data.highlights_score,
                shadows: data.shadows_score,
                whites: data.whites_score,
                blacks: data.blacks_score,
                vibrance: data.vibrance_score,
                saturation: data.saturation_score
            };

            // updates all progress bars
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

            // hiding loading indicator
            if (loadingContainer) {
                loadingContainer.style.animation = "none";
                loadingContainer.style.transition = "opacity 1s ease-out";
                loadingContainer.style.opacity = "0";
                setTimeout(() => (loadingContainer.style.display = "none"), 1000);
            }
        })
        .catch(error => {
            console.error('Error fetching scores:', error);
            if (loadingContainer) loadingContainer.innerText = "Error loading scores.";
        });
}

function updateProgressBar(paramId, score) {
    console.log(`Updating progress bar ${paramId} with score ${score}`);

    const bar = document.getElementById(`${paramId}-scale`);
    const value = document.getElementById(`${paramId}-value`);

    if (bar && value) {
        bar.style.transition = "width 1s ease-in-out";
        bar.style.width = `${score}%`;
        value.innerText = Math.round(score);
    }
}