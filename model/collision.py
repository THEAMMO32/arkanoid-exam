def rect_collision(rect1, rect2):
    x1, y1, w1, h1 = rect1
    x2, y2, w2, h2 = rect2
    return (x1 < x2 + w2 and x1 + w1 > x2 and
            y1 < y2 + h2 and y1 + h1 > y2)

def get_collision_side(ball_rect, brick_rect):
    """Возвращает сторону, с которой мяч столкнулся с блоком: 'top', 'bottom', 'left', 'right'."""
    ball_center_x = ball_rect[0] + ball_rect[2] / 2
    ball_center_y = ball_rect[1] + ball_rect[3] / 2
    brick_center_x = brick_rect[0] + brick_rect[2] / 2
    brick_center_y = brick_rect[1] + brick_rect[3] / 2

    dx = ball_center_x - brick_center_x
    dy = ball_center_y - brick_center_y
    overlap_x = (ball_rect[2] + brick_rect[2]) / 2 - abs(dx)
    overlap_y = (ball_rect[3] + brick_rect[3]) / 2 - abs(dy)

    if overlap_x > overlap_y:
        return 'left' if dx < 0 else 'right'
    else:
        return 'top' if dy < 0 else 'bottom'

def ball_paddle_collision(ball_rect, paddle_rect, ball):
    if not rect_collision(ball_rect, paddle_rect):
        return False
    ball.bounce_y()
    paddle_center = paddle_rect[0] + paddle_rect[2] / 2
    ball_center = ball_rect[0] + ball_rect[2] / 2
    offset = (ball_center - paddle_center) / (paddle_rect[2] / 2)
    ball.vx += offset * 150
    if abs(ball.vx) < 150:
        ball.vx = 150 if ball.vx > 0 else -150
    if abs(ball.vx) > 500:
        ball.vx = 500 if ball.vx > 0 else -500
    return True