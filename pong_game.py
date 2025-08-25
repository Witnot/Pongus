import pygame
import random

# ----- SETTINGS -----
WIDTH, HEIGHT = 800, 600
WHITE, BLACK = (255, 255, 255), (0, 0, 0)
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_RADIUS = 15
PADDLE_SPEED = 7
BALL_SPEED = 5
FPS = 60
MAX_BALLS = 16  # Prevent too many balls
GLOBAL_HIT_COUNTER = 0
# ----- CLASSES -----
class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.base_height = PADDLE_HEIGHT

        # Full-height mechanic
        self.full_height_active = False
        self.full_height_duration = 0.3  # seconds
        self.full_height_cooldown = 1.6  # seconds
        self.full_height_timer = 0
        self.cooldown_timer = 0
        self.saved_rect = self.rect.copy()  # store original position and height

    def move(self, speed, up=True):
        if up:
            self.rect.y -= speed
        else:
            self.rect.y += speed
        self.rect.y = max(0, min(HEIGHT - self.rect.height, self.rect.y))

    def update(self, dt):
        if self.full_height_active:
            self.full_height_timer -= dt
            if self.full_height_timer <= 0:
                # shrink back to original size and position
                self.rect = self.saved_rect.copy()
                self.full_height_active = False
                self.cooldown_timer = self.full_height_cooldown
        elif self.cooldown_timer > 0:
            self.cooldown_timer -= dt

    def activate_full_height(self):
        if not self.full_height_active and self.cooldown_timer <= 0:
            self.full_height_active = True
            # save original rect
            self.saved_rect = self.rect.copy()
            # expand both upward and downward to cover full screen
            center_y = self.rect.centery
            self.rect.height = HEIGHT
            self.rect.centery = center_y  # keep center the same
            # clamp to screen
            if self.rect.top < 0:
                self.rect.top = 0
            if self.rect.bottom > HEIGHT:
                self.rect.bottom = HEIGHT
            self.full_height_timer = self.full_height_duration

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)




class Ball:
    def __init__(self):
        self.x = 50
        self.y = HEIGHT // 2
        self.dx = BALL_SPEED
        self.dy = random.choice([-1, 1]) * BALL_SPEED
        self.recent_hit_frames = 0  # debounce to prevent multi-count
        self.prev_x = self.x
        self.prev_y = self.y

    def reset(self):
        self.x = 50
        self.y = HEIGHT // 2
        self.dx = random.choice([-1, 1]) * BALL_SPEED
        self.dy = random.choice([-1, 1]) * BALL_SPEED
        self.hit_counter = 0
        self.just_split = False

    def move(self):
        # store previous pos (useful if you later want swept-collision)
        self.prev_x, self.prev_y = self.x, self.y

        self.x += self.dx
        self.y += self.dy

        # wall bounce
        if self.y - BALL_RADIUS <= 0 or self.y + BALL_RADIUS >= HEIGHT:
            self.dy *= -1

        # decay hit debounce
        if self.recent_hit_frames > 0:
            self.recent_hit_frames -= 1

    def check_collision(self, paddle, is_left_paddle: bool) -> bool:
        """
        Returns True exactly once per legitimate contact.
        - Only counts if ball is moving toward the paddle.
        - Snaps ball outside the paddle to avoid re-collisions.
        - Uses a small cooldown to debounce.
        """
        # quick circle-rect overlap via ball's AABB
        ball_rect = pygame.Rect(int(self.x - BALL_RADIUS), int(self.y - BALL_RADIUS),
                                BALL_RADIUS * 2, BALL_RADIUS * 2)
        if not ball_rect.colliderect(paddle.rect):
            return False

        # must be moving toward this paddle to count
        moving_toward = (self.dx < 0 and is_left_paddle) or (self.dx > 0 and not is_left_paddle)
        if not moving_toward:
            # still separate to prevent sticking if overlapping while moving away
            if is_left_paddle:
                self.x = max(self.x, paddle.rect.right + BALL_RADIUS)
            else:
                self.x = min(self.x, paddle.rect.left - BALL_RADIUS)
            return False

        # debounce
        if self.recent_hit_frames > 0:
            # already counted recently; just separate to be safe
            if is_left_paddle:
                self.x = paddle.rect.right + BALL_RADIUS
            else:
                self.x = paddle.rect.left - BALL_RADIUS
            return False

        # --- legit hit: reflect, separate, add angle, set cooldown ---
        # position the ball just outside the paddle on the contact side
        if is_left_paddle:
            self.x = paddle.rect.right + BALL_RADIUS
        else:
            self.x = paddle.rect.left - BALL_RADIUS

        # reflect X velocity
        self.dx *= -1

        # add a bit of angle based on where it hit the paddle
        offset = (self.y - paddle.rect.centery) / (paddle.rect.height / 2)
        self.dy += offset * 2  # tweak as you like; small = steadier, big = wilder

        # clamp dy a bit so it never goes totally vertical
        max_dy = BALL_SPEED * 1.5
        if self.dy > max_dy: self.dy = max_dy
        if self.dy < -max_dy: self.dy = -max_dy

        # set cooldown so we don't re-count while still overlapping
        self.recent_hit_frames = 8  # ~8 frames @60fps ≈ 133ms

        return True


    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), BALL_RADIUS)


