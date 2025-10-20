from .base import BaseAgent
from pathlib import Path
from typing import Dict, Any
from faster_whisper import WhisperModel

class TranscriptionAgent(BaseAgent):
  name = "transcriber"

  def __init__(self, device: str = "auto", model_size: str = "small"):
    # CTranslate2 backend; fast on M1/M2/M3
    self.model = WhisperModel(model_size, device=device, compute_type="int8")

  def run(self, video_path: str) -> Dict[str, Any]:
    segments, info = self.model.transcribe(video_path, beam_size=1)
    text = []
    srt_lines = []
    for i, seg in enumerate(segments, start=1):
      text.append(seg.text.strip())
      srt_lines.append(
        f"""{i}
{self._fmt(seg.start)} --> {self._fmt(seg.end)}
{seg.text.strip()}

"""
      )
    transcript = "\n".join(text).strip()
    srt_path = Path(video_path).with_suffix(".srt")
    srt_path.write_text("".join(srt_lines))
    return {"transcript": transcript, "srt": str(srt_path)}

  @staticmethod
  def _fmt(sec: float) -> str:
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    ms = int((sec - int(sec)) * 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"
