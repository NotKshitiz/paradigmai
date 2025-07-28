# Paradigm – GPU-Aware ML Inference Engine

Paradigm is a plug-and-play desktop application that enables **local inference of large language models (LLMs)** using **GPU or CPU fallback**. It supports automatic conversion of Hugging Face models to **GGUF** format and leverages **llama.cpp** for fast, low-latency generation.

---

## Ideology

> **Paradigm** was built with a simple belief:  
> _Local inference should be accessible, efficient, and hardware-aware — not cloud-dependent or locked behind APIs._

In an era where LLMs are increasingly cloud-hosted and resource-intensive, Paradigm takes a developer-first approach to make **on-device inference** possible for anyone with a CPU or modest GPU. It's a tool for:
- Builders who want full control over inference.
- Researchers experimenting with quantization or model routing.
- Hobbyists who want to run models offline, privately, and affordably.

Paradigm is aimed to be modular, open, and optimized to run on real-world hardware — **even on laptops with 4–6GB of VRAM**.

> **Build once. Run anywhere. No vendor lock-in.*


## Features

- **Auto-converts Hugging Face LLMs** (e.g., LLaMA, Mistral) to `.gguf` format using a simple UI
- **GPU/CPU-aware inference** with automatic VRAM detection and device fallback
- **Tokenizer auto-detection** for compatible text generation
- Simple, fast UI
- Supports quantized models (e.g., `Q4_K_M`, `Q6_K`)
- Future support for **ONNX export** and inference
- Designed to work offline — ideal for local, private inference

---


## Upcoming Features

- **ONNX Export + Inference Support**  
  Convert `.bin`/`.safetensors` models into ONNX for accelerated inference on both NVIDIA and AMD GPUs.

- **Custom Model Settings UI**  
  Set temperature, top-p, context length, quantization level, and stop tokens via a config panel.

- **Multi-Model Switcher**  
  Load and swap between multiple GGUF/ONNX models with a dropdown interface.

- **Inference Performance Monitor**  
  View real-time VRAM usage, inference latency, and token generation stats.

- **One-Click Model Installer**  
  Paste a Hugging Face model link — Paradigm downloads and prepares it for local use.

- **Portable Builds for macOS and Linux**  
  Distributable `.dmg` and `.AppImage` packages with built-in backend.

---

##  Setup Instructions

### Download the application from Releases section v1.0.0 (a little buggy and scrappy)
---

##  Author
Kshitiz Kumar

##  License

Paradigm is dual-licensed under the terms of the [Apache License 2.0](http://www.apache.org/licenses/LICENSE-2.0) — at your option.
This file may not be copied, modified, or distributed except according to those terms.
