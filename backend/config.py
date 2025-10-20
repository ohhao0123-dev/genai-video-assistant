from pathlib import Path

DATA_DIR = Path(__file__).parent
OUTPUT_DIR = DATA_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True, parents=True)

# Model configs
WHISPER_MODEL = "small"     # base/small/medium (faster-whisper auto-ct2)
YOLO_MODEL = "yolov8n.pt"   # ultralytics tiny model
OCR_LANG = "en"