# ----- AI FUNCTION -----
def ai_move(paddle, balls, speed, difficulty="Medium"):
    """
    AI paddle movement with difficulty levels.
    Predicts the ball's Y position but reacts with smoothing and random error.
    """
    # Balls moving toward AI (right paddle)
    incoming_balls = [ball for ball in balls if ball.dx > 0]
    if not incoming_balls:
        return  # no threat

    # Choose closest incoming ball
    target = min(incoming_balls, key=lambda b: WIDTH - b.x)

    # Predict Y position at paddle's x
    if target.dx != 0:
        frames_to_reach = (paddle.rect.left - target.x) / target.dx
        predicted_y = target.y + target.dy * frames_to_reach
    else:
        predicted_y = target.y

    # Add random prediction error based on difficulty
    error_map = {"Easy": 50, "Medium": 25, "Hard": 10}
    predicted_y += random.randint(-error_map.get(difficulty, 25), error_map.get(difficulty, 25))

    # Clamp inside screen
    predicted_y = max(0, min(HEIGHT, predicted_y))

    # Weighted smoothing
    smoothing_map = {"Easy": 4, "Medium": 3, "Hard": 2}
    weight = smoothing_map.get(difficulty, 3)
    target_y = (paddle.rect.centery * weight + predicted_y) / (weight + 1)

    # AI difficulty speed adjustment
    if difficulty == "Easy":
        ai_speed = max(speed - 3, 1)
    elif difficulty == "Medium":
        ai_speed = speed
    else:  # Hard
        ai_speed = speed + 3

    # Move toward target
    if paddle.rect.centery < target_y - 5:
        paddle.rect.y += ai_speed
    elif paddle.rect.centery > target_y + 5:
        paddle.rect.y -= ai_speed

    # Keep paddle inside screen
    paddle.rect.y = max(0, min(HEIGHT - paddle.rect.height, paddle.rect.y))


# global counter
hit_counter = 0  

def register_hit():
    """Call this whenever any ball hits a paddle."""
    global hit_counter
    hit_counter += 1
    return hit_counter

def spawn_ball(balls):
    """Spawn a new ball in the center and reset counter."""
    global hit_counter
    new_ball = Ball()
    new_ball.x = WIDTH // 2   # use WIDTH instead of SCREEN_WIDTH
    new_ball.y = HEIGHT // 2  # use HEIGHT instead of SCREEN_HEIGHT
    new_ball.hit_counter = 0  # start fresh
    balls.append(new_ball)

    hit_counter = 0  # reset global counter
    print(f"Spawned new ball! Total balls: {len(balls)}")
    return balls




