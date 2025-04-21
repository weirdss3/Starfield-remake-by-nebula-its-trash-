import pygame
import random

# Initialize pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Starfield Game')

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Player spaceship class
class Player:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.speed = 5
        self.width = 30
        self.height = 40
        self.velocity_x = 0
        self.velocity_y = 0

    def move(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.x = max(0, min(WIDTH - self.width, self.x))
        self.y = max(0, min(HEIGHT - self.height, self.y))

    def draw(self, screen):
        pygame.draw.polygon(screen, WHITE, [
            (self.x + self.width // 2, self.y),
            (self.x, self.y + self.height),
            (self.x + self.width, self.y + self.height)
        ])

class Star:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.z = random.randint(1, 3)

    def move(self):
        self.z -= 0.1
        if self.z <= 0:
            self.z = random.randint(1, 3)
            self.x = random.randint(0, WIDTH)
            self.y = random.randint(0, HEIGHT)

# Create a list of stars
stars = [Star() for _ in range(200)]

# Initialize the player
player = Player()

# Game Loop
running = True
clock = pygame.time.Clock()

# Score variable
score = 0
font = pygame.font.SysFont(None, 36)

# Check for collision
def check_collision(player, stars):
    for star in stars:
        distance = ((player.x + player.width // 2 - star.x) ** 2 + (player.y + player.height // 2 - star.y) ** 2) ** 0.5
        if distance < 20:
            return True
    return False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    player.velocity_x = (-player.speed if keys[pygame.K_LEFT] or keys[pygame.K_a] else
                         player.speed if keys[pygame.K_RIGHT] or keys[pygame.K_d] else 0)
    player.velocity_y = (-player.speed if keys[pygame.K_UP] or keys[pygame.K_w] else
                         player.speed if keys[pygame.K_DOWN] or keys[pygame.K_s] else 0)

    player.move()
    for star in stars:
        star.move()

    if check_collision(player, stars):
        running = False

    score += 1

    screen.fill(BLACK)
    player.draw(screen)

    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

# Game Over screen
screen.fill(BLACK)
game_over_text = font.render("GAME OVER!", True, RED)
score_text = font.render(f"Final Score: {score}", True, WHITE)
screen.blit(game_over_text, (WIDTH // 3, HEIGHT // 3))
screen.blit(score_text, (WIDTH // 3, HEIGHT // 2))
pygame.display.flip()
pygame.time.wait(3000)

pygame.quit()
