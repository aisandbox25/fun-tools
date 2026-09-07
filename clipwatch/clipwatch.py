#!/usr/bin/env python3
"""clipwatch — 开着它,你复制什么,它就把那段文字追加到一个笔记文件里。

用法:
  python3 clipwatch.py              -> ~/Desktop/clipwatch/inbox.md
  python3 clipwatch.py 读书笔记  -> ~/Desktop/clipwatch/读书笔记.md

Ctrl+C 停止。同一个名字再跑,接着往同一个文件后面写。
"""

import platform
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

OUT_DIR = Path.home() / "Desktop" / "clipwatch"   # 笔记文件放哪
INTERVAL = 0.8                                     # 几秒看一次剪贴板


def read_clipboard() -> str:
    system = platform.system()
    if system == "Darwin":
        cmd = ["pbpaste"]
    elif system == "Windows":
        cmd = ["powershell", "-NoProfile", "-Command", "Get-Clipboard"]
    else:
        cmd = ["xclip", "-selection", "clipboard", "-o"]
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=2).stdout
    except Exception:
        return ""


def main() -> None:
    name = sys.argv[1] if len(sys.argv) > 1 else "inbox"
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    note = OUT_DIR / f"{name}.md"

    print(f"写到: {note}")
    print("复制任何文字就会自动记下来,Ctrl+C 停止。")

    last = read_clipboard()          # 启动时剪贴板里已有的内容不记
    while True:
        time.sleep(INTERVAL)
        text = read_clipboard()
        if not text.strip() or text == last:
            continue
        last = text
        stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with note.open("a", encoding="utf-8") as f:
            f.write(f"\n## {stamp}\n\n{text.rstrip()}\n")
        print(f"[{stamp}] 记下 {len(text)} 字", flush=True)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n已停止。")
