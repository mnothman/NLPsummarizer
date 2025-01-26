from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from app.summarizer import summarize_text, summarize_text_async
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.responses import FileResponse
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
        body = await request.body()
        if not body:
            return JSONResponse({"error": "Request body is empty."}, status_code=400)

        data = await request.json()
        text = data.get("text", "").strip()

        if not text:
            return JSONResponse({"error": "Input text cannot be empty."}, status_code=400)

        # Use async function to summarize text for performance
        summary = await summarize_text_async(text)
        return {"summary": summary}
    except json.JSONDecodeError:
        return JSONResponse({"error": "Invalid JSON format in request body."}, status_code=400)
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")
        return JSONResponse({"error": f"An unexpected error occurred: {str(e)}"}, status_code=500)


dist_path = os.path.join(os.path.dirname(__file__), "dist")
if not os.path.exists(dist_path):
    raise RuntimeError(f"Directory '{dist_path}' does not exist")

app.mount("/dist", StaticFiles(directory=dist_path), name="dist")

@app.get("/", response_class=FileResponse)
async def serve_index():
    index_path = os.path.join(dist_path, "index.html")
    if not os.path.exists(index_path):
        raise RuntimeError(f"Index file '{index_path}' does not exist")
    return FileResponse(index_path)

@app.get("/{full_path:path}")
async def fallback(full_path: str):
    index_path = os.path.join(dist_path, "index.html")
    if not os.path.exists(index_path):
        raise RuntimeError(f"Index file '{index_path}' does not exist")
    return FileResponse(index_path)