from model.brick import Brick
from model.wall import Wall
from utils.constants import *

LEVEL_LAYOUTS = [
    None,
    [
        "111111111111",
        "111111111111",
        "111111111111",
        "111111111111",
        "111111111111",
        "111111111111",
        "111111111111",
        "111111111111",
    ],
    [
        "222222222222",
        "211111111112",
        "211122221112",
        "211122221112",
        "211111111112",
        "222222222222",
    ],
    [
        "101010101010",
        "010101010101",
        "101010101010",
        "010101010101",
        "101010101010",
        "010101010101",
    ],
    [
        "000000220000",
        "000002222000",
        "000022222200",
        "111122222211",
        "111112222111",
        "111111111111",
        "111111111111",
    ],
]

THEMES = [
    {"bg": (15, 20, 45), "ball": (255, 120, 80), "paddle": (200, 200, 220),
     "weak": (60, 180, 255), "strong": (30, 90, 200)},
    {"bg": (25, 15, 35), "ball": (255, 200, 60), "paddle": (220, 180, 140),
     "weak": (255, 170, 40), "strong": (200, 80, 20)},
    {"bg": (40, 15, 35), "ball": (255, 150, 200), "paddle": (220, 180, 200),
     "weak": (255, 100, 150), "strong": (180, 40, 90)},
    {"bg": (25, 25, 30), "ball": (180, 255, 255), "paddle": (200, 200, 200),
     "weak": (200, 200, 100), "strong": (140, 140, 60)},
    {"bg": (10, 10, 25), "ball": (255, 80, 80), "paddle": (255, 200, 150),
     "weak": (255, 180, 50), "strong": (220, 120, 20)},
]

def _grid_geometry(width):
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
    """Denser brick layout for easy difficulty — more rows, full width."""
    start_x, bw, bh, gap_x, gap_y, cols = _grid_geometry(width)
    bricks = []
    rows = 8  # more rows than default 5
    for row in range(rows):
        for col in range(cols):
            x = start_x + col * (bw + gap_x)
            y = BRICK_OFFSET_Y + row * (bh + gap_y)
            bricks.append(Brick(x, y, bw, bh, strength=1))
    return bricks


def _build_medium_grid(width, height):
    """Средний уровень: 8 рядов, верхние — слабые, нижние — прочные, все заполнены."""
    start_x, bw, bh, gap_x, gap_y, cols = _grid_geometry(width)
    bricks = []
    rows = 8
    for row in range(rows):
        # Нижние 2 ряда — прочные (strength=2), остальные — 1
        s = 2 if row >= rows - 3 else 1
        for col in range(cols):
            x = start_x + col * (bw + gap_x)
            y = BRICK_OFFSET_Y + row * (bh + gap_y)
            bricks.append(Brick(x, y, bw, bh, s))
    return bricks

def build_bricks_for_level(width, height, level_index, strength_mode):
    layout = LEVEL_LAYOUTS[level_index % len(LEVEL_LAYOUTS)]
    # Easy difficulty (all_weak): use a denser brick layout
    if strength_mode == 'all_weak' and level_index == 0:
        return _build_easy_grid(width, height)
    # Medium difficulty (default): denser layout with mixed strength
    if strength_mode == 'default' and level_index == 0:
        return _build_medium_grid(width, height)
    if layout is None:
        return _default_grid(width, height, strength_mode)
    start_x, bw, bh, gap_x, gap_y, max_cols = _grid_geometry(width)
    bricks = []
    for row_idx, row_str in enumerate(layout):
        row_len = len(row_str)
        offset = (max_cols - row_len) // 2
        for col_idx, ch in enumerate(row_str):
            if ch == '0':
                continue
            strength = int(ch)
            if strength_mode == 'all_weak':
                strength = 1
            elif strength_mode == 'all_strong' and strength > 0:
                strength = 2
            col = offset + col_idx
            x = start_x + col * (bw + gap_x)
            y = BRICK_OFFSET_Y + row_idx * (bh + gap_y)
            bricks.append(Brick(x, y, bw, bh, strength))
    return bricks

def get_theme(level_index):
    return THEMES[level_index % len(THEMES)]


def build_walls_for_level(width, height, difficulty, level_index):
    """Создаёт неразрушаемые стенки. Пока только для среднего уровня (difficulty=1)."""
    walls = []
    if difficulty != 1 or level_index != 0:
        return walls

    start_x, bw, bh, gap_x, gap_y, cols = _grid_geometry(width)
    rows = 8

    # Стенки размещаются МЕЖДУ рядами блоков и МЕЖДУ колонками
    # Горизонтальная стенка между 3-м и 4-м рядами блоков
    h_wall_h = gap_y  # толщина = размер зазора
    h_wall_w = cols * (bw + gap_x) - gap_x  # на всю ширину сетки
    h_wall_x = start_x
    h_wall_y = BRICK_OFFSET_Y + 3 * (bh + gap_y) + bh  # после 3-го ряда
    walls.append(Wall(h_wall_x, h_wall_y, h_wall_w, h_wall_h))

    # Вертикальная стенка по центру между колонками
    v_wall_w = gap_x
    v_wall_h = 3 * (bh + gap_y)  # через первые 3 ряда
    v_wall_x = start_x + (cols // 2) * (bw + gap_x)  # между центральными колонками
    v_wall_y = BRICK_OFFSET_Y
    walls.append(Wall(v_wall_x, v_wall_y, v_wall_w, v_wall_h))

    # Ещё одна вертикальная стенка в нижних 3 рядах
    v_wall_y2 = h_wall_y + h_wall_h
    walls.append(Wall(v_wall_x, v_wall_y2, v_wall_w, v_wall_h))

    return walls