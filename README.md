# 🎥 GenAI Video Assistant (Offline Local AI Desktop App)

> **Test Assignment — GenAI Software Solutions Engineer**  
> Candidate: **Howell Ho**  
> Platform: **macOS M1 Pro/Max**  
> Date: **2025**

---

## 📘 Overview

**GenAI Video Assistant** is a fully **offline desktop application** that enables users to **analyze, summarize, and query local video files** through natural language.

The system uses a **multi-agent architecture** running locally on Python with **gRPC**, connected to a **React + Tauri (Rust)** desktop interface.  
It processes short videos (~1 minute each), extracts speech, recognizes visual objects, detects charts, and generates automated **PDF/PPT reports** — all without any internet access or cloud APIs.

---

## 🧠 Core Objectives

✅ Operate **entirely offline** using local models  
✅ Support **natural language queries** for video analysis  
✅ Provide **clarification prompts** for ambiguous inputs  
✅ Maintain **persistent chat history** between sessions  
✅ Generate **PDF/PPTX summaries** of insights  
✅ Use **modular, agent-based architecture**

---

## 🏗️ System Architecture

```
┌────────────────────────────────────────────────────────────────────────────┐
│ Frontend (Tauri)                                                           │
│ ┌──────────────────────────────┐     ┌──────────────────────────────┐       │
│ │ React Chat UI (App.tsx)      │ →   │ Rust Bridge (main.rs, tonic)│       │
│ └──────────────────────────────┘     └──────────────────────────────┘       │
│ ↑                                                                        │
└─────────────┼───────────────────────────┼────────────────────────────────┘
              │ gRPC (localhost:50051)
              ▼
┌──────────────────────────────────────────────────────────────┐
│ Python Backend (Agents)                                      │
│--------------------------------------------------------------│
│ • TranscriptionAgent → Speech-to-text (Whisper)              │
│ • VisionAgent → Object / Graph Detection (YOLOv8)            │
│ • GenerationAgent → PDF & PPTX Generation                    │
│ • ChatStore → Persistent JSON History                        │
└──────────────────────────────────────────────────────────────┘
              │
              ▼
         Local AI Models
     (Whisper · YOLOv8 · ReportLab · PPTX)
```

---

## 🧩 Agent Responsibilities

