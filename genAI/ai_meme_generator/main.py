from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
from PIL import Image
import io
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="AI Meme Generator")

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the static directory to serve HTML, CSS, JS
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/robots.txt", include_in_schema=False)
async def robots():
    return FileResponse("static/robots.txt", media_type="text/plain")

@app.get("/sitemap.xml", include_in_schema=False)
async def sitemap():
    return FileResponse("static/sitemap.xml", media_type="application/xml")

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
        
        # Using gemini-2.5-flash as verified to exist for this key
        model_name = 'gemini-2.5-flash'
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
