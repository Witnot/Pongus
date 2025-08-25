import random




def check_ball_splitting(balls, left_paddle_speed, right_paddle_speed):
    """
    For each ball, check if hit_counter reached 4. If so, split and increase paddle speeds.
    """
    new_balls = []
    for ball in balls[:]:  # iterate over a copy
        if ball.hit_counter >= 4:
            # Reset hit counter for original ball
            ball.hit_counter = 0

            # Split ball into 2 new balls
            b1 = Ball()
            b1.x, b1.y = ball.x, ball.y
            b1.dx = ball.dx
            b1.dy = ball.dy

            b2 = Ball()
            b2.x, b2.y = ball.x, ball.y
            b2.dx = -ball.dx
            b2.dy = -ball.dy

            new_balls.extend([b1, b2])

            # Increase paddle speeds by 50%
            left_paddle_speed *= 1.5
            right_paddle_speed *= 1.5

            print(f"Ball split! Total balls: {len(balls) + len(new_balls)}")
            print(f"New paddle speeds: {left_paddle_speed}, {right_paddle_speed}")

    balls.extend(new_balls)
    return balls, left_paddle_speed, right_paddle_speed
