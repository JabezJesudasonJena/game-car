import pygame
import random
import os
pygame.init()

WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Racing Game")


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)


player_car = pygame.image.load("player_car.png")
ai_car = pygame.image.load("ai_car.png")
road = pygame.image.load("road.png")


car_width, car_height = 70, 140  
player_car = pygame.transform.scale(player_car, (car_width, car_height))
ai_car = pygame.transform.scale(ai_car, (car_width, car_height))
road = pygame.transform.scale(road, (WIDTH, HEIGHT))


player_x, player_y = WIDTH // 2 - car_width // 2, HEIGHT - 150
ai_cars = []
num_ai_cars = 3
for _ in range(num_ai_cars):
    ai_cars.append([random.randint(100, WIDTH - 100 - car_width), random.randint(-600, -100)])


player_speed = 5
ai_speed = 3
road_speed = 5


score = 0
font = pygame.font.Font(None, 36)


def draw_score():
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))



road_y = 0


def check_collision():
    player_rect = pygame.Rect(player_x, player_y, car_width, car_height)
    for ai in ai_cars:
        ai_rect = pygame.Rect(ai[0], ai[1], car_width, car_height)
        if player_rect.colliderect(ai_rect):
            return True
    return False


def game_over_screen():
    screen.fill(WHITE)
    game_over_text = font.render("Game Over!", True, RED)
    final_score_text = font.render(f"Final Score: {score}", True, BLACK)
    restart_text = font.render("Press R to Restart or Q to Quit", True, BLACK)
    screen.blit(game_over_text, (WIDTH // 2 - 60, HEIGHT // 2 - 50))
    screen.blit(final_score_text, (WIDTH // 2 - 80, HEIGHT // 2))
    screen.blit(restart_text, (WIDTH // 2 - 150, HEIGHT // 2 + 50))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                if event.key == pygame.K_q:
                    pygame.quit()
                    exit()



running = True
clock = pygame.time.Clock()
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    road_y += road_speed
    if road_y >= HEIGHT:
        road_y = 0

    screen.blit(road, (0, road_y - HEIGHT))
    screen.blit(road, (0, road_y))

 
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - car_width:
        player_x += player_speed
    if keys[pygame.K_UP] and player_y > 0:
        player_y -= player_speed
    if keys[pygame.K_DOWN] and player_y < HEIGHT - car_height:
        player_y += player_speed


    for i in range(len(ai_cars)):
        ai_cars[i][1] += ai_speed
        if ai_cars[i][1] > HEIGHT:
            ai_cars[i] = [random.randint(100, WIDTH - 100 - car_width), random.randint(-600, -100)]
            score += 1  


    if check_collision():
        if game_over_screen():
            player_x, player_y = WIDTH // 2 - car_width // 2, HEIGHT - 150
            ai_cars = [[random.randint(100, WIDTH - 100 - car_width), random.randint(-600, -100)] for _ in
                       range(num_ai_cars)]
            score = 0
            road_y = 0
            continue
        else:
            break

    
    screen.blit(player_car, (player_x, player_y))
    for ai in ai_cars:
        screen.blit(ai_car, (ai[0], ai[1]))

    
    draw_score()

    pygame.display.update()
    clock.tick(30)

pygame.quit()
