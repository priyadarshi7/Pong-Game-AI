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

def get_state(ball_x, ball_y, paddle_y):
    if ball_x > WIDTH / 2:
        if ball_y < paddle_y:
            return 0  
        elif ball_y > paddle_y + PADDLE_HEIGHT:
            return 1  
        else:
            return 2  
    else:
        return 0  

def choose_action(state):
    if np.random.rand() < epsilon:
        return random.choice(range(num_actions))  
    else:
        return np.argmax(q_table[state])

def update_q_table(state, action, reward, next_state):
    q_value = q_table[state][action]
    max_next_q_value = np.max(q_table[next_state])
    new_q_value = q_value + learning_rate * (reward + discount_factor * max_next_q_value - q_value)
    q_table[state][action] = new_q_value


username = text_input("Enter your username: ")

player_paddle = Paddle(WIDTH - PADDLE_WIDTH - 10, HEIGHT // 2 - PADDLE_HEIGHT // 2)
ai_paddle = Paddle(10, HEIGHT // 2 - PADDLE_HEIGHT // 2)
ball = Ball()


num_states = 3  
num_actions = 2  
q_table = np.zeros((num_states, num_actions))  
learning_rate = 0.1
discount_factor = 0.9
epsilon = 0.1

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

    state = get_state(ball.rect.x, ball.rect.y, ai_paddle.rect.y)
    action = choose_action(state)
    if action == 0:
        if ball.rect.centery < ai_paddle.rect.centery + PADDLE_HEIGHT / 2:
            ai_paddle.move(-1)
        else:
            ai_paddle.move(1)

    ball.move()

    if ball.rect.colliderect(player_paddle.rect):
        ball.speed[0] *= -1
    elif ball.rect.colliderect(ai_paddle.rect):
        ball.speed[0] *= -1

    if ball.rect.left <= 0:
        ai_score += 1
        ball.reset()
    elif ball.rect.right >= WIDTH:
        player_score += 1
        ball.reset()

    screen.blit(background_image, (0, 0))

    player_paddle.draw()
    ai_paddle.draw()
    ball.draw()

    username_text = font.render(username, True, WHITE)
    username_rect = username_text.get_rect(center=(WIDTH // 2, 20))
    screen.blit(username_text, username_rect)

    player_score_text = font.render(username + ":"+ str(ai_score), True, WHITE)
    player_score_rect = player_score_text.get_rect(topright=(WIDTH - 20, 20))
    screen.blit(player_score_text, player_score_rect)

    ai_score_text = font.render("AI: " + str(player_score), True, WHITE)
    ai_score_rect = ai_score_text.get_rect(topleft=(20, 20))
    screen.blit(ai_score_text, ai_score_rect)

    pygame.display.flip()

    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()
