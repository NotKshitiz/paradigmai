import argparse
import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
from app.run_conversion import run_conversion  # your actual converter function
from app.check_gguf import is_llama_family    # your model family checker

# ✅ Reusable function for FastAPI and CLI
def convert_to_gguf(model_path: str) -> str:
    if not os.path.exists(model_path):
        raise FileNotFoundError("Model folder does not exist.")

    if is_llama_family(model_path):
        print("GGUF-compatible model detected. Starting conversion...")
        gguf_path = run_conversion(model_path)
        print(f"[DEBUG] Returning GGUF path: {gguf_path}")
        return gguf_path
    else:
        raise ValueError("⚠️ This model is not supported for GGUF conversion.")

# ✅ CLI wrapper
def main():
    parser = argparse.ArgumentParser(description="GGUF Auto Converter")
    parser.add_argument("model_path", help="Path to the original Hugging Face model folder")
    args = parser.parse_args()
    try:
        gguf_path = convert_to_gguf(args.model_path)
        print(f"✅ Conversion complete. GGUF model saved at: {gguf_path}")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
