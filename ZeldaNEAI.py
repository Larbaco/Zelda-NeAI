import arcade
import subprocess
from core import *


def _ultimo_commit():
    try:
        sha = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            stderr=subprocess.DEVNULL).decode().strip()
        branch = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            stderr=subprocess.DEVNULL).decode().strip()
        return f"{branch} @ {sha}"
    except Exception:
        return "desconhecido (sem git)"


def main():
    print(f"[ZeldaNEAI] iniciando | ultimo commit: {_ultimo_commit()}")
    game = Zenai("ZENAI")
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
