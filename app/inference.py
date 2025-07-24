from llama_cpp import Llama
import os
from functools import lru_cache


def detect_nvidia_gpu():
    try:
        import torch
        return torch.cuda.is_available()
    except ImportError:
        return False


@lru_cache(maxsize=1)
def load_model(gguf_path: str, n_gpu_layers: int = 32) -> Llama:
    return Llama(
        model_path=gguf_path,
        n_gpu_layers=n_gpu_layers,
        n_ctx=2048,
        temperature=0.7,
        top_p=0.95,
        repeat_penalty=1.1,
        verbose=False
    )


def get_prompt_and_stop(prompt: str, metadata: dict) -> tuple[str, list[str]]:
    model_type = metadata.get("model_type", "").lower()
    model_name = metadata.get("model_name", "").lower()
    chat_format = metadata.get("file_metadata", {}).get("chat_template", "").lower()

    chat_keywords = ["chat", "instruct", "alpaca", "mistral", "llama", "wizard", "orca"]
    is_chat_model = any(
        kw in model_type or kw in model_name or kw in chat_format
        for kw in chat_keywords
    )

    if is_chat_model:
        formatted_prompt = f"""### System:
You are a helpful assistant.

### User:
{prompt.strip()}

### Assistant:"""
        stop_tokens = ["### User:", "### System:", "</s>", "<|end|>"]
    else:
        formatted_prompt = prompt.strip()
        stop_tokens = ["</s>"]

    return formatted_prompt, stop_tokens


def run_inference_stream(gguf_path: str, prompt: str):
    if not os.path.exists(gguf_path):
        yield "[ERROR] Model path does not exist."
        return

    if detect_nvidia_gpu():
        device = "🧠 Running on GPU (NVIDIA)...\n"
        n_gpu_layers = 32
    else:
        device = "🧠 Running on CPU...\n"
        n_gpu_layers = 0

    print(device)
    yield device

    print("📤 Model is generating response...\n")
    yield "📤 Model is generating response...\n\n"

    # Load the model (cached if same path used before)
    try:
        llm = load_model(gguf_path, n_gpu_layers)
    except Exception as e:
        err_msg = f"[ERROR] Failed to load model: {str(e)}"
        print(err_msg)
        yield err_msg
        return

    # Prepare prompt and stop tokens
    try:
        safe_prompt, stop_tokens = get_prompt_and_stop(prompt, llm.metadata)
    except Exception as e:
        err_msg = f"[ERROR] Invalid model metadata: {str(e)}"
        print(err_msg)
        yield err_msg
        return

    try:
        previous_token = ""
        for i, output in enumerate(llm(safe_prompt, stream=True, max_tokens=1024, stop=stop_tokens)):
            token = output["choices"][0]["text"]

            # Insert space if two tokens are jammed together
            if previous_token and not previous_token.endswith((" ", "\n")) and not token.startswith((" ", "\n", ".", ",", "!", "?", ":", ";")):
                yield " "
                print(" ", end='')

            yield token
            print(token, end='', flush=True)
            previous_token = token

            # Safety cap
            if i >= 1200:
                yield "\n[INFO] Output truncated to prevent runaway generation."
                break

    except Exception as e:
        err_msg = f"[ERROR] Inference failed: {str(e)}"
        print(err_msg)
        yield err_msg
