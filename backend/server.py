import sys, os
sys.path.insert(0, os.path.dirname(__file__))  # allow "from agents ..." and "from proto ..."

import grpc
from concurrent import futures
from pathlib import Path
from rich import print

from proto import assistant_pb2, assistant_pb2_grpc
from chat_store import ChatStore
from config import OUTPUT_DIR, WHISPER_MODEL, YOLO_MODEL
from agents.transcriber import TranscriptionAgent
from agents.vision import VisionAgent
from agents.generator import GenerationAgent

STORE = ChatStore(Path.home() / ".genai_video_assistant" / "history.json")

# Initialize local agents
TRANSCRIBER = TranscriptionAgent(model_size=WHISPER_MODEL)
VISION = VisionAgent(model_path=YOLO_MODEL)
GENERATOR = GenerationAgent()


class AssistantService(assistant_pb2_grpc.AssistantServicer):
  def ProcessQuery(self, request, context):
    from pathlib import Path
    import shutil
    session_id = request.session_id or "default"
    query = (request.query or "").lower().strip()
    video = request.video_path or ""

    # 1) Basic validation
    if not video:
      return assistant_pb2.QueryReply(
        session_id=session_id,
        needs_clarification=True,
        clarification_prompt="Please provide the absolute path to a local .mp4 file."
      )
    if not Path(video).exists():
      return assistant_pb2.QueryReply(
        session_id=session_id,
        needs_clarification=True,
        clarification_prompt=f"Video file not found: {video}"
      )
    if shutil.which("ffmpeg") is None:
      return assistant_pb2.QueryReply(
        session_id=session_id,
        needs_clarification=True,
        clarification_prompt="FFmpeg not detected. Please install it using: brew install ffmpeg"
      )

    STORE.append(session_id, "user", request.query)

    needs_clar, clar_prompt = False, ""
    answer, artifacts = "", []

    try:
      if "transcrib" in query:
        # 2) Transcription
        result = TRANSCRIBER.run(video)
        answer = (result.get("transcript") or "")[:2000]
        if result.get("srt"):
          artifacts.append(result["srt"])

      elif "object" in query or "what do you see" in query:
        # 3) Object detection
        result = VISION.run(video)
        objs = ", ".join([f"{k}({v})" for k, v in sorted(result["objects"].items(), key=lambda x: -x[1])])
        answer = f"Detected objects: {objs or 'none'}"
        if result.get("graphs_detected"):
          answer += "\nPossible charts or graphs detected on screen."

      elif "graph" in query:
        # 4) Graph detection heuristic
        result = VISION.run(video)
        answer = "Charts or graphs " + ("likely present." if result.get("graphs_detected") else "not detected.")

      elif "powerpoint" in query or "ppt" in query:
        # 5) Generate PowerPoint requires content
        history_text = "\n".join([f"{m['role']}: {m['content']}" for m in STORE.get(session_id)])
        if not history_text.strip():
          needs_clar = True
          clar_prompt = "I need content first (for example, run 'Transcribe the video'). Do you want to transcribe now?"
        else:
          out = GENERATOR.run(history_text, str(OUTPUT_DIR), kind="pptx")
          answer = "Generated PowerPoint with key points."
          artifacts.append(out["report"])

      elif "pdf" in query or "summarize" in query:
        # 6) Generate PDF requires content
        history_text = "\n".join([f"{m['role']}: {m['content']}" for m in STORE.get(session_id)])
        if not history_text.strip():
          needs_clar = True
          clar_prompt = "I need content first (for example, run 'Transcribe the video'). Do you want to transcribe now?"
        else:
          out = GENERATOR.run(history_text, str(OUTPUT_DIR), kind="pdf")
          answer = "Generated PDF summary."
          artifacts.append(out["report"])

      else:
        needs_clar = True
        clar_prompt = "Did you mean: 'Transcribe the video', 'What objects are shown', 'Create a PowerPoint', or 'Summarize to PDF'?"

      if answer:
        STORE.append(session_id, "assistant", answer)

      return assistant_pb2.QueryReply(
        session_id=session_id,
        answer=answer,
        artifacts=artifacts,
        needs_clarification=needs_clar,
        clarification_prompt=clar_prompt
      )

    except Exception as e:
      # 7) Catch-all fallback: return error message to frontend
      err = f"Backend processing error: {type(e).__name__} — {e}"
      print(f"[red]{err}[/red]")
      return assistant_pb2.QueryReply(
        session_id=session_id,
        needs_clarification=True,
        clarification_prompt=err
      )


  def GenerateReport(self, request, context):
    session_id = request.session_id or "default"
    fmt = request.format.lower()
    history_text = "\n".join([f"{m['role']}: {m['content']}" for m in STORE.get(session_id)])
    out = GENERATOR.run(history_text, str(OUTPUT_DIR), kind=fmt)
    return assistant_pb2.ReportReply(session_id=session_id, path=out["report"])

  def GetHistory(self, request, context):
    import json
    hist = STORE.get(request.session_id or "default")
    return assistant_pb2.HistoryReply(
      session_id=request.session_id or "default",
      history_json=json.dumps(hist)
    )


# =========================
# gRPC Server Launcher
# =========================
def serve():
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
  assistant_pb2_grpc.add_AssistantServicer_to_server(AssistantService(), server)
  server.add_insecure_port("[::]:50051")
  print("[green]Python gRPC backend listening on :50051[/green]")
  server.start()
  server.wait_for_termination()


if __name__ == "__main__":
  serve()