screen = pygame.display.set_mode((WIDTH, HEIGHT))
# ----- GAME LOOP FUNCTION -----
def start_game(difficulty):
    import pygame, random
    pygame.init()

    # --- Screen setup ---
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pong AI")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    # --- Constants ---
    MAX_BALLS = 10
    PADDLE_SPEED = 7
    POINTS_TO_WIN_ROUND = 15
    ROUNDS_TO_WIN_GAME = 3

    # --- Initialize paddles and balls ---
    left_paddle = Paddle(50, HEIGHT // 2 - PADDLE_HEIGHT // 2)
    right_paddle = Paddle(WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2)
    balls = [Ball()]

    left_speed = PADDLE_SPEED
    right_speed = PADDLE_SPEED
    hit_counter = 0

    # --- Scores & rounds ---
    left_score = 0
    right_score = 0
    current_round = 1
    round_wins_left = 0
    round_wins_right = 0

    running = True
    while running:
        dt = clock.get_time() / 1000  # seconds        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        keys = pygame.key.get_pressed()
        # --- Player movement ---
        if keys[pygame.K_s]:
            left_paddle.move(-left_speed)
        if keys[pygame.K_w]:
            left_paddle.move(left_speed)
        if keys[pygame.K_SPACE]:
            left_paddle.activate_full_height()
        # --- Update paddle timers ---
        left_paddle.update(dt)               
        # --- AI movement ---
        ai_move(right_paddle, balls, speed=PADDLE_SPEED, difficulty="Medium")

        # --- Draw background ---
        screen.fill((0, 0, 0))

        frame_had_hit = False

        for ball in balls[:]:
            ball.move()
            ball.draw(screen)

            if ball.check_collision(left_paddle, is_left_paddle=True):
                frame_had_hit = True
            if ball.check_collision(right_paddle, is_left_paddle=False):
                frame_had_hit = True

            # scoring
            if ball.x < 0:
                right_score += 1
                balls.remove(ball)
                balls.append(Ball())
                continue
            elif ball.x > WIDTH:
                left_score += 1
                balls.remove(ball)
                balls.append(Ball())
                continue

        # global 4-hit spawn (only increment once per frame)
        if frame_had_hit and len(balls) < MAX_BALLS:
            hit_counter += 1
            if hit_counter >= 4:
                hit_counter = 0
                nb = Ball()
                nb.x, nb.y = WIDTH // 2, HEIGHT // 2
                balls.append(nb)
                left_speed = min(left_speed * 1.2, PADDLE_SPEED * 3)
                right_speed = min(right_speed * 1.2, PADDLE_SPEED * 3)

        # --- Draw paddles ---
        left_paddle.draw(screen)
        right_paddle.draw(screen)

        # --- Draw scores and round ---
        score_text = font.render(f"{left_score} - {right_score}", True, (255, 255, 255))
        round_text = font.render(f"Round {current_round}", True, (255, 255, 255))
        screen.blit(score_text, (WIDTH // 2 - 50, 20))
        screen.blit(round_text, (WIDTH // 2 - 50, 50))

        # --- Check round win ---
        if left_score >= POINTS_TO_WIN_ROUND:
            round_wins_left += 1
            left_score = 0
            right_score = 0
            balls = [Ball()]
            current_round += 1
        elif right_score >= POINTS_TO_WIN_ROUND:
            round_wins_right += 1
            left_score = 0
            right_score = 0
            balls = [Ball()]
            current_round += 1

        # --- Check game win ---
        if round_wins_left == ROUNDS_TO_WIN_GAME or round_wins_right == ROUNDS_TO_WIN_GAME:
            winner = "Left Player" if round_wins_left == ROUNDS_TO_WIN_GAME else "Right Player"
            print(f"{winner} wins the game!")
            running = False

        # --- Refresh display ---
        pygame.display.flip()
        clock.tick(60)

# ----- GAME LOOP FUNCTION -----
def start_game1():
    import pygame, random
    pygame.init()

    # --- Screen setup ---
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pong PvP")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    # --- Constants ---
    MAX_BALLS = 10
    PADDLE_SPEED = 7
    POINTS_TO_WIN_ROUND = 15
    ROUNDS_TO_WIN_GAME = 3

    # --- Initialize paddles and balls ---
    left_paddle = Paddle(50, HEIGHT // 2 - PADDLE_HEIGHT // 2)
    right_paddle = Paddle(WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2)
    balls = [Ball()]

    left_speed = PADDLE_SPEED
    right_speed = PADDLE_SPEED
    hit_counter = 0

    # --- Scores & rounds ---
    left_score = 0
    right_score = 0
    current_round = 1
    round_wins_left = 0
    round_wins_right = 0

    running = True
    while running:
        dt = clock.get_time() / 1000  # seconds           
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        keys = pygame.key.get_pressed()

        # --- Player 1 movement (W/S/SPACE) ---
        if keys[pygame.K_s]:
            left_paddle.move(-left_speed)
        if keys[pygame.K_w]:
            left_paddle.move(left_speed)
        if keys[pygame.K_SPACE]:
            left_paddle.activate_full_height()

        # --- Player 2 movement (UP/DOWN/LEFT) ---
        if keys[pygame.K_DOWN]:
            right_paddle.move(-right_speed)
        if keys[pygame.K_UP]:
            right_paddle.move(right_speed)
        if keys[pygame.K_LEFT]:
            right_paddle.activate_full_height()
        # --- Update paddle timers ---
        left_paddle.update(dt)   
        right_paddle.update(dt)
        # --- Draw background ---
        screen.fill((0, 0, 0))

        frame_had_hit = False

        for ball in balls[:]:
            ball.move()
            ball.draw(screen)

            if ball.check_collision(left_paddle, is_left_paddle=True):
                frame_had_hit = True
            if ball.check_collision(right_paddle, is_left_paddle=False):
                frame_had_hit = True

            # scoring
            if ball.x < 0:
                right_score += 1
                balls.remove(ball)
                balls.append(Ball())
                continue
            elif ball.x > WIDTH:
                left_score += 1
                balls.remove(ball)
                balls.append(Ball())
                continue

        # global 4-hit spawn (only increment once per frame)
        if frame_had_hit and len(balls) < MAX_BALLS:
            hit_counter += 1
            if hit_counter >= 4:
                hit_counter = 0
                nb = Ball()
                nb.x, nb.y = WIDTH // 2, HEIGHT // 2
                balls.append(nb)
                left_speed = min(left_speed * 1.2, PADDLE_SPEED * 3)
                right_speed = min(right_speed * 1.2, PADDLE_SPEED * 3)

        # --- Draw paddles ---
        left_paddle.draw(screen)
        right_paddle.draw(screen)

        # --- Draw scores and round ---
        score_text = font.render(f"{left_score} - {right_score}", True, (255, 255, 255))
        round_text = font.render(f"Round {current_round}", True, (255, 255, 255))
        screen.blit(score_text, (WIDTH // 2 - 50, 20))
        screen.blit(round_text, (WIDTH // 2 - 50, 50))

        # --- Check round win ---
        if left_score >= POINTS_TO_WIN_ROUND:
            round_wins_left += 1
            left_score = 0
            right_score = 0
            balls = [Ball()]
            current_round += 1
        elif right_score >= POINTS_TO_WIN_ROUND:
            round_wins_right += 1
            left_score = 0
            right_score = 0
            balls = [Ball()]
            current_round += 1

        # --- Check game win ---
        if round_wins_left == ROUNDS_TO_WIN_GAME or round_wins_right == ROUNDS_TO_WIN_GAME:
            winner = "Left Player" if round_wins_left == ROUNDS_TO_WIN_GAME else "Right Player"
            print(f"{winner} wins the game!")
            running = False

        # --- Refresh display ---
        pygame.display.flip()
        clock.tick(60)
