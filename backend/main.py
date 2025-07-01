from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pathlib import Path
from multiprocessing import cpu_count
from llama_cpp import Llama
import os, uuid
from backend.model_selector import choose_model

app = FastAPI(title="Modern Question Generator")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static UI files (e.g., index.html)
app.mount("/", StaticFiles(directory="static", html=True), name="static")

# Model registry
MODELS = {
    "deepseek": {
        "path": "models/DeepSeek-R1-0528-Qwen3-8B-Q4_K_M.gguf",
        "system": "You are a knowledgeable general tutor.",
    },
    "math": {
        "path": "models/Nous-Hermes-2-Mistral-7B.Q4_K_M.gguf",
        "system": "You are a math professor creating exam problems.",
    },
    "programming": {
        "path": "models/CodeLlama-7B-Instruct.Q4_K_M.gguf",
        "system": "You are a programming instructor creating exam problems.",
    },
}

# Load LLM instance
def load_llm(key: str):
    cfg = MODELS[key]
    return Llama(
        model_path=cfg["path"],
        n_ctx=4096,
        n_threads=min(8, cpu_count()),
        temperature=0.3,
        system_prompt=cfg["system"],
    )

# Request schema for question generation
class GenerateRequest(BaseModel):
    language: str = "fa"          # Output language: fa | en
    model: str = "auto"           # Model: auto | math | programming | deepseek

# Main API endpoint
@app.post("/generate")
async def generate(
    req: GenerateRequest = Form(...),
    file: UploadFile = File(...),
):
    text = (await file.read()).decode("utf-8")

    # Determine which model to use
    model_key = req.model
    if model_key == "auto":
        model_key = choose_model(text, MODELS.keys())

    llm = load_llm(model_key)

    prompt = (
        f"You are an expert exam designer. "
        f"Language of output: {'Persian' if req.language=='fa' else 'English'}. "
        f"Generate 4–6 deep, varied, creative questions in LaTeX. "
        f"Types: multiple‑choice, short‑answer, proof/derivation, or coding if relevant. "
        f"Provide brief explanations under each answer key. "
        f"\n\nCONTENT START\n{text}\nCONTENT END\n\nQUESTIONS:"
    )

    result = llm(prompt)["choices"][0]["text"]

    filename = f"questions_{uuid.uuid4().hex[:6]}.tex"
    path = Path("output") / filename
    path.parent.mkdir(exist_ok=True)
    path.write_text(result, encoding="utf-8")

    return {"file_path": str(path), "model_used": model_key}

# Download endpoint
@app.get("/download/{file_path:path}")
async def download(file_path: str):
    return FileResponse(file_path, media_type="text/plain", filename=os.path.basename(file_path))
