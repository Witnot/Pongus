import pygame
from pong_game import start_game, start_game1
from campaign import run_campaign, load_highscore, save_highscore   



# ---------------------- Constants ----------------------
WIDTH, HEIGHT = 800, 600
WHITE, BLACK = (255, 255, 255), (0, 0, 0)
FPS = 60

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Menu")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 50)

# ---------------------- Game Over Screen ----------------------

# ---------------------- Difficulty Menu ----------------------
def difficulty_menu(current):
    selected = ["Easy", "Medium", "Hard"].index(current)
    running = True
    while running:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % 3
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % 3
                elif event.key == pygame.K_RETURN:
                    return ["Easy", "Medium", "Hard"][selected]
                elif event.key == pygame.K_ESCAPE:
                    return current

        for i, level in enumerate(["Easy", "Medium", "Hard"]):
            color = WHITE if i == selected else (150, 150, 150)
            text = font.render(level, True, color)
            screen.blit(text, (WIDTH//2 - text.get_width()//2, 200 + i*70))

        pygame.display.flip()
        clock.tick(FPS)

# ---------------------- Campaign Start Wrapper ----------------------
def show_rules():
    """
    Displays the rules/mechanics of the game.
    """
    running = True
    font_title = pygame.font.SysFont("Arial", 48)
    font_text = pygame.font.SysFont("Arial", 28)

    rules_lines = [
        "Player 1 (Left Paddle): W = Up, S = Down, SPACE = Full-height boost",
        "Player 2 (Right Paddle): Up/Down arrows = Move, Left arrow = Full-height boost",
        "New Balls spawn at the center after every 4 paddle hits",
        "Score 15 points to win a round",
        "First player to win 3 rounds wins the game",
        "Bricks Mode: Break all bricks to advance levels",
        "Press ESC to return to Main Menu"
    ]

    while running:
        screen.fill(BLACK)
        title_surf = font_title.render("Rules & Mechanics", True, (255, 255, 255))
        screen.blit(title_surf, (WIDTH // 2 - title_surf.get_width() // 2, 50))

        # Draw rules lines
        for i, line in enumerate(rules_lines):
            line_surf = font_text.render(line, True, (200, 200, 200))
            screen.blit(line_surf, (50, 150 + i * 40))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False  # return to main menu

# ---------------------- Main Menu ----------------------
def main_menu():
    selected = 0
    options = ["Start Game", "Player vs Player", "Bricks Endless", "Rules", "Difficulty", "Quit"]
    difficulty = "Medium"
    running = True

    # Load highscore once at menu startup
    highscore = load_highscore()

    while running:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if options[selected] == "Start Game":
                        start_game(difficulty)
                    elif options[selected] == "Bricks Endless":
                        run_campaign()
                        # refresh highscore after playing campaign
                        highscore = load_highscore()
                    elif options[selected] == "Player vs Player":
                        start_game1()                          # uses wrapper
                    elif options[selected] == "Difficulty":
                        difficulty = difficulty_menu(difficulty)
                    elif options[selected] == "Rules":
                        show_rules()    
                    elif options[selected] == "Quit":
                        running = False

        # --- Draw menu options ---
        for i, option in enumerate(options):
            color = WHITE if i == selected else (150, 150, 150)
            text = font.render(option, True, color)
            screen.blit(text, (WIDTH//2 - text.get_width()//2, 200 + i*70))

        # --- Draw Highscore at top-right ---
        hs_text = font.render(f"Highscore: Stage {highscore}", True, WHITE)
        screen.blit(hs_text, (WIDTH - hs_text.get_width() - 20, 20))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


# ---------------------- Entry Point ----------------------
if __name__ == "__main__":
    main_menu()
