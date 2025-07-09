import os
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional

from backend.utils import (
    get_available_models,
    load_model,
    build_prompt_from_markdown,
    build_prompt_from_tex,
    run_model_selector,
    save_tex_file,
)

app = FastAPI()

# Enable CORS for all origins (adjust in production!)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static directory to serve frontend assets
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configurable paths
MODELS_DIR = "~/llama.cpp/models/"
MODEL_SELECTOR_MODEL = "~/llama.cpp/models/DeepSeek-R1-0528-Qwen3-8B-Q4_K_M.gguf"  # e.g. "models/deepseek-selector.gguf" or None to disable selector

# Request body for generating questions from text content
class GenerateRequest(BaseModel):
    content: str
    model_type: Optional[str] = None  # if None, use model selector


@app.post("/generate_questions")
async def generate_questions(
    request: GenerateRequest,
    content_language: str = Form("fa")
):
    # Load list of available models
    models = get_available_models(MODELS_DIR)
    if not models:
        raise HTTPException(status_code=500, detail="No available models found")

    # Decide which model to use
    model_name = request.model_type
    if not model_name or model_name not in models:
        # Use model selector if available, else first model
        if MODEL_SELECTOR_MODEL:
            model_name = run_model_selector(request.content, models, MODEL_SELECTOR_MODEL)
        else:
            model_name = models[0]

    model_path = os.path.join(MODELS_DIR, model_name)
    llm = load_model(model_path)

    prompt = build_prompt_from_markdown(request.content, language=content_language)
    response = llm(prompt)

    # Assume response is dict with "choices"[0]["text"]
    generated_text = response.get("choices", [{}])[0].get("text", "")

    file_path = save_tex_file(generated_text)

    return {"file_path": file_path, "model_used": model_name}


@app.post("/generate_similar_questions")
async def generate_similar_questions(
    file: UploadFile = File(...),
    model_type: Optional[str] = Form(None),
    content_language: str = Form("fa"),
):
    content_bytes = await file.read()
    try:
        content_str = content_bytes.decode("utf-8").strip()
    except Exception:
        raise HTTPException(status_code=400, detail="Unable to decode uploaded file as UTF-8")

    models = get_available_models(MODELS_DIR)
    if not models:
        raise HTTPException(status_code=500, detail="No available models found")

    model_name = model_type
    if not model_name or model_name not in models:
        if MODEL_SELECTOR_MODEL:
            model_name = run_model_selector(content_str, models, MODEL_SELECTOR_MODEL)
        else:
            model_name = models[0]

    model_path = os.path.join(MODELS_DIR, model_name)
    llm = load_model(model_path)

    prompt = build_prompt_from_tex(content_str, language=content_language)
    response = llm(prompt)
    generated_text = response.get("choices", [{}])[0].get("text", "")

    file_path = save_tex_file(generated_text, suffix="_similar")

    return {"file_path": file_path, "model_used": model_name}


@app.get("/download_file/{file_name}")
async def download_file(file_name: str):
    safe_path = os.path.join("output", os.path.basename(file_name))
    if not os.path.isfile(safe_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(
        path=safe_path,
        filename=os.path.basename(safe_path),
        media_type="text/plain",
        headers={"Content-Disposition": f"attachment; filename={os.path.basename(safe_path)}"},
    )
