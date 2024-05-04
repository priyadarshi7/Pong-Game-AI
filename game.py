import pygame
import numpy as np
import random
import sys

pygame.init()

WIDTH, HEIGHT = 600, 400
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 60
BALL_SIZE = 10
PADDLE_SPEED = 5
BALL_SPEED = 5
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
FONT_SIZE = 36

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

background_image = pygame.image.load("background.png").convert()
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

font = pygame.font.Font("freesansbold.ttf", FONT_SIZE)

def text_input(message):
    user_text = ""
    active = True
    while active:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    active = False
                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode

        screen.fill(BLACK)
        text_surface = font.render(message + user_text, True, WHITE)
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text_surface, text_rect)
        pygame.display.flip()

    return user_text

class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)

    def move(self, direction):
        self.rect.y += direction * PADDLE_SPEED
   
        self.rect.y = min(max(self.rect.y, 0), HEIGHT - PADDLE_HEIGHT)

    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect)


class Ball:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2, HEIGHT // 2, BALL_SIZE, BALL_SIZE)
        self.reset()

    def reset(self):
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.speed = [random.choice((-1, 1)) * BALL_SPEED, random.uniform(-1, 1) * BALL_SPEED]

    def move(self):
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]

        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed[1] *= -1

    def draw(self):
        pygame.draw.ellipse(screen, WHITE, self.rect)

player_paddle = Paddle(WIDTH - PADDLE_WIDTH - 10, HEIGHT // 2 - PADDLE_HEIGHT // 2)
ai_paddle = Paddle(10, HEIGHT // 2 - PADDLE_HEIGHT // 2)
ball = Ball()
username = text_input("Enter your username: ")

player_score = 0
ai_score = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        player_paddle.move(-1)
    if keys[pygame.K_DOWN]:
        player_paddle.move(1)

    if ball.speed[0] < 0:
        if random.random() < 0.7:
            if ball.rect.centery < ai_paddle.rect.centery:
                ai_paddle.move(-1)
            elif ball.rect.centery > ai_paddle.rect.centery:
                ai_paddle.move(1)

    elif random.random() < 0.3:
        ai_paddle.move(random.choice([-1, 1]))

    ball.move()

    if ball.rect.left <= 0:
        ai_score += 1
        ball.reset()
    elif ball.rect.right >= WIDTH:
        player_score += 1
        ball.reset()

    if ball.rect.colliderect(player_paddle.rect):
        ball.speed[0] *= -1
    elif ball.rect.colliderect(ai_paddle.rect):
        ball.speed[0] *= -1

    screen.blit(background_image, (0, 0))

    player_paddle.draw()
    ai_paddle.draw()
    ball.draw()

    player_text = font.render(username + ": " + str(ai_score), True, WHITE)
    player_text_rect = player_text.get_rect(topright=(WIDTH - 20, 20))
    screen.blit(player_text, player_text_rect)

    ai_text = font.render("AI: " + str(player_score), True, WHITE)
    ai_text_rect = ai_text.get_rect(topleft=(20, 20))
    screen.blit(ai_text, ai_text_rect)

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()
