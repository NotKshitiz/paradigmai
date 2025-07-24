from fastapi import FastAPI
from app.models import Structure, Input_Inference
from app.convert_to_gguf import convert_to_gguf
from app.inference import run_inference_stream
from fastapi.responses import StreamingResponse
import os

app = FastAPI()

# Global variable to store model path (converted or already .gguf)
converted_model_path = None


@app.post("/path")
def gguf_convert(input: Structure):
    global converted_model_path
    try:
        path = input.path

        # ✅ If it's a folder, check for .gguf files
        if os.path.isdir(path):
            gguf_files = [f for f in os.listdir(path) if f.endswith(".gguf")]
            if gguf_files:
                # Use the first .gguf file found
                converted_model_path = os.path.join(path, gguf_files[0])
                print(f"✅ Found existing GGUF model: {converted_model_path}")
            else:
                print("🔄 No GGUF file found in folder. Proceeding to convert...")
                converted_model_path = convert_to_gguf(path)
        elif path.endswith(".gguf"):
            converted_model_path = path
            print(f"✅ Model is already in GGUF format: {converted_model_path}")
        else:
            print("🔄 Provided path is not .gguf or folder — assuming it's a model to convert.")
            converted_model_path = convert_to_gguf(path)

        return {
            "message": "Model ready for inference.",
            "gguf_model_path": converted_model_path
        }

    except Exception as e:
        print(f"GGUF conversion error: {e}")
        return {"error": str(e)}


@app.post("/inference")
def infer(input: Input_Inference):
    global converted_model_path
    try:
        if not converted_model_path:
            return StreamingResponse(iter(["data: No model converted yet.\n\n"]), media_type="text/event-stream")

        def token_stream():
            for token in run_inference_stream(converted_model_path, input.input):
                yield f"data: {token}\n\n"

        return StreamingResponse(token_stream(), media_type="text/event-stream")

    except Exception as e:
        print(f"Inference error: {e}")
        return StreamingResponse(iter([f"data: Error: {str(e)}\n\n"]), media_type="text/event-stream")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
