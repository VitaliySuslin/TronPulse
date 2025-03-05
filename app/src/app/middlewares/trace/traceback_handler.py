import traceback
from typing import Optional, List


async def get_last_trace() -> Optional[List[str]]:
    try:
        data = traceback.format_exc()
        return str(data)[-200:].split("\n")
    except Exception:
        return None