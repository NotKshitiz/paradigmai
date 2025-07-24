import os
import subprocess
import sys
from pathlib import Path

def run_conversion(model_dir: str):
    # Get last folder name (e.g., "gemma")
    model_name = Path(model_dir).resolve().name

    # Final GGUF output path
    output_dir = Path.home() / "Downloads" / "Paradigm_Models"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{model_name}.gguf"

    # llama.cpp and convert.py path (assuming it's inside your project)
    llama_cpp_dir = os.path.join(os.path.dirname(__file__), "..", "llama.cpp")
    convert_script = os.path.join(llama_cpp_dir, "convert_hf_to_gguf.py")

    if not os.path.exists(convert_script):
        print("❌ convert.py not found in llama.cpp directory.")
        return None

    print(f"📦 Converting: {model_dir}")
    result = subprocess.run([
        sys.executable, convert_script,
        model_dir,
        "--outfile", str(output_path)
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if result.returncode == 0:
        print(f"✅ GGUF saved to: {output_path}")
        print(f"[DEBUG] Returning GGUF path: {output_path}")  # ✅ ADD THIS
        return str(output_path)  # ✅ AND THIS
    else:
        print("❌ Conversion failed:")
        print(result.stderr)
        return None
