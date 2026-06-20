import math
from model.brick import Brick
from model.wall import Wall
from utils.constants import *

WALL_THICKNESS = 8  # толщина стенки для надёжного отскока

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
    [
        "111111111111",
        "222222222222",
        "111100001111",
        "000033330000",
        "111100001111",
        "222222222222",
        "111111111111",
    ],
]

THEMES = [
    {"bg": (15, 20, 45), "ball": (255, 120, 80), "paddle": (200, 200, 220),
     "weak": (60, 180, 255), "strong": (30, 90, 200)},
    {"bg": (8, 10, 30), "ball": (255, 80, 200), "paddle": (220, 120, 200),
     "weak": (80, 255, 200), "strong": (20, 200, 140)},
    {"bg": (40, 15, 35), "ball": (255, 150, 200), "paddle": (220, 180, 200),
     "weak": (255, 100, 150), "strong": (180, 40, 90)},
    {"bg": (25, 25, 30), "ball": (180, 255, 255), "paddle": (200, 200, 200),
     "weak": (200, 200, 100), "strong": (140, 140, 60)},
    {"bg": (10, 10, 25), "ball": (255, 80, 80), "paddle": (255, 200, 150),
     "weak": (255, 180, 50), "strong": (220, 120, 20)},
]

def _grid_geometry(width, extra_gap_x=0, extra_gap_y=0):
    margin = 10
    gap_x = BRICK_GAP_X + extra_gap_x
    gap_y = BRICK_GAP_Y + extra_gap_y
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
        return _build_easy_grid(width, height), []
    # Medium difficulty (default): denser layout with mixed strength
    if strength_mode == 'default' and level_index == 0:
        return _build_medium_grid(width, height), []
    if layout is None:
        return _default_grid(width, height, strength_mode), []

    # Уровень 2 (индекс 1): увеличенные зазоры (+4 px)
    extra_gap_x = 4 if level_index == 1 else 0
    extra_gap_y = 4 if level_index == 1 else 0
    start_x, bw, bh, gap_x, gap_y, max_cols = _grid_geometry(width, extra_gap_x, extra_gap_y)

    bricks = []
    layout_walls = []
    for row_idx, row_str in enumerate(layout):
        row_len = len(row_str)
        offset = (max_cols - row_len) // 2
        for col_idx, ch in enumerate(row_str):
            if ch == '0':
                continue
            if ch == '3':
                # '3' — неразрушаемая стена (Wall), не кирпич
                col = offset + col_idx
                x = start_x + col * (bw + gap_x)
                y = BRICK_OFFSET_Y + row_idx * (bh + gap_y)
                layout_walls.append(Wall(x, y, bw, bh))
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
    return bricks, layout_walls

def get_theme(level_index):
    return THEMES[level_index % len(THEMES)]


def build_walls_for_level(width, height, difficulty, level_index):
    """Создаёт неразрушаемые стенки. Только для среднего уровня (difficulty=1).

    Крестообразная фигура из 4 стенок:
    - 2 вертикальные стенки точно в зазорах между колонками на 1/3 и 2/3 сетки
    - 2 горизонтальные стенки точно в зазоре между рядами 4 и 5,
      с отступами от краёв экрана (ball_diameter + 10px)
    """
    walls = []
    if difficulty != 1 or level_index != 0:
        return walls

    start_x, bw, bh, gap_x, gap_y, cols = _grid_geometry(width)
    rows = 8
    t = WALL_THICKNESS
    edge_gap = BALL_RADIUS * 2 + 10  # clearance = ball_diameter + 10px

    # --- Вертикальные стенки ---
    # Точно в зазорах между колонками cols//3 и cols//3+1,
    # и между cols*2//3 и cols*2//3+1
    col_1 = cols // 3
    col_2 = cols * 2 // 3
    v1_x = start_x + col_1 * (bw + gap_x) + bw + (gap_x - t) // 2
    v2_x = start_x + col_2 * (bw + gap_x) + bw + (gap_x - t) // 2
    v_top = BRICK_OFFSET_Y
    v_h = rows * (bh + gap_y) - gap_y
    walls.append(Wall(v1_x, v_top, t, v_h))
    walls.append(Wall(v2_x, v_top, t, v_h))

    # --- Горизонтальные стенки (2 штуки на одном Y) ---
    # Точно в зазоре между рядами 4 и 5 (row_after=4)
    row_after = 4
    h_y = BRICK_OFFSET_Y + row_after * (bh + gap_y) + bh + (gap_y - t) // 2

    # Зазор между горизонтальной и вертикальной стенкой
    h_clear = bw + gap_x  # один блок + зазор — достаточно для мяча
    # Отступ от краёв экрана = edge_gap
    h1_x = start_x + edge_gap
    h1_w = v1_x - h1_x - h_clear
    h2_x = v2_x + t + h_clear
    h2_w = start_x + cols * (bw + gap_x) - gap_x - h2_x - edge_gap
    walls.append(Wall(h1_x, h_y, max(h1_w, t), t))
    walls.append(Wall(h2_x, h_y, max(h2_w, t), t))

    return walls