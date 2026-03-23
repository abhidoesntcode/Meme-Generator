from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from google import genai
from google.genai import types
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

        # Read and resize the uploaded image to stay within token limits
        contents = await image.read()
        raw_img = Image.open(io.BytesIO(contents))
        
        # Resize if image is too large (important for token & quota management)
        # We use a max dimension of 800px
        max_dim = 800
        if max(raw_img.width, raw_img.height) > max_dim:
            raw_img.thumbnail((max_dim, max_dim))
        
        # Re-save to buffer for transmission
        img_byte_arr = io.BytesIO()
        raw_img.save(img_byte_arr, format='JPEG', quality=85)
        processed_img = Image.open(img_byte_arr)

        # Initialize Google GenAI Client
        client = genai.Client(api_key=API_KEY)
        
        # --- DIAGNOSTICS: List Available Models to Render Logs ---
        print("DIAGNOSTICS: Listing your available models:")
        try:
            available_models = client.models.list()
            for m in available_models:
                print(f"- Found model: {m.name}")
        except Exception as diag_err:
            print(f"DIAGNOSTIC FAILED: {diag_err}")

        # 100% Free Tier model list
        model_names = [
            'gemini-1.5-flash',        # Fastest, best free quota
            'gemini-1.5-flash-8b',     # Most efficient fallback
        ]
        
        response = None
        last_error = ""
        
        for model_name in model_names:
            try:
                print(f"Attempting to generate with model: {model_name}")
                prompt = f"Generate 5 short, hilarious meme captions for social media. Humor style: {humor_style}. Format as a numbered list."
                
                config = types.GenerateContentConfig(
                    max_output_tokens=300,
                    temperature=0.8,
                    stop_sequences=["\n6", "6."]
                )
                
                # FIRST TRY: With Image
                try:
                    print("TRYING WITH IMAGE...")
                    response = client.models.generate_content(
                        model=model_name,
                        contents=[prompt, processed_img],
                        config=config
                    )
                except Exception as img_err:
                    err_msg = str(img_err).lower()
                    if "token" in err_msg or "400" in err_msg or "limit" in err_msg:
                        print(f"VISION FAILED ({err_msg}). FALLING BACK TO TEXT-ONLY...")
                        # SECOND TRY: Without Image (Fallback)
                        fallback_prompt = f"Create 5 hilarious meme captions for a social media image. Theme/Style: {humor_style}. (AI Note: Image vision was glitchy, so using pure creativity). Format as a numbered list."
                        response = client.models.generate_content(
                            model=model_name,
                            contents=fallback_prompt,
                            config=config
                        )
                    else:
                        raise img_err # Rethrow if it's a different error (like API Key)

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
    diagnostic = {"status": "ok", "api_key_set": bool(API_KEY), "available_models": []}
    if API_KEY:
        try:
            client = genai.Client(api_key=API_KEY)
            models = client.models.list()
            diagnostic["available_models"] = [m.name for m in models]
        except Exception as e:
            diagnostic["error"] = str(e)
    return diagnostic

@app.get("/robots.txt", include_in_schema=False)
async def robots():
    return FileResponse(os.path.join(BASE_DIR, "robots.txt"))

@app.get("/sitemap.xml", include_in_schema=False)
async def sitemap():
    return FileResponse(os.path.join(BASE_DIR, "sitemap.xml"))

