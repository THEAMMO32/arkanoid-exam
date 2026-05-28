def rect_collision(rect1, rect2):
    x1, y1, w1, h1 = rect1
    x2, y2, w2, h2 = rect2
    return (x1 < x2 + w2 and x1 + w1 > x2 and
            y1 < y2 + h2 and y1 + h1 > y2)

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