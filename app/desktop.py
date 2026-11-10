"""Zengő asztali app: a belső szerver láthatatlanul fut, a felület saját ablakban (pywebview, WebView2).

Indítás:  pythonw -m app.desktop [--root MAPPA]
A --root a hordozható mappa (benne data\\, Hangoskönyvek\\, runtime\\). Ha nincs megadva, a régi
(Felolvasó) adathelyeket használja, ami fejlesztéshez kényelmes.
"""

from __future__ import annotations

import argparse
import ctypes
import logging
import os
import socket
import sys
import threading
import time
from pathlib import Path

TITLE = "Zengő"
log = logging.getLogger("zengo")


def _focus_existing() -> bool:
    """Ha már fut egy Zengő ablak, azt hozza előre."""
    if os.name != "nt":
        return False
    user32 = ctypes.windll.user32
    hwnd = user32.FindWindowW(None, TITLE)
    if not hwnd:
        return False
    user32.ShowWindow(hwnd, 9)  # SW_RESTORE
    user32.SetForegroundWindow(hwnd)
    return True


def _single_instance_lock(data: Path):
    """Kizárólagos zár a data mappában; None, ha egy másik példány már tartja."""
    import msvcrt

    data.mkdir(parents=True, exist_ok=True)
    f = open(data / "zengo.lock", "a+")  # noqa: SIM115 - a zár a folyamat élete végéig marad nyitva
    try:
        msvcrt.locking(f.fileno(), msvcrt.LK_NBLCK, 1)
    except OSError:
        f.close()
        return None
    return f


def _free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def _message(text: str) -> None:
    if os.name == "nt":
        ctypes.windll.user32.MessageBoxW(None, text, TITLE, 0x10)
    else:
        print(text, file=sys.stderr)


def main() -> int:
    parser = argparse.ArgumentParser(prog="zengo")
    parser.add_argument("--root", type=Path, default=None, help="a hordozható mappa")
    args = parser.parse_args()

    root = args.root.resolve() if args.root else None
    if root:
        from app import portable

        portable.setup_env(root)  # az app.config importálása előtt kell
        data = portable.data_dir(root)
    else:
        from platformdirs import user_data_dir

        data = Path(user_data_dir("Felolvaso", appauthor=False))

    lock = _single_instance_lock(data)
    if lock is None:
        if not _focus_existing():
            _message("A Zengő már fut.")
        return 0

    if root:
        logging.basicConfig(level=logging.INFO)
        try:
            portable.migrate(root)
        except Exception as e:
            log.exception("Átköltöztetés sikertelen")
            _message(f"A régi adatok átmásolása nem sikerült:\n{e}\n\nA régi adatok érintetlenek.")
            return 1

    import uvicorn
    import webview

    from app.main import HOST, create_app
    from app.state import AppState, setup_logging

    state = AppState()
    setup_logging(state.config)
    state.init_qa()
    port = _free_port()
    server = uvicorn.Server(uvicorn.Config(create_app(state), host=HOST, port=port, log_level="warning"))
    thread = threading.Thread(target=server.run, name="zengo-server", daemon=True)
    thread.start()
    for _ in range(300):
        if server.started:
            break
        if not thread.is_alive():
            _message("A Zengő belső szervere nem indult el. Részletek: data\\logs")
            return 1
        time.sleep(0.05)

    window = webview.create_window(TITLE, f"http://{HOST}:{port}/", width=1360, height=900, min_size=(900, 600),
                                   background_color="#1f2a26", text_select=True)

    def on_closing():
        job = state.queue.current
        if job is None:
            return True
        ok = window.create_confirmation_dialog(
            TITLE, "Éppen generálás fut. Ha most bezárod, szünetel, és a következő indításkor folytatható.\n\n"
                   "Bezárod?")
        return bool(ok)

    window.events.closing += on_closing
    webview.settings["ALLOW_DOWNLOADS"] = True
    webview.settings["OPEN_EXTERNAL_LINKS_IN_BROWSER"] = True
    icon = (root / "zengo.ico") if root else Path(__file__).resolve().parent / "web" / "static" / "zengo.ico"
    webview.start(icon=str(icon) if icon.exists() else None, private_mode=False,
                  storage_path=str(data / "webview"))

    # ablak bezárva: szerver és motorok leállítása (a lifespan leállítja a sort és a workereket)
    server.should_exit = True
    thread.join(timeout=60)
    lock.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
