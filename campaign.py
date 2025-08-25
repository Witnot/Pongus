import pygame, random
from pong_game import Ball, Paddle, WIDTH, HEIGHT, BALL_RADIUS, PADDLE_SPEED
import os

def load_highscore():
    if os.path.exists("highscore.txt"):
        with open("highscore.txt", "r") as f:
            try:
                return int(f.read().strip())
            except:
                return 0
    return 0

def save_highscore(score):
    with open("highscore.txt", "w") as f:
        f.write(str(score))   
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

MAX_BALLS = 6
HITS_TO_SPLIT = 3
LIVES_PER_STAGE = 3

BRICK_WIDTH = 20
BRICK_HEIGHT = 40
FPS = 60    
# ---------------------- Brick Class ----------------------
class Brick:
    def __init__(self, x, y, hits=1, indestructible=False):
        self.rect = pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT)
        self.hits = hits
        self.indestructible = indestructible
        self.alive = True

    def hit(self, ball):
        """
        Handle collision with a ball.
        Returns True if the ball should reflect.
        """
        if self.indestructible:
            # Always reflect
            self.resolve_collision(ball)
            return True

        self.hits -= 1
        self.resolve_collision(ball)
        if self.hits <= 0:
            self.alive = False
        return True

    def resolve_collision(self, ball):
        """
        Pushes the ball completely outside the brick and reverses velocity.
        Works for destructible and indestructible bricks.
        """
        overlap_left = ball.x + BALL_RADIUS - self.rect.left
        overlap_right = self.rect.right - (ball.x - BALL_RADIUS)
        overlap_top = ball.y + BALL_RADIUS - self.rect.top
        overlap_bottom = self.rect.bottom - (ball.y - BALL_RADIUS)

        # Find the minimum overlap to separate ball
        min_overlap = min(overlap_left, overlap_right, overlap_top, overlap_bottom)

        if min_overlap == overlap_left:
            ball.x = self.rect.left - BALL_RADIUS
            ball.dx = -abs(ball.dx)
        elif min_overlap == overlap_right:
            ball.x = self.rect.right + BALL_RADIUS
            ball.dx = abs(ball.dx)
        elif min_overlap == overlap_top:
            ball.y = self.rect.top - BALL_RADIUS
            ball.dy = -abs(ball.dy)
        elif min_overlap == overlap_bottom:
            ball.y = self.rect.bottom + BALL_RADIUS
            ball.dy = abs(ball.dy)


    def draw(self, screen):
        if not self.alive:
            return
        if self.indestructible:
            color = (50, 50, 50)  # wall
            pygame.draw.rect(screen, color, self.rect, width=4)  # thicker border for walls
        elif self.hits == 2:
            color = (200, 100, 100)
            pygame.draw.rect(screen, color, self.rect, width=2)
        else:
            color = (200, 200, 200)
            pygame.draw.rect(screen, color, self.rect, width=2)




