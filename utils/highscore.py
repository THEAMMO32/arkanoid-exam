"""Загрузка и сохранение рекордного счёта."""

import os

HIGHSCORE_FILE = "highscore.txt"


def load_highscore():
    """Возвращает сохранённый рекорд или 0, если файл отсутствует."""
    if os.path.exists(HIGHSCORE_FILE):
        with open(HIGHSCORE_FILE, "r") as f:
            try:
                return int(f.read())
            except ValueError:
                return 0
    return 0


def save_highscore(score):
    """Записывает рекордный счёт в файл."""
    with open(HIGHSCORE_FILE, "w") as f:
        f.write(str(score))
