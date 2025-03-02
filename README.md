<p align="center">
</p>
<a href="https://weekendofcode.computercodingclub.in/"> <img src="https://i.postimg.cc/njCM24kx/woc.jpg" height=30px> </a>

## Introduction:
**snapinsight** is a minimalistic web-based tool designed to help photographers enhance their composition and editing skills. Users can upload a photo, and the platform provides an instant evaluation based on key photography fundamentals such as exposure, contrast, highlights, shadows, and color balance. Each parameter is scored on a scale of 0-100, with a visual representation of strengths and areas for improvement. The project focuses on simplicity, usability, and an intuitive user experience, making it an accessible tool for photographers of all skill levels. 

  
## Table of Contents:
  - [Features](#features)
  - [How Scores Are Derived](#how-scores-are-derived)
  - [Folder Structure](#folder-structure)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Future Improvements](#future-improvements)
  - [Technology Stack](#technology-stack)
  - [Contributors](#contributors)


## Features
- **Real-time Image Analysis**
- **Score-Based Feedback System**
- **Minimalistic, Aesthetic UI**
- **Mobile-Friendly Design**

## How Scores Are Derived
Our system uses **CLIP (Contrastive Language–Image Pretraining)** to analyze the uploaded photo.
1. **Image Classification with CLIP**: 
   - The image is processed using CLIP, which identifies the closest matching photography category (e.g., "sunset," "portrait").
2. **Fetching Ideal Parameter Values**:
   - Predefined ideal values for each parameter (exposure, contrast, etc.) are retrieved based on the detected category.
3. **Score Calculation**:
   - The uploaded image's parameters are extracted.
   - Each parameter is compared with the ideal values.
   - A score (0-100) is assigned based on how close the image’s parameters are to the ideal values.
   - A **visual bar representation** displays these scores.
   
This method ensures that feedback is adaptive, offering personalized suggestions for improvement based on the image type.

## Folder Structure

The main project files are inside the `photoapp` folder. Below is the structure:

```plaintext
photoapp/
│── templates/ # Contains all HTML files
│── static/ # Holds static assets
│ ├── css/ # CSS files for styling
│ ├── js/ # JavaScript files
```

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/shashankcods/snapinsight.git
   cd snapinsight
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Run the Django backend:
   ```sh
   python manage.py runserver
   ```
4. Open `homepage.html` in your browser to view the frontend.

## Usage
1. Upload a photo by clicking the **upload** button.
2. Wait for the loading animation while the backend analyzes the photo.
3. View the score for each photography parameter.

## Future Improvements
We plan to enhance the project with the following features:

- **More Detailed Insights**: Provide deeper analysis of images, including composition, sharpness, and color theory evaluation.
- **User History Page**: A dedicated page where users can view their past uploads and corresponding scores.
- **Custom Machine Learning Model**: Instead of relying on predefined parameters, we aim to train our own ML model to analyze images and offer more accurate feedback.
- **Mobile Optimization Enhancements**: Improve the mobile experience with a more responsive UI.
- **User Authentication**: Implement user accounts to save progress and access past results anytime.
  
## Technology Stack:
  1) HTML, CSS
  2) Vanilla JS
  3) Fetch API
  4) Django
  5) CLIP for image understanding
  6) Figma (for UI/UX design)
  
## Contributors:

Team Name: Figma Boys

* [Harish Raju](https://github.com/kyrolxg)
* [Shabbeer Mohammed](https://github.com/Shabbeer2513)
* [Sumit Surendran](https://github.com/sumit10866)


### Made at:



<a href="https://weekendofcode.computercodingclub.in/"> <img src="https://i.postimg.cc/Z9fC676j/devjam.jpg" height=30px> </a>
