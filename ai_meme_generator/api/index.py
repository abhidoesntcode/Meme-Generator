from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
from PIL import Image
import io
import os
from dotenv import load_dotenv
from mangum import Mangum

load_dotenv()

app = FastAPI(title="AI Meme Generator")
handler = Mangum(app)

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount not needed in serverless
# Static files served by Vercel directly

API_KEY = os.getenv("GEMINI_API_KEY")

@app.post("/generate")
async def generate_meme(
    image: UploadFile = File(...),
    humor_style: str = Form(...)
):
    try:
        # Read the uploaded image
        contents = await image.read()
        img = Image.open(io.BytesIO(contents))
        
        # Configure Gemini
        genai.configure(api_key=API_KEY)
        
        # Using gemini-1.5-flash as verified to exist for this key
        model_name = 'gemini-1.5-flash'
        try:
            model = genai.GenerativeModel(model_name)
        except Exception as model_err:
            print(f"Error initializing model {model_name}: {model_err}")
            # Fallback to gemini-pro if flash fails
            model = genai.GenerativeModel('gemini-pro')

        prompt = f"Analyze this image and generate 5 short meme captions suitable for social media. Humor style: {humor_style}. Keep them funny and concise. Format the output clearly."
        
        response = model.generate_content([prompt, img])
        
        return {"success": True, "captions": response.text}
        
    except Exception as e:
        print(f"Error during generation: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
