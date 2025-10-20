from typing import Dict, Any

class BaseAgent:
  name = "base"
  def run(self, *args, **kwargs) -> Dict[str, Any]:
    raise NotImplementedError
