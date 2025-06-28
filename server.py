
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os

from langchain_community.llms import Ollama

app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Model Definitions
models = {
    "programming": {
        "name": "falcon:7b",
        "system": "You are a programming instructor creating exam questions...",
    },
    "math": {
        "name": "mathstral:7b",
        "system": "You are a math tutor creating problems and explanations...",
    },
}


# Request Body with Model Selection
class GenerateRequest(BaseModel):
    content: str
    model_type: str = "programming"  # Default to programming


def get_llm(model_type: str):
    model_info = models.get(model_type)
    if not model_info:
        raise ValueError("Invalid model type selected")
    return Ollama(
        model=model_info["name"],
        temperature=0.3,
        system=model_info["system"],
    )


@app.post("/generate_questions")
async def generate_questions(request: GenerateRequest):
    llm = get_llm(request.model_type)
    prompt_text = f"Based on the following content, generate questions in LaTeX format:\n\n{request.content}\n\nQuestions:"
    response = llm(prompt_text)

    # Save the response to a .tex file
    file_path = "questions.tex"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(response)

    return {"file_path": file_path}


@app.post("/generate_similar_questions")
async def generate_similar_questions(
    file: UploadFile = File(...),
    model_type: str = "programming"
):
    content = await file.read()
    content_str = content.decode("utf-8")

    prompt = (
        f"Below is a sample exam question in LaTeX format:\n\n"
        f"{content_str}\n\n"
        f"Based on this sample, generate similar exam questions in LaTeX format.  Include practical problems and explanations."
    )

    llm = get_llm(model_type)
    response = llm(prompt)

    # Save the response to a .tex file
    file_path = "similar_questions.tex"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(response)

    return {"file_path": file_path}


@app.get("/download_file/{file_path}")
async def download_file(file_path: str):
    file_path = os.path.join(".", file_path)
    return FileResponse(
        path=file_path,
        filename=os.path.basename(file_path),
        media_type="text/plain",  # or "application/pdf" if you save as PDF
        headers={"Content-Disposition": f"attachment; filename={os.path.basename(file_path)}"},
    )