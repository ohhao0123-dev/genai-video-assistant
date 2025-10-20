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

## ⚙️ Installation and Execution Steps (macOS/Linux)

Below is the full end-to-end setup process for running **GenAI Video Assistant** locally  
on macOS or Linux (tested on macOS M1 Pro/Max).

---

### 🧩 1. Clone the Repository

```bash
git clone https://github.com/ohhao0123-dev/genai-video-assistant.git
cd genai-video-assistant
```

---

### 🐍 2. Create and Manage Conda Environment

Set up a clean Python 3.11 environment for backend execution.

```bash
conda create -n genai-video-assistant python=3.11
conda activate genai-video-assistant
```

You can deactivate or remove the environment later if needed:

```bash
conda deactivate
conda env remove -n genai-video-assistant
```

---

### 🔧 3. Backend Setup (Python gRPC Server)

The backend hosts multiple AI agents (transcription, vision, report generation)  
and must be running before launching the desktop app.

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip wheel setuptools
pip install -r requirements.txt
```

---

### 🧠 4. Compile gRPC Proto Definitions

Generate the Python gRPC bindings from the `assistant.proto` file.

```bash
python -m grpc_tools.protoc   -I backend/proto   --python_out=backend/proto   --grpc_python_out=backend/proto   backend/proto/assistant.proto
```

If successful, this creates two files inside `backend/proto/`:
```
assistant_pb2.py
assistant_pb2_grpc.py
```

---

### ▶️ 5. Start the Python Backend Server

Run the backend (ensure no other process uses port 50051):

```bash
python server.py
```

✅ **Expected output:**
```
Python gRPC backend listening on :50051
```

Keep this terminal open while running the frontend (next step).

---

### 🧰 6. Frontend Setup (React + Tauri Desktop App)

Open a new terminal window (**do not close the backend**).

Install Node.js, npm, and pnpm via Conda:

```bash
conda install -c conda-forge nodejs
```

Verify installation:
```bash
node -v
npm -v
```

Install PNPM globally (for package management):
```bash
npm install -g pnpm
pnpm -v
```

---

### 🖥️ 7. Launch the Frontend Application

Navigate to the frontend folder and start the Tauri app:

```bash
cd frontend
pnpm install
pnpm tauri dev
```

✅ You should see the **GenAI Video Assistant** desktop window open.

---

### 🧪 8. Verify Functionality

In the app, enter an **absolute path** to a local `.mp4` video file.  
Example:

```
/Users/howell/Documents/Project Collation/genai-video-assistant/Imagine for 1 Minute.mp4
```

Try commands like:
- `Transcribe the video`
- `What objects are shown in the video?`
- `Create a PowerPoint with the key points`
- `Summarize and generate a PDF`

Check generated results in:
```
backend/outputs/
```

---

### ⚙️ 9. (Optional) Troubleshooting Commands

**Rebuild gRPC bindings**
```bash
python -m grpc_tools.protoc -I backend/proto --python_out=. --grpc_python_out=. backend/proto/assistant.proto
```

**Clean Rust and Frontend builds**
```bash
cd frontend/src-tauri
cargo clean
cd ..
pnpm tauri dev
```

**Update Node and Rust toolchains**
```bash
brew upgrade node rustup
rustup update
```

---

### 🧾 Environment Summary

| Component | Version (Recommended) | Description |
|------------|----------------------|--------------|
| **Python** | 3.11 | Backend (AI agents, gRPC server) |
| **Node.js** | ≥ 18.x | Frontend (React + Vite) |
| **Rust** | ≥ 1.75 | Tauri bridge and gRPC client |
| **PNPM** | ≥ 8.x | Frontend package manager |
| **Conda** | ≥ 24.x | Environment manager |

✅ **After setup, you’ll have:**
- 🧠 Local AI agents running via Python gRPC  
- ⚡ Interactive Tauri desktop UI via Rust + React  
- 📄 Outputs: Transcripts (.srt), Summaries (.pdf), Presentations (.pptx)  
- 💬 Persistent chat logs stored locally under  
  `~/.genai_video_assistant/history.json`

---

### 🧹 10. Cleanup (Optional)

When you’re done testing:

```bash
# Stop backend (Ctrl + C in terminal)
conda deactivate
conda env remove -n genai-video-assistant
```

---

### ✅ Quick Recap

| Step | Action | Command |
|------|---------|----------|
| 1 | Clone the repo | `git clone …` |
| 2 | Create Conda environment | `conda create -n genai-video-assistant python=3.11` |
| 3 | Install backend dependencies | `pip install -r requirements.txt` |
| 4 | Compile gRPC definitions | `python -m grpc_tools.protoc …` |
| 5 | Run backend server | `python server.py` |
| 6 | Install frontend dependencies | `pnpm install` |
| 7 | Launch desktop app | `pnpm tauri dev` |

---

🎉 **Your local GenAI Video Assistant app is now fully functional and running offline!**
