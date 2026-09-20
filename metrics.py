import psutil
import json
from datetime import datetime, timezone

memory = psutil.virtual_memory()
cpu = psutil.cpu_percent(interval=0.1)

data = {
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "cpu_percent": cpu,
    "memory_total": memory.total,
    "memory_used": memory.used,
    "memory_percent": memory.percent,
}

print(json.dumps(data, indent=2))