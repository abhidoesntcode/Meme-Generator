after going to the project folder run this command:-    
uvicorn main:app --reload

Once it says "Application startup complete", open your web browser and go to this exact address: 
👉 http://localhost:8000

Project Title: AI Meme Generator

Tech Stack: Python, FastAPI, JavaScript (ES6+), HTML5, CSS3, Google Gemini API, Pillow (PIL), Render/Vercel

Comprehensive Project Breakdown:

1. Advanced Multimodal AI Integration (Google Gemini)

Vision & Text Processing: Integrated the Google GenAI API leveraging the gemini-2.5-flash multimodal LLM. The system successfully analyzes pixel-level context from user-uploaded images and contextualizes it alongside injected text guidelines to synthesize humor.
Dynamic Prompt Engineering: Engineered dynamic prompt templates that map user-selected personas (Sarcastic, Dark Humor, Wholesome, Gen Z Brainrot, Dad Jokes) into strict formatting constraints, forcing the LLM to output exactly 5 complete, numbered, and contextually appropriate sentences.
Intelligent Two-Tier Fallback System: Designed a highly resilient execution block. If the primary vision-based API call fails (due to strict payload limits, 400 token errors, or server-side glitches), the backend catches the exception and automatically triggers a secondary, text-only generative fallback prompt—ensuring 100% application uptime and a seamless user experience despite underlying API limitations.
API Model Diagnostics: Developed an administrative /api/health diagnostic endpoint that dynamically lists all available GenAI models specifically authorized by the server's API key, ensuring smooth scaling and future model updates.

2. Backend Architecture & Data Optimization (FastAPI)

High-Performance API Routing: Architected the backend using Python’s FastAPI, creating asynchronous POST endpoints (/api/generate) capable of handling complex MIME-type multipart/form-data (images and form strings) concurrently.
Image Payload Optimization: Implemented strict server-side preprocessing using the Python Pillow (PIL) library. The backend intercepts raw image buffers, dynamically resizes them to a maximum dimension of 800px, and re-saves them into a compressed JPEG byte-array in volatile memory before transmitting them to Google's servers. This dramatically reduces API token consumption, prevents payload rejections, and significantly shortens network transit times.

3. Frontend Engineering & DOM Manipulation (Vanilla JS)

Asynchronous State Management: Utilized modern ES6 async/await syntax and the fetch API to handle data transmission to the backend. Built a robust UI state manager that disables inputs, displays engaging loading spinners, and dynamically renders HTML output using marked.js upon receiving the AI's markdown response.
Advanced File Handling: Engineered a custom drag-and-drop file upload zone. Implemented native browser FileReader APIs to immediately read and display client-side image previews in Base64 before server submission, minimizing perceived latency and improving UX.
Algorithmic Micro-Animations: Wrote a self-executing continuous Javascript engine (IIFE) that procedurally generates floating background emojis. The algorithm randomizes spawn coordinates (using viewport width calculations), font scaling, traversal duration (8–18 seconds), and css opacity, dynamically injecting and garbage-collecting DOM elements to prevent memory leaks and ensure optimal frame rates.

4. UI/UX Design & SEO (HTML5/CSS3)

Glassmorphism Aesthetic: Developed a highly modern, responsive UI leveraging advanced CSS properties (backdrop-filter: blur, rgba translucency, and multi-layered drop shadows) to create a premium frosted-glass effect over dynamically animated SVG background blobs.
Comprehensive SEO & Metadata: Implemented best-in-class technical SEO standardizations within the HTML <head>. This includes Open Graph (og:) tags for rich previews on Facebook/LinkedIn, Twitter Cards for native X rendering, and a fully compliant application/ld+json schema definition to ensure the web app is contextually understood by search engine crawlers.
Accessibility & UX Consistency: Ensured robust semantic structuring and accessibility through custom icon implementations (FontAwesome), clear contextual label tags, zero-layout-shift image placeholders, and dedicated empty/error states that clearly communicate backend failures to the end user.
