from .base import BaseAgent
from typing import Dict, Any
from ultralytics import YOLO
import cv2

class VisionAgent(BaseAgent):
  name = "vision"

  def __init__(self, model_path: str = "yolov8n.pt"):
    self.model = YOLO(model_path)

  def run(self, video_path: str) -> Dict[str, Any]:
    cap = cv2.VideoCapture(video_path)
    objects = {}
    frames = 0
    while True:
      ret, frame = cap.read()
      if not ret: break
      frames += 1
      if frames % 15 != 0:  # ~2 fps sampling for 30fps
        continue
      results = self.model.predict(frame, verbose=False)[0]
      for b in results.boxes:
        cls = int(b.cls[0])
        label = results.names[cls]
        objects[label] = objects.get(label, 0) + 1
    cap.release()
    # Simple heuristic for "graphs" on screen
    has_graph = any(k in ["tv", "monitor", "laptop", "cell phone"] for k in objects)
    return {"objects": objects, "graphs_detected": has_graph}
