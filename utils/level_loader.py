"""Генерация сетки кирпичей, стен и тем оформления по сложности."""

from model.brick import Brick
from model.wall import Wall
from utils.constants import *

WALL_THICKNESS = 8

THEMES = [
    {
        "bg": (15, 20, 45), "ball": (255, 120, 80),
        "paddle": (200, 200, 220),
        "weak": (60, 180, 255), "strong": (30, 90, 200),
        "indestructible": (100, 100, 120),
    },
    {
        "bg": (8, 10, 30), "ball": (255, 80, 200),
        "paddle": (220, 120, 200),
        "weak": (80, 255, 200), "strong": (20, 200, 140),
        "indestructible": (100, 100, 120),
    },
    {
        "bg": (40, 15, 35), "ball": (255, 150, 200),
        "paddle": (220, 180, 200),
        "weak": (255, 100, 150), "strong": (180, 40, 90),
        "indestructible": (120, 110, 130),
    },
]


def _grid_geometry(width):
    """Вычисляет геометрию сетки: стартовую позицию, шаги, число колонок."""
    margin = 10
    gap_x = BRICK_GAP_X
    gap_y = BRICK_GAP_Y
    bw = BRICK_WIDTH
    bh = BRICK_HEIGHT
    available = width - 2 * margin
    cols = max(1, (available + gap_x) // (bw + gap_x))
    total_w = cols * (bw + gap_x) - gap_x
    start_x = (width - total_w) // 2
    return start_x, bw, bh, gap_x, gap_y, cols


def _default_grid(width, height, strength_mode):
    """Базовая сетка блоков (не используется напрямую)."""
    start_x, bw, bh, gap_x, gap_y, cols = _grid_geometry(width)
    bricks = []
    rows = BRICK_ROWS
    for row in range(rows):
        for col in range(cols):
            x = start_x + col * (bw + gap_x)
            y = BRICK_OFFSET_Y + row * (bh + gap_y)
            if strength_mode == 'all_weak':
                s = 1
            elif strength_mode == 'all_strong':
                s = 2
            else:
                s = 2 if row >= rows - 2 else 1
            bricks.append(Brick(x, y, bw, bh, s))
    return bricks


def _build_easy_grid(width, height):
    """Плотная раскладка для уровня «Легко» — все блоки слабые."""
    start_x, bw, bh, gap_x, gap_y, cols = _grid_geometry(width)
    bricks = []
    rows = 8
    for row in range(rows):
        for col in range(cols):
            x = start_x + col * (bw + gap_x)
            y = BRICK_OFFSET_Y + row * (bh + gap_y)
            bricks.append(Brick(x, y, bw, bh, strength=1))
    return bricks


def _build_medium_grid(width, height):
    """Уровень «Средне»: нижние два ряда — прочные, остальные — слабые."""
    start_x, bw, bh, gap_x, gap_y, cols = _grid_geometry(width)
    bricks = []
    rows = 8
    for row in range(rows):
        s = 2 if row >= rows - 2 else 1
        for col in range(cols):
            x = start_x + col * (bw + gap_x)
            y = BRICK_OFFSET_Y + row * (bh + gap_y)
            bricks.append(Brick(x, y, bw, bh, s))
    return bricks


def _build_hard_grid(width, height):
    """Сложный уровень: 8 рядов, zigzag неразрушаемых столбов, все прочные."""
    start_x, bw, bh, gap_x, gap_y, cols = _grid_geometry(width)
    bricks = []
    rows = 8

    pillar_a = [c for c in range(cols) if c % 4 == 1]
    pillar_b = [c for c in range(cols) if c % 4 == 3]
    edges = [0, cols - 1]

    indestructible_map = {
        0: edges,
        2: pillar_a,
        4: pillar_b + edges,
        6: pillar_a,
        7: edges,
    }

    for row in range(rows):
        inde_cols = set(indestructible_map.get(row, []))
        for col in range(cols):
            x = start_x + col * (bw + gap_x)
            y = BRICK_OFFSET_Y + row * (bh + gap_y)
            if col in inde_cols:
                bricks.append(
                    Brick(x, y, bw, bh, strength=1, indestructible=True)
                )
            else:
                bricks.append(Brick(x, y, bw, bh, strength=2))
    return bricks


def build_bricks_for_level(width, height, difficulty):
    """Возвращает список Brick для выбранной сложности."""
    if difficulty == 0:
        return _build_easy_grid(width, height)
    if difficulty == 1:
        return _build_medium_grid(width, height)
    return _build_hard_grid(width, height)


def get_theme(difficulty):
    """Возвращает цветовую тему для выбранной сложности."""
    return THEMES[difficulty % len(THEMES)]


def build_walls_for_level(width, height, difficulty):
    """Возвращает список Wall: крест для «Средне», лестница для «Сложно»."""
    walls = []
    if difficulty == 1:
        walls = _build_medium_walls(width, height)
    elif difficulty == 2:
        walls = _build_hard_walls(width, height)
    return walls


def _build_medium_walls(width, height):
    """Крестообразная фигура для уровня «Средне»."""
    walls = []
    rows = 8
    start_x, bw, bh, gap_x, gap_y, cols = _grid_geometry(width)
    t = WALL_THICKNESS
    edge_gap = BALL_RADIUS * 2 + 10

    col_1 = cols // 3
    col_2 = cols * 2 // 3
    v1_x = start_x + col_1 * (bw + gap_x) + bw + (gap_x - t) // 2
    v2_x = start_x + col_2 * (bw + gap_x) + bw + (gap_x - t) // 2
    v_top = BRICK_OFFSET_Y
    v_h = rows * (bh + gap_y) - gap_y
    walls.append(Wall(v1_x, v_top, t, v_h))
    walls.append(Wall(v2_x, v_top, t, v_h))

    row_after = 4
    h_y = (
        BRICK_OFFSET_Y + row_after * (bh + gap_y) + bh
        + (gap_y - t) // 2
    )
    h_clear = bw + gap_x
    h1_x = start_x + edge_gap
    h1_w = v1_x - h1_x - h_clear
    h2_x = v2_x + t + h_clear
    h2_w = start_x + cols * (bw + gap_x) - gap_x - h2_x - edge_gap
    walls.append(Wall(h1_x, h_y, max(h1_w, t), t))
    walls.append(Wall(h2_x, h_y, max(h2_w, t), t))

    return walls


def _build_hard_walls(width, height):
    """Лестничная фигура для уровня «Сложно»: 2 вертикальные + 3 ступени."""
    walls = []
    rows = 8
    start_x, bw, bh, gap_x, gap_y, cols = _grid_geometry(width)
    t = WALL_THICKNESS
    h_clear = bw + gap_x
    edge_gap = BALL_RADIUS * 2 + 10

    col_1 = cols // 3
    col_2 = cols * 2 // 3
    v1_x = start_x + col_1 * (bw + gap_x) + bw + (gap_x - t) // 2
    v2_x = start_x + col_2 * (bw + gap_x) + bw + (gap_x - t) // 2

    v_top = BRICK_OFFSET_Y
    v_h = rows * (bh + gap_y) - gap_y + 80
    walls.append(Wall(v1_x, v_top, t, v_h))
    walls.append(Wall(v2_x, v_top, t, v_h))

    h1_row = 1
    h1_y = (
        BRICK_OFFSET_Y + h1_row * (bh + gap_y) + bh
        + (gap_y - t) // 2
    )
    h1_x = start_x + edge_gap
    h1_w = v1_x - h1_x - h_clear
    walls.append(Wall(h1_x, h1_y, max(h1_w, t), t))

    h2_row = 3
    h2_y = (
        BRICK_OFFSET_Y + h2_row * (bh + gap_y) + bh
        + (gap_y - t) // 2
    )
    h2_x = v1_x + t + h_clear
    h2_w = v2_x - h2_x - h_clear
    walls.append(Wall(h2_x, h2_y, max(h2_w, t), t))

    h3_row = 5
    h3_y = (
        BRICK_OFFSET_Y + h3_row * (bh + gap_y) + bh
        + (gap_y - t) // 2
    )
    h3_x = v2_x + t + h_clear
    h3_w = start_x + cols * (bw + gap_x) - gap_x - h3_x - edge_gap
    walls.append(Wall(h3_x, h3_y, max(h3_w, t), t))

    return walls
