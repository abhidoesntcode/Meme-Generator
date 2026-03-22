from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
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

@app.get("/api/health")
async def health():
    return {"status": "ok"}

@app.post("/api/generate")
async def generate_meme(
    image: UploadFile = File(...),
    humor_style: str = Form(...)
):
    try:
        if not API_KEY:
            raise HTTPException(status_code=500, detail="GEMINI_API_KEY is not configured on Vercel")

        # Read the uploaded image
        contents = await image.read()
        img = Image.open(io.BytesIO(contents))
        
        # Configure Gemini
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')

        prompt = f"Analyze this image and generate 5 short meme captions. Style: {humor_style}."
        
        response = model.generate_content([prompt, img])
        
        return {"success": True, "captions": response.text}
        
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
