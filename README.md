# 🧠 GenAI Video Assistant (Offline Desktop Application)

> **Test Assignment — GenAI Software Solutions Engineer**

A lightweight **offline desktop AI application** built with **React + Tauri + Rust + Python (gRPC)**.  
The system analyzes local video files, performs **speech transcription**, **object detection**, and **report generation** (PDF & PowerPoint) — entirely **without any cloud dependency**.

---

## 🚀 Overview

| Component | Technology | Purpose |
|------------|-------------|----------|
| **Frontend (UI)** | React + Tauri | Chat-style interface for querying and managing video insights |
| **Bridge** | Rust (tonic gRPC client) | Connects the desktop UI with the local Python backend |
| **Backend (Core)** | Python (gRPC server) | Multi-agent architecture for video transcription, vision analysis, and report generation |
| **Inference Models** | Whisper (faster-whisper) · YOLOv8 · ReportLab / PPTX | Fully local model inference optimized for CPU/MPS |
| **Runtime** | 100% Offline | Runs locally on macOS (M1/M2/M3), no cloud API calls |

---

## 🧩 Features

- 🎬 **Video Upload** — Select and process local `.mp4` files.
- 💬 **Natural Language Interaction**
  - “Transcribe the video.”
  - “What objects are shown?”
  - “Are there any graphs in the video?”
  - “Create a PowerPoint with the key points.”
  - “Summarize and generate a PDF report.”
- 👁️ **Computer Vision Agent (YOLOv8)** — Detects objects and estimates presence of charts/graphs.
- 🔊 **Transcription Agent (Whisper)** — Converts audio to text and generates `.srt` subtitles.
- 📄 **Generation Agent** — Produces summary reports in both **PDF** and **PPTX**.
- 🔁 **Persistent Chat History** — Saves conversation context locally (JSON).
- 🧠 **Human-in-the-loop Clarifications** — Prompts for disambiguation when a request is incomplete.
- 🔒 **Completely Offline** — All inference runs locally, no external or public APIs.

---

## 🏗️ Architecture

