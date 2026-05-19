from __future__ import annotations

import os
import socket
import sys
import threading
import time
import webbrowser
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent
DEFAULT_PORT = 5000


def setup_console() -> None:
    if os.name == "nt":
        os.system("chcp 65001 > nul")

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")


def find_free_port(start_port: int = DEFAULT_PORT) -> int:
    for port in range(start_port, start_port + 50):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.2)
            if sock.connect_ex(("127.0.0.1", port)) != 0:
                return port

    return DEFAULT_PORT


def open_browser(url: str) -> None:
    time.sleep(1.5)
    webbrowser.open(url)


def pause() -> None:
    print()
    input("Нажмите Enter, чтобы закрыть окно...")


def main() -> None:
    setup_console()
    os.chdir(PROJECT_DIR)

    try:
        from app import create_app
        from app.extensions import db
        from app.models import User
        from werkzeug.security import generate_password_hash
    except ModuleNotFoundError as exc:
        print("Ошибка: не установлена зависимость.")
        print(f"Отсутствующий модуль: {exc.name}")
        print()
        print("Выполните команду:")
        print(r".venv\Scripts\python.exe -m pip install -r requirements.txt")
        pause()
        return

    try:
        app = create_app()

        with app.app_context():
            db.create_all()

            admin = User.query.filter_by(username="admin").first()
            if not admin:
                admin = User(
                    username="admin",
                    password_hash=generate_password_hash("admin123"),
                )
                db.session.add(admin)
                db.session.commit()

        port = find_free_port()
        url = f"http://127.0.0.1:{port}/"

        print("Сайт запущен.")
        print(f"Адрес: {url}")
        print("Логин: admin")
        print("Пароль: admin123")
        print()
        print("Чтобы остановить сайт, закройте это окно или нажмите Ctrl+C.")

        threading.Thread(target=open_browser, args=(url,), daemon=True).start()

        app.run(
            host="127.0.0.1",
            port=port,
            debug=False,
            use_reloader=False
        )

    except KeyboardInterrupt:
        print()
        print("Сайт остановлен.")

    except Exception as exc:
        print()
        print("Ошибка при запуске сайта:")
        print(exc)
        pause()


if __name__ == "__main__":
    main()