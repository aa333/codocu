import asyncio
import os
import socket
import time
from collections import deque
from pathlib import Path

import psutil

from src.core import di
from src.core.di import ModuleList

hostname = socket.gethostname()

MIN_SLEEP = 10
MAX_SLEEP = 1200


class SystemService:
    def __init__(self, log_file: str) -> None:
        self._log_file = log_file
        self._sleeping = False
        self._start_time = time.monotonic()

    def get_uptime_seconds(self) -> int:
        return int(time.monotonic() - self._start_time)

    def get_uptime_text(self) -> str:
        uptime = self.get_uptime_seconds()
        h, remainder = divmod(uptime, 3600)
        m, s = divmod(remainder, 60)
        parts = []
        if h:
            parts.append(f"{h}h")
        if m:
            parts.append(f"{m}m")
        parts.append(f"{s}s")
        return " ".join(parts)

    async def collect_debug_info(self) -> str:
        modules = di.get(ModuleList)
        debugs = [f"Host: {hostname}"]
        for module in modules:
            debug_result = module.debug()
            if asyncio.iscoroutine(debug_result):
                debugs.append(await debug_result)
            else:
                debugs.append(debug_result)
        debugs.append(self._get_mem())
        return "\n=========\n".join(debugs)

    def _get_mem(self) -> str:
        pid = os.getpid()
        proc = psutil.Process(pid)
        mem_mb = round(proc.memory_info()[0] / 1048576, 2)
        return f"CPU: {psutil.cpu_percent()}%, RAM (bot): {mem_mb}MB, RAM (total): {psutil.virtual_memory()[2]}%"

    def get_recent_logs(self, max_lines: int = 200) -> str | None:
        log_path = Path(self._log_file)
        if not log_path.is_file():
            return None
        with open(log_path, encoding="utf-8", errors="replace") as f:
            lines = deque(f, maxlen=max_lines)
        return "".join(lines)

    @property
    def module_count(self) -> int:
        return len(di.get(ModuleList))

    def parse_sleep_args(self, args: list[str]) -> tuple[bool, str]:
        """Validate /sleep args. Returns (ok, error_or_empty)."""
        if len(args) < 1:
            return False, (f"Надо: /sleep seconds (мин {MIN_SLEEP}, макс {MAX_SLEEP})")
        if not args[0].isdecimal():
            return False, "Секунды должны быть целым числом"
        val = int(args[0])
        if val < MIN_SLEEP or val > MAX_SLEEP:
            return False, (f"Секунды должны быть от {MIN_SLEEP} до {MAX_SLEEP}")
        return True, ""

    async def sleep(self, seconds: int) -> None:
        """Block the event loop to stop polling and yield to another instance."""
        self._sleeping = True
        time.sleep(seconds)
        self._sleeping = False
