from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from app.summarizer import summarize_text, summarize_text_async
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
import os
import logging
import json

# Preload the model on startup to avoid delays on first request
# Use lifespan event handler since on_event is deprecated
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code to run during startup
    logging.info("Preloading Pegasus model...")
    _ = summarize_text("This is a test text.")
    logging.info("Model preloaded successfully.")

    yield  # Wait until the app is shutting down

    # Run during shutdown
    logging.info("Application is shutting down.")

app = FastAPI(lifespan=lifespan)

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