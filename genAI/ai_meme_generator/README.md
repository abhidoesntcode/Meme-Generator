# AI Meme Generator 😂

A stunning, lightweight web application that uses the Google Gemini Multimodal API to generate funny meme captions for uploaded images based on different humor styles.

This project uses a modern **FastAPI** backend paired with a beautiful **HTML/CSS/JS** frontend.

## Features

- **Beautiful UI:** Premium dark mode design with glassmorphism and smooth animations.
- **Interactive Upload:** Drag and drop image uploader. 
- **Humor Styles:** Choose your caption style from Sarcastic, Dark Humor, Wholesome, Gen Z, or Dad Jokes.
- **AI-Powered:** Uses the `gemini-2.5-flash` model via the FastAPI backend to generate context-aware, funny captions.

## Prerequisites

- [Python 3.8+](https://www.python.org/downloads/)
- A Google Gemini API Key. You can get one for free from [Google AI Studio](https://aistudio.google.com/app/apikey).

## Project Structure

```text
ai_meme_generator/
│
├── main.py             # FastAPI Server & API integration
├── requirements.txt    # Python dependencies
├── README.md           # Project instructions (this file)
└── static/             # Frontend Files
    ├── index.html      # UI Structure
    ├── style.css       # Premium Styling
    └── script.js       # App Logic & API Calls
```

## Installation Instructions

1. **Navigate to the project folder:**
   Make sure you are in the `ai_meme_generator` directory.
   ```bash
   cd path/to/ai_meme_generator
   ```

2. **(Optional but recommended) Create a virtual environment:**
   ```bash
   python -m venv venv
   ```
   Activate the virtual environment:
   - **Windows:** `venv\Scripts\activate`
   - **Mac/Linux:** `source venv/bin/activate`

3. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. **Start the FastAPI Server:**
   ```bash
   uvicorn main:app --reload
   ```
2. **Open the Web App:**
   Open your browser and navigate to:
   [http://localhost:8000](http://localhost:8000)
3. **Generate Memes:**
   - Enter your **Google Gemini API Key**.
   - Upload an image.
   - Select a humor style from the dropdown.
   - Click **Generate Memes** and enjoy the results!
