from fastapi import FastAPI, Request
from app.summarizer import summarize_text, summarize_text_async
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
import os
import logging
import json

app = FastAPI()

logging.basicConfig(level=logging.DEBUG)

@app.post("/summarize")
async def summarize(request: Request):
    try:
        # Read the raw body and then parse JSON from request
        body = await request.body()
        if not body:
            return {"error": "Request body is empty."}

        data = await request.json()
        text = data.get("text", "").strip()

        if not text:
            return {"error": "Input text cannot be empty."}

        # Use async function to summarize text for performance
        summary = await summarize_text_async(text)
        return {"summary": summary}
    except json.JSONDecodeError:
        return {"error": "Invalid JSON format in request body."}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}

static_path = os.path.join(os.path.dirname(__file__), "../static")
app.mount("/static", StaticFiles(directory=static_path), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})