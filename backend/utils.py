from llama_cpp import Llama
import os
import re
import uuid


def list_models(models_dir="models"):
    models = []
    if not os.path.exists(models_dir):
        return models
    for file in os.listdir(models_dir):
        if file.endswith(".gguf"):
            models.append(file)
    return models


def run_model(model_path: str, prompt: str, max_tokens: int = 1024) -> str:
    llm = Llama(
        model_path=model_path,
        n_ctx=8192,
        n_threads=8,
        n_gpu_layers=0,
        verbose=False
    )
    
    output = llm(prompt, max_tokens=max_tokens, stop=["</s>", "###"])
    return output["choices"][0]["text"].strip()



def call_model_selector(model_path, prompt, model_names):
    model_list_str = "\n".join([f"- {name}" for name in model_names])
    selector_prompt = f"""
You are an expert model selector for educational content.

Given the following list of available models:
{model_list_str}

Choose the best model for the provided input and ONLY return its exact filename.

Input Description:
{prompt}
"""

    return run_model(model_path, selector_prompt)


def extract_text_from_tex(tex_content):
    content = re.sub(r"\\begin\{.*?\}.*?\\end\{.*?\}", "", tex_content, flags=re.DOTALL)
    content = re.sub(r"\\[a-zA-Z]+\*?(?:\[[^\]]*\])?(?:\{[^\}]*\})?", "", content)
    content = re.sub(r"\%.*", "", content)
    content = re.sub(r"\s+", " ", content)
    return content.strip()


def build_prompt_from_content(content, language="fa"):
    prompt = f"""
You are an advanced educational AI assistant.

Given the following lesson content in Markdown format, generate 5 to 10 diverse and deep questions, focusing on mathematical and computer science concepts.

Question types can include:
- Multiple Choice
- Fill in the Blank
- Short Answer
- Descriptive Questions
- Creative / Logical reasoning questions

Please ensure:
- The questions are based on the *exact content* provided.
- The questions are challenging yet clear.
- Answers are detailed and accurate.
- Include references to the content when possible.

Output Format:
- Write the questions and answers in LaTeX.
- Use clear sectioning:
  \\section*{{Questions}}
  (list of questions)
  \\newpage
  \\section*{{Answers}}
  (list of answers with reference)

Target Output Language: {'Persian' if language == 'fa' else 'English'}

Content:
\"\"\"
{content}
\"\"\"
"""
    return prompt


def build_prompt_from_examples(example_text, language="fa"):
    prompt = f"""
You are an expert question generator AI specialized in academic domains.

Given the following sample exam questions in LaTeX, analyze the style and structure, then generate 5 to 10 similar but *new* questions.

Ensure:
- New questions are original, not duplicates.
- They follow the same topic, difficulty, and style.
- Answers must be complete, correct, and included.
- Reference any patterns observed from the examples.

Output Format:
- Provide output in LaTeX.
- Use clear sectioning:
  \\section*{{Questions}}
  (new questions)
  \\newpage
  \\section*{{Answers}}
  (answers)

Target Output Language: {'Persian' if language == 'fa' else 'English'}

Sample TeX Questions:
\"\"\"
{example_text}
\"\"\"
"""
    return prompt
