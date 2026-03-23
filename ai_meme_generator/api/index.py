from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import google.generativeai as genai
from PIL import Image
import io
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="AI Meme Generator")

# Enable CORS 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = os.getenv("GEMINI_API_KEY")

# Define the base directory (where index.html and other files are)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@app.post("/api/generate")
async def generate_meme(
    image: UploadFile = File(...),
    humor_style: str = Form(...)
):
    try:
        if not API_KEY:
            raise HTTPException(status_code=500, detail="GEMINI_API_KEY is not configured on Render")

        # Read the uploaded image
        contents = await image.read()
        img = Image.open(io.BytesIO(contents))
        
        # Configure Gemini
        genai.configure(api_key=API_KEY)
        
        # Try different model names for better compatibility
        model_names = ['gemini-1.5-flash-latest', 'gemini-1.5-flash', 'gemini-pro']
        model = None
        for name in model_names:
            try:
                model = genai.GenerativeModel(name)
                # Success
                break
            except:
                continue
        
        if not model:
             raise Exception("Failed to initialize any compatible Gemini models.")

        prompt = f"Analyze this image and generate 5 short meme captions. Style: {humor_style}."
        
        response = model.generate_content([prompt, img])
        
        return {"success": True, "captions": response.text}
        
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# --- RENDER STATIC FILE SERVING ---
# This allows Render to serve your script.js, style.css, etc.
app.mount("/static", StaticFiles(directory=BASE_DIR), name="static")

@app.get("/")
async def read_index():
    return FileResponse(os.path.join(BASE_DIR, "index.html"))

@app.get("/api/health")
async def health():
    return {"status": "ok"}

@app.get("/robots.txt", include_in_schema=False)
async def robots():
    return FileResponse(os.path.join(BASE_DIR, "robots.txt"))

@app.get("/sitemap.xml", include_in_schema=False)
async def sitemap():
    return FileResponse(os.path.join(BASE_DIR, "sitemap.xml"))
