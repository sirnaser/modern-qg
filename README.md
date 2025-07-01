# Modern Question Generator API

A FastAPI-based backend with a simple React frontend for generating exam questions from educational content using local language models.

---

## Features

- Upload educational content files in `.md` (Markdown) or `.tex` (LaTeX) formats.
- Automatically detect content type and select a suitable language model (Programming or Math).
- Option to select output language (Persian/Farsi or English).
- Generate LaTeX formatted exam questions that are logical, deep, and creative.
- Clean, minimal user interface with university branding and animated background.
- Download generated `.tex` files easily.
- Support for local language models via `llama.cpp` or Ollama integration.

---

## Requirements

- Python 3.9 or higher
- Node.js and npm (for frontend build)
- Compatible language models such as DeepSeek-R1, Mistral 7B, Falcon, etc.

---

## Setup Instructions

### Backend Setup

1. Create and activate a Python virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate   # On Linux/macOS
   .venv\Scripts\activate      # On Windows
   ```

2. Install backend dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the backend server:

   ```bash
   uvicorn backend.main:app --reload
   ```

   The API server will be available at:  
   `http://127.0.0.1:8000`

---

### Frontend Setup

1. Navigate to the frontend directory:

   ```bash
   cd frontend
   ```

2. Install frontend dependencies:

   ```bash
   npm install
   ```

3. Build the React frontend:

   ```bash
   npm run build
   ```

4. Copy the contents of the `build/` directory into the backend’s static directory:

   ```bash
   cp -r build/* ../static/
   ```

---

## Usage

- Open your browser and go to:  
  `http://127.0.0.1:8000/static/index.html`

- Upload your content file (Markdown `.md` or LaTeX `.tex`).
- Select output language and model or use automatic detection.
- Click **Generate Questions**.
- Download the generated `.tex` file when ready.

---

## Customization & Extensibility

- Language models and prompt templates can be adjusted in `backend/main.py`.
- Frontend styles and animations are located in `backend/static/style.css` and associated JavaScript files.
- Replace the university logos in `backend/static/logo.svg` or add your own assets.
- Background animation can be further customized or replaced with other effects.

---

## License

This project is licensed under the MIT License.

---

## Contact & Support

Feel free to open issues or contribute via GitHub repository:  
[https://github.com/sirnaser/modern-qg](https://github.com/sirnaser/modern-qg)

---

Thank you for using this project! 🌟
