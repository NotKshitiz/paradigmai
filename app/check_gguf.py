import json
import os

def is_llama_family(model_path: str) -> bool:
    config_path = os.path.join(model_path, "config.json")
    if not os.path.exists(config_path):
        return False

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
    except json.JSONDecodeError:
        return False

    model_type = config.get("model_type", "").lower()
    architectures = [arch.lower() for arch in config.get("architectures", [])]

    gguf_families = [
    "llama",       # LLaMA 1/2/3 (Meta)
    "mistral",     # Mistral-7B
    "mixtral",     # Mixtral-8x7B, Mixtral-8x22B
    "falcon",      # Falcon-7B (40B partially supported)
    "gptj",        # GPT-J (EleutherAI)
    "gptneox",     # GPT-NeoX (Pythia, RedPajama)
    "mpt",         # MPT (MosaicML)
    "bloom",       # BLOOM (BigScience)
    "stablelm",    # StableLM (Stability AI)
    "qwen",        # Qwen-1.5 (Alibaba)
    "gemma",       # Gemma (Google)
    "starcoder",   # StarCoder (BigCode)
    "baichuan",    # Baichuan-7B/13B
    "codellama",   # CodeLlama (Meta)
    "guanaco",     # LLaMA fine-tunes (e.g., Guanaco-7B)
    "rwkv"         # RWKV (requires custom conversion)
] 

    gguf_keywords = gguf_families  

    if model_type in gguf_families:
        return True

    for arch in architectures:
        if any(keyword in arch for keyword in gguf_keywords):
            return True

    return False
