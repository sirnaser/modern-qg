from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import os

from backend.utils import (
    list_models,
    run_model,
    call_model_selector,
    extract_text_from_tex,
    build_prompt_from_content,
    build_prompt_from_examples
)

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODELS_DIR = "models"

app.mount("/static", StaticFiles(directory="frontend/static"), name="static")


@app.get("/")
def read_index():
    return FileResponse(Path("frontend/index.html"))

@app.get("/api/models")
def get_models():
    models = list_models(MODELS_DIR)
    return {"models": models}

@app.post("/api/generate-from-md")
async def generate_from_md(
    file: UploadFile = File(...),
    model_name: str = Form(...),
    language: str = Form("fa")
):
    try:
        content = await file.read()
        content_text = content.decode("utf-8")
        model_path = os.path.join(MODELS_DIR, model_name)
        prompt = build_prompt_from_content(content_text, language)
        result = run_model(model_path, prompt)
        return JSONResponse(content={"result": result})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/api/generate-from-tex")
async def generate_from_tex(
    file: UploadFile = File(...),
    model_name: str = Form(...),
    language: str = Form("fa")
):
    try:
        tex_content = await file.read()
        tex_text = tex_content.decode("utf-8")
        plain_text = extract_text_from_tex(tex_text)
        model_path = os.path.join(MODELS_DIR, model_name)
        prompt = build_prompt_from_examples(plain_text, language)
        result = run_model(model_path, prompt)
        return JSONResponse(content={"result": result})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/api/select-model")
async def select_model(
    file: UploadFile = File(...),
    language: str = Form("fa")
):
    try:
        content = await file.read()
        content_text = content.decode("utf-8")
        models = list_models(MODELS_DIR)

        default_model = models[0] if models else None
        deepseek_model = next((m for m in models if "deepseek" in m.lower()), default_model)

        selected_model = call_model_selector(
            model_path=os.path.join(MODELS_DIR, deepseek_model),
            prompt=content_text,
            model_names=models
        )

        if selected_model not in models:
            selected_model = default_model

        return JSONResponse(content={"selected_model": selected_model})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
