import json
from pathlib import Path
from typing import List, Dict, Any

class ChatStore:
  def __init__(self, path: Path):
    self.path = path
    self.path.parent.mkdir(parents=True, exist_ok=True)
    if not self.path.exists():
      self._write({})

  def _read(self) -> Dict[str, Any]:
    return json.loads(self.path.read_text())

  def _write(self, data: Dict[str, Any]):
    self.path.write_text(json.dumps(data, indent=2))

  def append(self, session_id: str, role: str, content: str):
    data = self._read()
    data.setdefault(session_id, [])
    data[session_id].append({"role": role, "content": content})
    self._write(data)

  def get(self, session_id: str) -> List[Dict[str, str]]:
    return self._read().get(session_id, [])
