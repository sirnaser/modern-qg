import os
from datetime import datetime
from llama_cpp import Llama


def get_available_models(models_dir="models"):
    """
    Return a list of all available .gguf model filenames in the specified directory.
    """
    return [f for f in os.listdir(models_dir) if f.endswith(".gguf")]


def load_model(model_path):
    """
    Load a GGUF model using llama.cpp with reasonable default parameters.
    """
    return Llama(
        model_path=model_path,
        n_ctx=2048,
        n_threads=6,
        n_batch=64,
        verbose=False,
    )


def build_prompt_from_markdown(content, language="fa"):
    """
    Build a question generation prompt from markdown lesson content.
    Language can be 'fa' for Persian or 'en' for English.
    """

    if language == "fa":
        return f"""
شما یک دستیار دانشگاهی متخصص در دانشکده علوم ریاضی هستید.
وظیفه‌ی شما تولید مجموعه‌ای از پرسش‌های عمیق، خلاقانه و دقیق بر اساس محتوای آموزشی زیر (فرمت markdown) است.

خروجی شما باید شامل ۱۰ تا ۱۲ سؤال در فرمت LaTeX باشد که موضوعات مهم محتوا را پوشش دهند.
انواع سوالات شامل:
- چند گزینه‌ای
- جای خالی
- پاسخ کوتاه
- تشریحی
- سوالات خلاقانه و مفهومی جدید (در صورت امکان)

پاسخ تمام سوالات را به‌صورت دقیق و کامل و با ارجاع به بخش‌های مربوطه از محتوا در صفحات جداگانه بیاورید.

زبان سوالات و پاسخ‌ها: فارسی

محتوا:
--------------------
{content}
--------------------

فقط خروجی LaTeX تولید کنید. از \\documentclass شروع کنید.
"""
    else:
        return f"""
You are an academic assistant in the Faculty of Mathematical Sciences.
Your task is to generate a set of deep, creative, and precise exam questions based on the following lesson content (in markdown format).

Your output must include 10 to 12 LaTeX-formatted questions that reflect key concepts and reasoning skills.

Include a mix of question types:
- Multiple choice
- Fill-in-the-blank
- Short answer
- Open-ended or creative types when suitable

At the end, provide full, well-explained answers with references to the lesson content on separate pages.

Language: English

Lesson Content:
--------------------
{content}
--------------------

Only return valid LaTeX starting with \\documentclass.
"""


def build_prompt_from_tex(sample_question_tex, language="fa"):
    """
    Build a question generation prompt from LaTeX sample questions.
    """

    if language == "fa":
        return f"""
شما یک دستیار دانشگاهی در دانشکده علوم ریاضی هستید.

در ادامه یک نمونه سوال به زبان LaTeX ارائه شده است. بر اساس آن، ۱۰ تا ۱۲ سوال جدید، مشابه و خلاقانه طراحی کنید.

سوالات باید از نظر سطح و موضوع مشابه باشند اما عیناً تکرار نشوند.
از انواع مختلف سوالات استفاده کنید (چندگزینه‌ای، جای‌خالی، پاسخ کوتاه، ...).
پاسخ تمام سوالات را نیز به صورت کامل در صفحات جداگانه بیاورید.

زبان سوالات و پاسخ‌ها: فارسی

نمونه سوال:
---------------------
{sample_question_tex}
---------------------

فقط خروجی LaTeX تولید کنید و آن را با \\documentclass شروع کنید.
"""
    else:
        return f"""
You are an academic assistant at the Faculty of Mathematical Sciences.

Below is a sample LaTeX exam question. Based on this example, create 10–12 new, creative and similarly-styled questions.

Questions should be similar in topic and complexity but not identical.
Use a variety of question types (MCQ, short answer, fill-in-the-blank, etc.)
Include answers to all questions, clearly separated and placed on new pages.

Language: English

Sample Question:
---------------------
{sample_question_tex}
---------------------

Start your output with \\documentclass and return only valid LaTeX.
"""


def build_model_selector_prompt(content, model_list):
    """
    Create an English prompt for selecting the most suitable model from a list.
    """
    model_names = ", ".join(model_list)
    return f"""
You are a general-purpose language model tasked with selecting the best model for generating exam questions from university-level educational content.

Available models: {model_names}

Your task:
- Analyze the provided content.
- Determine which model is most suitable for generating accurate, creative, and deep questions based on this input.
- Choose the model that best fits the content type, subject, and complexity.

ONLY respond with the exact model name from the list above. Do not include any explanation, extra text, or formatting.

Content:
--------------------
{content}
--------------------
"""


def run_model_selector(content, model_dir="models"):
    """
    Run a language model (preferably DeepSeek) to determine the best model from a list.
    """
    available_models = get_available_models(model_dir)
    if not available_models:
        raise RuntimeError("No models found in the models directory.")

    preferred_model = next((m for m in available_models if "deepseek" in m.lower()), available_models[0])
    model_path = os.path.join(model_dir, preferred_model)

    llm = load_model(model_path)
    prompt = build_model_selector_prompt(content, available_models)
    response = llm(prompt, max_tokens=20)

    response_text = response["choices"][0]["text"].strip()
    if response_text in available_models:
        return response_text
    else:
        return preferred_model


def save_tex_file(content, suffix=""):
    """
    Save LaTeX content to a timestamped .tex file in the output directory.
    """
    if not os.path.exists("output"):
        os.makedirs("output")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"questions{suffix}_{timestamp}.tex"
    file_path = os.path.join("output", filename)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    return file_path
