import pygame
import random
import os



# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800 #size
SCREEN_HEIGHT = 600 #size
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Adventure")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Load spaceship image and resize it
spaceship_img = pygame.image.load('spaceship.png') #change this to your file path
spaceship_img = pygame.transform.scale(spaceship_img, (55, 55))  # Size of spaceship

# Load asteroid image and resize it
asteroid_img = pygame.image.load('asteroid.png') # change this to your file path
asteroid_img = pygame.transform.scale(asteroid_img, (65, 65))  #size of asteroid

# Font for text
font = pygame.font.SysFont(None, 36)

# File for high score
HIGH_SCORE_FILE = "high_score.txt"

def load_high_score():
    if os.path.exists(HIGH_SCORE_FILE):
        with open(HIGH_SCORE_FILE, "r") as file:
            try:
                return int(file.read().strip())
            except ValueError:
                return 0
    return 0

def save_high_score(score):
    with open(HIGH_SCORE_FILE, "w") as file:
        file.write(str(score))

def display_text(text, color, size, position):
    font = pygame.font.SysFont(None, size)
    rendered_text = font.render(text, True, color)
    screen.blit(rendered_text, position)

def level_selection():
    while True:
        screen.fill(BLACK)
        display_text("Select Level:", WHITE, 48, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 100))
        display_text("1. Easy", WHITE, 36, (SCREEN_WIDTH // 2 - 30, SCREEN_HEIGHT // 2 - 30))
        display_text("2. Medium", WHITE, 36, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2))
        display_text("3. Hard", WHITE, 36, (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 + 30))
        display_text("Press 1, 2, or 3 to select", WHITE, 24, (SCREEN_WIDTH // 2 - 90, SCREEN_HEIGHT // 2 + 90))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 1
                if event.key == pygame.K_2:
                    return 2
                if event.key == pygame.K_3:
                    return 3

def game_over(score, high_score):
    screen.fill(BLACK)
    display_text(f"Game Over! Your Score: {score}", RED, 48, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 100))
    display_text(f"High Score: {high_score}", WHITE, 36, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))
    display_text("Press R to Restart or Q to Quit", WHITE, 36, (SCREEN_WIDTH // 2 - 160, SCREEN_HEIGHT // 2 + 10))
    pygame.display.flip()

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting_for_input = False
                    return True  # Restart the game
                if event.key == pygame.K_q:
                    pygame.quit()
                    exit()

def main():
    clock = pygame.time.Clock()
    high_score = load_high_score()

    while True:
        score = 0
        spaceship_rect = spaceship_img.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60))
        asteroids = []

        # Level selection
        level = level_selection()

        # Set difficulty based on selected level
        if level == 1:
            spaceship_speed = 5
            asteroid_speed = 7
            asteroid_frequency = 25
            max_asteroids = 3
        elif level == 2:
            spaceship_speed = 4
            asteroid_speed = 10
            asteroid_frequency = 15
            max_asteroids = 5
        elif level == 3:
            spaceship_speed = 3
            asteroid_speed = 15
            asteroid_frequency = 10
            max_asteroids = 7

        # Wait for 3 seconds before starting the game
        pygame.time.wait(3000)  # Wait for 3000 milliseconds (3 seconds)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                spaceship_rect.x -= spaceship_speed
            if keys[pygame.K_RIGHT]:
                spaceship_rect.x += spaceship_speed
            
            # Ensure spaceship stays within screen boundaries
            spaceship_rect.x = max(0, min(SCREEN_WIDTH - spaceship_rect.width, spaceship_rect.x))
            
            # Add a new asteroid
            if random.randint(1, asteroid_frequency) == 1 and len(asteroids) < max_asteroids:
                new_asteroid = pygame.Rect(random.randint(0, SCREEN_WIDTH - 65), -65, 65, 65)  # Adjusted size
                asteroids.append(new_asteroid)

            # Move asteroids
            for asteroid in asteroids[:]:
                asteroid.y += asteroid_speed
                if asteroid.y > SCREEN_HEIGHT:
                    asteroids.remove(asteroid)
                    score += 1

            # Check for collisions
            for asteroid in asteroids:
                if spaceship_rect.colliderect(asteroid):
                    running = False

            # Draw everything
            screen.fill(BLACK)
            screen.blit(spaceship_img, spaceship_rect)
            for asteroid in asteroids:
                screen.blit(asteroid_img, asteroid)
            display_text(f"Score: {score}", WHITE, 36, (10, 10))

            pygame.display.flip()
            clock.tick(30)
        
        # Update high score if necessary
        if score > high_score:
            high_score = score
            save_high_score(high_score)

        # Game over screen
        if not game_over(score, high_score):
            break  # Exit the game loop if the user chose to quit

if __name__ == "__main__":
    main()