# ---------------------- Random Brick Generator ----------------------
# ---------------------- Random Brick Generator ----------------------
def generate_random_bricks(stage_index, right_clearance=80):
    bricks = []
    row_count = min(random.randint(5 + stage_index//2, 9 + stage_index//2), 13)  # cap at 13
    wall_chance = min(0.1 + 0.02 * stage_index, 0.3)
    strong_chance = min(0.3 + 0.05 * stage_index, 0.5)

    for r in range(row_count):
        # shift bricks so they don’t spawn flush against the right paddle
        x = WIDTH - right_clearance - (r + 1) * (BRICK_WIDTH + random.randint(15, 30))

        y = 0
        last_y = -100

        while y < HEIGHT - BRICK_HEIGHT:
            density_factor = 0.2 + 0.3 * (r / row_count)
            if random.random() < density_factor:
                indestructible = random.random() < wall_chance
                hits = 1 if indestructible else (2 if random.random() < strong_chance else 1)
                new_brick_rect = pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT)

                # check collision and vertical spacing
                collision = any(new_brick_rect.colliderect(b.rect) for b in bricks)
                if not collision and y - last_y >= BRICK_HEIGHT + 5:
                    bricks.append(Brick(x, y, hits, indestructible))
                    last_y = y

            y += BRICK_HEIGHT + random.randint(5, 20)

    return bricks






# ---------------------- Reset Stage ----------------------
def reset_stage(stage_index):
    balls = [Ball()]
    left_speed = PADDLE_SPEED
    right_speed = PADDLE_SPEED
    split_multiplier = 1.0
    hits_since_last_split = 0
    lives = LIVES_PER_STAGE
    bricks = generate_random_bricks(stage_index)
    return balls, bricks, left_speed, right_speed, split_multiplier, hits_since_last_split, lives

# ---------------------- HUD ----------------------
def draw_hud(screen, stage, lives, bricks, goals):
    font = pygame.font.SysFont("Arial", 24, bold=True)
    hud_text = f"Stage: {stage}   Lives: {lives}   Bricks left: {len(bricks)}   Goals: {goals}"
    text_surface = font.render(hud_text, True, WHITE)
    screen.blit(text_surface, (20, 20))

# ---------------------- AI Movement ----------------------
import random

def ai_move(paddle, balls, speed):
    """
    AI paddle movement (slightly easier than medium difficulty).
    Predicts the ball's Y position but reacts with smoothing and random error.
    """
    # Balls moving toward AI (right paddle)
    incoming_balls = [ball for ball in balls if ball.dx > 0]
    if not incoming_balls:
        return  # no threat, stay put

    # Choose closest incoming ball
    target = min(incoming_balls, key=lambda b: WIDTH - b.x)

    # Predict Y position at paddle's x
    if target.dx != 0:
        frames_to_reach = (paddle.rect.left - target.x) / target.dx
        predicted_y = target.y + target.dy * frames_to_reach
    else:
        predicted_y = target.y

    # Add random prediction error to make AI less perfect
    predicted_y += random.randint(-25, 25)  # ±25 px miss

    # Clamp inside screen
    predicted_y = max(0, min(HEIGHT, predicted_y))

    # Weighted smoothing: more weight to current paddle position (slower reaction)
    target_y = (paddle.rect.centery * 3 + predicted_y) / 4

    # Move toward target with capped speed
    max_move = speed - 1  # slightly slower than player
    if paddle.rect.centery < target_y - 5:
        paddle.rect.y += max_move
    elif paddle.rect.centery > target_y + 5:
        paddle.rect.y -= max_move

    # Keep paddle inside screen
    paddle.rect.y = max(0, min(HEIGHT - paddle.rect.height, paddle.rect.y))








# ---------------------- Campaign Loop ----------------------

def run_campaign():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    left_paddle = Paddle(20, HEIGHT//2 - 50)
    right_paddle = Paddle(WIDTH - 30, HEIGHT//2 - 50)
    # --- Internal Game Over Screen ---
    def game_over_screen():
        font = pygame.font.Font(None, 50)
        while True:
            screen.fill(BLACK)
            title = font.render("GAME OVER", True, WHITE)
            restart_text = font.render("Press R to Restart", True, WHITE)
            quit_text = font.render("Press Q to Quit", True, WHITE)

            screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//3))
            screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2))
            screen.blit(quit_text, (WIDTH//2 - quit_text.get_width()//2, HEIGHT//2 + 60))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        return "restart"
                    elif event.key == pygame.K_q:
                        return "quit"
            clock.tick(FPS)
    # --- Pause Menu ---
    def pause_menu():
        font = pygame.font.Font(None, 50)
        while True:
            screen.fill(BLACK)
            title = font.render("PAUSED", True, WHITE)
            resume_text = font.render("Press R to Resume", True, WHITE)
            quit_text = font.render("Press Q to Quit to Main Menu", True, WHITE)

            screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//3))
            screen.blit(resume_text, (WIDTH//2 - resume_text.get_width()//2, HEIGHT//2))
            screen.blit(quit_text, (WIDTH//2 - quit_text.get_width()//2, HEIGHT//2 + 60))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        return "resume"
                    elif event.key == pygame.K_q:
                        return "quit"
            clock.tick(FPS)
    # --- Load highscore ---
    highscore = load_highscore()            
    stage_index = 1
    balls, bricks, left_speed, right_speed, split_multiplier, hits_since_last_split, lives = reset_stage(stage_index)
    base_speed = PADDLE_SPEED
    goals = 0

    running = True
    while running:
        dt = clock.get_time() / 1000  # seconds
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    action = pause_menu()
                    if action == "quit":
                        return

        # --- Player input ---
        keys = pygame.key.get_pressed()
        if keys[pygame.K_s]: left_paddle.move(-left_speed)
        if keys[pygame.K_w]: left_paddle.move(left_speed)
        if keys[pygame.K_SPACE]:
            left_paddle.activate_full_height()
        # --- Update paddle timers ---
        left_paddle.update(dt)            
        # --- AI ---
        ai_move(right_paddle, balls, right_speed)

        # --- Ball update ---
        for ball in balls[:]:
            ball.move()

            # lose life if ball goes past left
            if ball.x < 0:
                lives -= 1
                if lives > 0:
                    ball.reset()
                    left_paddle.rect.centery = HEIGHT//2
                    right_paddle.rect.centery = HEIGHT//2
                else:
                    game_over_screen()  # This works because it is already the lambda
                    return
                break

            # win: score against right
            if ball.x > WIDTH:
                goals += 1
                print(f"✅ Stage {stage_index} cleared!")
                stage_index += 1
                # --- Update highscore ---
                if stage_index > highscore:
                    highscore = stage_index
                    save_highscore(highscore)

                balls, bricks, left_speed, right_speed, split_multiplier, hits_since_last_split, lives = reset_stage(stage_index)
                left_paddle.rect.centery = HEIGHT//2
                right_paddle.rect.centery = HEIGHT//2
                goals = 0
                break

            # paddle collisions
            if ball.check_collision(left_paddle, True) or ball.check_collision(right_paddle, False):
                hits_since_last_split += 1

            for brick in bricks[:]:
                if brick.alive and brick.rect.colliderect(
                        pygame.Rect(ball.x - BALL_RADIUS, ball.y - BALL_RADIUS, BALL_RADIUS*2, BALL_RADIUS*2)):
                    brick.hit(ball)  # pass the ball here
                    if not brick.alive:
                        bricks.remove(brick)
                    break

        # --- Ball splitting ---
        if hits_since_last_split >= HITS_TO_SPLIT:
            hits_since_last_split = 0
            if len(balls) < MAX_BALLS:
                balls.append(Ball())
                if split_multiplier < 3.0:
                    split_multiplier += 0.2
                    left_speed = min(base_speed * split_multiplier, base_speed*3)
                    right_speed = min(base_speed * split_multiplier, base_speed*3)

        # --- Draw ---
        screen.fill(BLACK)
        left_paddle.draw(screen)
        right_paddle.draw(screen)
        for ball in balls: ball.draw(screen)
        for brick in bricks: brick.draw(screen)
        draw_hud(screen, stage_index, lives, bricks, goals)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
