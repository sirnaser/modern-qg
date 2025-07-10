# 📚 Question Generation System (Offline, Local Models)

An elegant, extendable, and offline-friendly question generation system that uses locally hosted language models (e.g., LLaMA, DeepSeek) to generate high-quality questions from lesson content or example exam files.

---

## 🚀 Features

- 📄 Supports two input types:
  - Markdown lesson content (`.md`)
  - Example questions in LaTeX format (`.tex`)
- 🤖 Choose from local models manually — or let the system **auto-select** the best model
- 🌐 Output language: **Persian** or **English**
- 📥 Outputs result as a downloadable `.tex` file
- 💻 Clean, modern UI with particle background and responsive design
- 📜 Real-time status log with timestamps and detailed process tracking

---

## 📁 Project Structure

```
modern-qg/
├── backend/
│   ├── main.py
│   └── utils.py
├── frontend/
│   ├── index.html
│   └── static/
│       ├── style.css
│       ├── script.js
│       └── particles-config.js
├── models/
│   └── (your .gguf model files here)
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/sirnaser/modern-qg.git
cd modern-qg
```

### 2. Create virtual environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your models

Place your `.gguf` model files inside the `models/` directory. For example:

```
models/
├── DeepSeek-R1-0528-Qwen3-8B-Q4_K_M.gguf
└── Llama-3.2-3B-Instruct-Q4_K_M.gguf
```

---

## 🖥️ Running the App

Start the FastAPI server with:

```bash
uvicorn backend.main:app --reload
```

Then open your browser and go to:

```
http://localhost:8000
```

---

## 📤 Inputs

### Markdown Mode
Upload a `.md` file containing raw lesson content.

### TeX Mode
Upload a `.tex` file containing example exam questions.

---

## 📄 Output Format

The result is generated as a `.tex` file with the following structure:

```latex
\section*{Questions}
(Generated questions)

\newpage

\section*{Answers}
(Answers and references)
```

---

## 🤖 Model Selection

You can either:
- **Manually** select a model from the dropdown, or
- Choose **"Auto-select best model"** to let the system analyze the input and decide which model fits best (using a helper model like DeepSeek).

---

## 🛠️ Advanced Notes

- Make sure your system supports local inference. At least **8GB RAM** is recommended.
- The backend uses [`llama-cpp-python`](https://pypi.org/project/llama-cpp-python/) — no need to compile llama.cpp manually.
- If you encounter this error:

  ```
  Requested tokens (5303) exceed context window of 4096
  ```

  You may adjust the context size (`n_ctx`) in `utils.py`:

  ```python
  llm = Llama(
      model_path=model_path,
      n_ctx=8192,
      ...
  )
  ```

---

## 💬 Status Log

The UI logs all actions, including:

- File uploads
- Model/language changes
- Auto-selection attempts
- Model generation start/complete
- Error handling with timestamp

This helps users know what’s happening under the hood — like a mini debug console.

---

## 👤 Author

Designed and developed by [@sirnaser](https://github.com/sirnaser)  
Made with ❤️ for educational tools and open-source AI

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
