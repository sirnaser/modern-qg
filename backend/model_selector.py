from llama_cpp import Llama
from multiprocessing import cpu_count

META_MODEL_PATH = "models/DeepSeek-R1-0528-Qwen3-8B-Q4_K_M.gguf"

# Use the meta-model to select the best model key for given content
def choose_model(content: str, available_models):
    
    # Load the meta-model used for selecting the best specialized model
    _meta_llm = Llama(
        model_path=META_MODEL_PATH,
        n_ctx=2048,
        n_threads=min(8, cpu_count()),
        temperature=0.2,
        system_prompt="You are an AI assistant that chooses the most suitable specialised model.",
    )

    prompt = (
        f"Available specialised models: {', '.join(available_models)}.\n"
        f"Given the academic content below, reply **only** with the single model name that is most appropriate.\n"
        f"CONTENT:\n{content}\n"
        f"MODEL:"
    )
    ans = _meta_llm(prompt)["choices"][0]["text"].strip().lower()
    return ans if ans in available_models else "deepseek"
