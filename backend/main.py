
from fastapi import FastAPI, UploadFile, File, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, PlainTextResponse
from pathlib import Path
from uuid import uuid4
from langchain_community.llms import Ollama

# ------------------------------------------------------------
# FastAPI initialisation
# ------------------------------------------------------------

app = FastAPI(title="Modern Question Generator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------------------
#  Models & helpers
# ------------------------------------------------------------

_MODELS = {
    "programming": {
        "name": "falcon:7b",
        "system": "You are an experienced software‑engineering instructor who designs thought‑provoking exam questions.",
    },
    "math": {
        "name": "mathstral:7b",
        "system": "You are a mathematics lecturer who writes rigorous problem‑sets with worked solutions.",
    },
}


def get_llm(model_type: str):
    cfg = _MODELS.get(model_type)
    if cfg is None:
        raise ValueError("Unsupported model_type")
    return Ollama(
        model=cfg["name"],
        temperature=0.2,
        system=cfg["system"],
    )


CONTENT_TEMPLATE = """    You are an expert educational assessment designer. Your task is to carefully read the **lesson content** (written in Markdown)
and craft a **diverse set of deep, insight‑testing questions** in **pure LaTeX**.

─── Guidelines ───────────────────────────────────────────────
• Mix question types: multiple‑choice, short‑answer, fill‑in‑the‑blank, proof/long‑form, and at least one creative/novel type.  
• Vary the cognitive level (recall → application → analysis → synthesis).  
• For each question, include the correct answer right after the question inside an \answer{{...}} macro.  
• Wrap the complete list in a standalone \begin{{questions}} … \end{{questions}} environment so the resulting .tex compiles directly.  
• Do **not** output any text outside the LaTeX.  

─── Lesson content ───────────────────────────────────────────
{content}
──────────────────────────────────────────────────────────────

Write between 8 and 15 questions.
"""

SAMPLE_TEMPLATE = """    Below you see a **sample question set** formatted in LaTeX.  
Your task is to create a **new set of similar but original questions** that test the same concepts, *without copying text*.

─── Sample ───────────────────────────────────────────────────
{sample}
──────────────────────────────────────────────────────────────

Follow the same LaTeX structure and include answers inside \answer{{…}} macros.  
Produce between 8 and 15 questions only. Return **pure LaTeX**, nothing else.
"""


def build_prompt(md_text: str | None, sample_tex: str | None) -> str:
    if sample_tex:
        return SAMPLE_TEMPLATE.format(sample=sample_tex)
    if md_text:
        return CONTENT_TEMPLATE.format(content=md_text)
    raise ValueError("You must provide either lesson content or a sample question file.")


# ------------------------------------------------------------
#  Routes
# ------------------------------------------------------------

@app.post("/generate_questions")
async def generate_questions(
    md_file: UploadFile = File(None, description="Markdown lesson content"),
    sample_file: UploadFile | None = File(None, description="Existing LaTeX sample"),
    model_type: str = Query("programming", description="Choice of local LLM"),
):
    """Generate a .tex file from uploaded lesson content **or** a LaTeX sample.

    Exactly one of *md_file* or *sample_file* must be supplied.
    """

    md_text = (await md_file.read()).decode() if md_file else None
    sample_tex = (await sample_file.read()).decode() if sample_file else None

    prompt = build_prompt(md_text, sample_tex)

    llm = get_llm(model_type)
    tex_output = llm(prompt)

    token = uuid4().hex
    tex_path = Path(f"questions_{token}.tex")
    tex_path.write_text(tex_output, encoding="utf-8")

    return {"file_name": tex_path.name}


@app.get("/download/{file_name}")
async def download(file_name: str):
    path = Path(file_name)
    if not path.exists():
        return PlainTextResponse("File not found", status_code=404)
    return FileResponse(
        path=path,
        filename=path.name,
        media_type="text/x-tex",
        headers={"Content-Disposition": f"attachment; filename={path.name}"},
    )


# Serve the modern static front‑end (built with Tailwind / Vanilla JS)
from fastapi.staticfiles import StaticFiles

static_path = Path(__file__).parent / "static"
if static_path.exists():
    app.mount("/", StaticFiles(directory=str(static_path), html=True), name="static")
