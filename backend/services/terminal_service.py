# backend/services/terminal_service.py
import os
import pty
import subprocess
import asyncio
from fastapi import WebSocket
from config import PROJECT_REPO_PATH


class TerminalSession:
    def __init__(self):
        self.process = None
        self.fd = None

    def start(self):
        master_fd, slave_fd = pty.openpty()
        self.fd = master_fd
        self.process = subprocess.Popen(
            ["claude", "--dangerously-skip-permissions"],
            cwd=str(PROJECT_REPO_PATH),
            stdin=slave_fd,
            stdout=slave_fd,
            stderr=slave_fd,
            env={**os.environ, "TERM": "xterm-256color"},
            start_new_session=True,
        )
        os.close(slave_fd)

    def write(self, data: str):
        if self.fd is not None:
            os.write(self.fd, data.encode())

    def resize(self, rows: int, cols: int):
        if self.fd is not None:
            import fcntl
            import termios
            import struct

            winsize = struct.pack("HHHH", rows, cols, 0, 0)
            fcntl.ioctl(self.fd, termios.TIOCSWINSZ, winsize)

    def stop(self):
        if self.process:
            self.process.terminate()
            self.process = None
        if self.fd:
            os.close(self.fd)
            self.fd = None

    async def stream_to_ws(self, ws: WebSocket):
        loop = asyncio.get_event_loop()
        while self.fd is not None:
            try:
                data = await loop.run_in_executor(
                    None, lambda: os.read(self.fd, 4096)
                )
                if not data:
                    break
                await ws.send_bytes(data)
            except OSError:
                break

    async def read_from_ws(self, ws: WebSocket):
        while True:
            try:
                data = await ws.receive_text()
                self.write(data)
            except Exception:
                break

    def inject_command(self, cmd: str):
        self.write(cmd + "\r")


# Global singleton for stage-auto-inject
_terminal: "TerminalSession | None" = None

def get_terminal() -> "TerminalSession | None":
    return _terminal

def set_terminal(session: "TerminalSession"):
    global _terminal
    _terminal = session