| Agent | Description | Framework |
|--------|--------------|------------|
| **TranscriptionAgent** | Converts speech to text using [`faster-whisper`](https://github.com/guillaumekln/faster-whisper); outputs `.srt` subtitles | Whisper (CTranslate2 backend) |
| **VisionAgent** | Detects objects and possible charts in frames | Ultralytics YOLOv8 |
| **GenerationAgent** | Summarizes and creates reports (PDF, PPTX) | ReportLab · python-pptx |
| **ChatStore** | Persists chat history per session in local JSON | Built-in JSON I/O |

---

## 📁 Repository Structure

```
genai-video-assistant/
├─ backend/
│  ├─ agents/
│  │  ├─ transcriber.py        # Whisper transcription
│  │  ├─ vision.py             # YOLOv8 object detection
│  │  ├─ generator.py          # PDF/PPTX generation
│  │  └─ base.py               # Base agent class
│  ├─ proto/assistant.proto    # gRPC definitions
│  ├─ server.py                # gRPC backend orchestrator
│  ├─ chat_store.py            # Persistent chat manager
│  ├─ config.py                # Model paths & configuration
│  ├─ requirements.txt
│  └─ outputs/                 # Generated outputs
│
├─ frontend/
│  ├─ src/
│  │  ├─ App.tsx               # Main React UI
│  │  └─ main.tsx
│  ├─ src-tauri/
│  │  ├─ src/main.rs           # Rust tonic bridge
│  │  ├─ build.rs              # Builds assistant.proto
│  │  └─ Cargo.toml
│  ├─ index.html
│  ├─ package.json
│  └─ pnpm-lock.yaml
│
└─ README.md
```

---

## 🧰 Technology Stack

| Layer | Tools / Libraries | Purpose |
|-------|--------------------|----------|
| **Frontend** | React 18 · TypeScript · Vite · Tauri 2 | Lightweight UI and packaging |
| **Bridge** | Rust · tonic · tokio · serde_json | Secure IPC & gRPC bridge |
| **Backend** | Python 3.11 · gRPC · faster-whisper · YOLOv8 · ReportLab | Local inference |
| **Storage** | JSON (`~/.genai_video_assistant/history.json`) | Persistent history |
| **Platform** | macOS (M1/M2/M3) | Full local runtime |

---

## 💾 Local Model Inference

| Model | Function | Backend | Notes |
|--------|-----------|----------|-------|
| **Whisper (small)** | Speech-to-text | CTranslate2 | Optimized for Apple Silicon |
| **YOLOv8n** | Object / Scene detection | Ultralytics | CPU/MPS optimized |
| **ReportLab** | PDF generation | Local | Fully offline |
| **python-pptx** | PPTX generation | Local | Fully offline |
| *(Optional)* PaddleOCR | OCR / chart text recognition | Local | Optional on macOS M1 |

> 🧠 Once models are downloaded, everything runs **completely offline**.

---

## ⚙️ Setup Instructions (macOS)

### 1️⃣ Install Dependencies
```bash
xcode-select --install
brew install ffmpeg protobuf pnpm rustup
rustup-init
```

### 2️⃣ Backend Setup
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip wheel setuptools
pip install -r requirements.txt

# Compile protobufs
python -m grpc_tools.protoc -I proto --python_out=. --grpc_python_out=. proto/assistant.proto

# Start backend
python server.py
```
✅ You should see:
```
Python gRPC backend listening on :50051
```

### 3️⃣ Frontend Setup
```bash
cd frontend
pnpm install
pnpm tauri dev
```
This opens the **GenAI Video Assistant** desktop window.

---

## 💡 Usage Guide

### Select a Local Video File
Example:  
`/Users/howell/Documents/Project/genai-video-assistant/ImagineFor1Minute.mp4`

### Example Queries
- “Transcribe the video.”
- “What objects are shown?”
- “Are there any graphs?”
- “Create a PowerPoint with key points.”
- “Summarize and generate a PDF report.”

### Output Locations
| Type | Location |
|------|-----------|
| `.srt` subtitles | Same folder as video |
| `summary.pdf` / `summary.pptx` | `backend/outputs/` |
| Chat history | `~/.genai_video_assistant/history.json` |

---

## 🧠 Human-in-the-loop Clarification

If a user request is incomplete or unclear, the backend prompts:
> **Clarification:** “Need a transcript first — run *‘Transcribe the video’*?”

This ensures **logical workflow order** and **error prevention**.

---

## 🔒 Offline Design Compliance

All computation runs **locally**:
- No cloud APIs or online endpoints  
- All model weights cached locally  
- gRPC restricted to `localhost`

**Privacy Guaranteed:**  
All data, transcripts, and outputs remain on the user’s device.

---

## 🧭 Example Interaction Flow

```text
User: Transcribe the video.
→ TranscriptionAgent: transcript + .srt generated

User: What objects are shown?
→ VisionAgent: person(18), laptop(4), screen(1), possible chart detected

User: Summarize and generate a PDF.
→ GenerationAgent: summary.pdf created under backend/outputs/
```

---

## 🛠️ Troubleshooting

| Issue | Cause | Fix |
|--------|--------|------|
| `protoc not found` | Missing compiler | `brew install protobuf` |
| `Command process_query not found` | Tauri not registered | Add to `generate_handler![]` in `main.rs` |
| No output | Backend not running | Ensure Python backend shows connection |
| PaddleOCR fails on M1 | Incompatible build | Remove it from `requirements.txt` |

---

## 🔄 Build & Packaging

**Development**
```bash
pnpm tauri dev
```

**Production**
```bash
pnpm tauri build
```
Output:  
`frontend/src-tauri/target/release/bundle/macos/GenAI Video Assistant.app`

---

## 🧮 Clarification Logic Summary

| User Intent | Routed Agent | Clarification |
|--------------|---------------|----------------|
| Transcription | TranscriptionAgent | — |
| Object Detection | VisionAgent | — |
| Generate PDF/PPT | GenerationAgent | Needs transcript first |
| Unknown command | — | Suggest valid options |

---

## 📊 Performance (M1 Pro)

| Task | Duration | Model | Remarks |
|-------|-----------|--------|----------|
| Transcription (1-min video) | 5–8s | Whisper-small-int8 | Real-time |
| Object Detection | 2–4s | YOLOv8n | Optimized |
| PDF/PPT Generation | < 1s | ReportLab / PPTX | Instant |

---

## 🧩 Architecture Modules

| Module | File | Role |
|--------|------|------|
| gRPC Definitions | `backend/proto/assistant.proto` | Defines RPC methods |
| Backend Service | `backend/server.py` | Dispatches to agents |
| Rust Bridge | `src-tauri/src/main.rs` | Handles IPC calls |
| Frontend UI | `frontend/src/App.tsx` | Chat interface |
| Persistence | `chat_store.py` | Local JSON history |

---

## 🚀 Future Improvements

| Category | Enhancement |
|-----------|--------------|
| Architecture | Split agents into micro-services |
| Summarization | Integrate local LLM (Llama.cpp / Mistral) |
| Graph Detection | Add PaddleOCR + CNN classifier |
| UX | Drag-drop uploads, progress bars, previews |
| Cross-Platform | Add Windows & Linux builds |
| Automation | Auto-launch backend process |

---

## 📈 Status Summary

✅ **Working**
- Offline transcription & object detection  
- gRPC bridge (Python ↔ Rust)  
- Natural language chat UI  
- PDF/PPT generation  
- Persistent chat history  

⚠️ **Not Implemented**
- OCR chart recognition  
- Cloud fallback  
- Multi-threaded orchestration  

---

## 🧾 License

**MIT License © 2025 Howell Ho**  
This project was created as part of the **GenAI Software Solutions Engineer Test Assignment**.  
You may freely use and adapt it for educational or demonstration purposes.

---

## 🧩 Summary

The **GenAI Video Assistant** demonstrates a **complete offline AI system** integrating:

- Agentic modular architecture  
- Local inference with Whisper & YOLO  
- Cross-language orchestration (React → Rust → Python)  
- Explainable, persistent, and privacy-safe workflows  

✅ **Key Takeaway:**  
A modular, transparent, and offline **GenAI architecture** for practical, human-in-the-loop video understanding.
