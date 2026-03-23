from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from google import genai
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

# API Key from Environment
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
        
        # Initialize Google GenAI Client with explicit 'v1' preference
        client = genai.Client(api_key=API_KEY)
        
        # --- DIAGNOSTICS: List Available Models to Render Logs ---
        print("DIAGNOSTICS: Listing your available models:")
        try:
            available_models = client.models.list()
            for m in available_models:
                print(f"- Found model: {m.name}")
        except Exception as diag_err:
            print(f"DIAGNOSTIC FAILED: {diag_err}")

        # Comprehensive fallback list
        model_names = [
            'gemini-1.5-flash',        # Most compatible for free-tier
            'gemini-1.5-pro',          # High-end fallback
            'gemini-1.0-pro',          # Legacy baseline
            'gemini-2.0-flash-exp',    # Experimental
            'gemini-2.0-flash',        # Newest
        ]
        
        response = None
        last_error = ""
        
        for model_name in model_names:
            try:
                print(f"Attempting to generate with model: {model_name}")
                prompt = f"Analyze this image and generate 5 short, hilarious meme captions. Humor style: {humor_style}. Format as a numbered list."
                
                response = client.models.generate_content(
                    model=model_name,
                    contents=[prompt, img]
                )
                if response and response.text:
                    print(f"SUCCESS with model: {model_name}")
                    break
            except Exception as e:
                last_error = str(e)
                print(f"Model {model_name} failed: {last_error}")
                continue
        
        if not response:
            raise Exception(f"All models failed. Last error: {last_error}")
            
        return {"success": True, "captions": response.text}
        
    except Exception as e:
        print(f"FINAL APP ERROR: {e}")
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

