import pygame
import random
import sys

pygame.init()

width = 500
height = 500

screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()

# Colors
white = (255,255,255)
red = (255,0,0)
black = (0,0,0)

# Game variables
snake_pos = [100,50]
snake_body = [[100,50],[90,50],[80,50]]

food_pos = [random.randrange(1,50)*10,random.randrange(1,50)*10]
food_spawn = True

direction = 'RIGHT'
change_to = direction

score = 0

# Game Over
def game_over():
    myFont = pygame.font.SysFont('monaco', 72)
    GOsurf = myFont.render('Game Over!', True, red)
    GOrect = GOsurf.get_rect()
    GOrect.midtop = (width/2, height/4)
    screen.blit(GOsurf,GOrect)
    show_score(0)
    pygame.display.flip()
    pygame.time.delay(1000)
    pygame.quit()
    sys.exit()

# Score
def show_score(choice=1):
    sfont = pygame.font.SysFont('monaco', 24)
    ssurf = sfont.render('Score : {0}'.format(score), True, black)
    srect = ssurf.get_rect()
    if choice == 1:
        srect.midtop = (width/2, 10)
    else:
        srect.midtop = (width/2, height/1.25)
    screen.blit(ssurf, srect)

# Main Logic
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                change_to = 'RIGHT'
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                change_to = 'LEFT'
            if event.key == pygame.K_UP or event.key == ord('w'):
                change_to = 'UP'
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                change_to = 'DOWN'
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    # validation of direction
    if change_to == 'RIGHT' and not direction == 'LEFT':
        direction = 'RIGHT'
    if change_to == 'LEFT' and not direction == 'RIGHT':
        direction = 'LEFT'
    if change_to == 'UP' and not direction == 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and not direction == 'UP':
        direction = 'DOWN'

    if direction == 'RIGHT':
        snake_pos[0] += 10
    if direction == 'LEFT':
        snake_pos[0] -= 10
    if direction == 'UP':
        snake_pos[1] -= 10
    if direction == 'DOWN':
        snake_pos[1] += 10

    # Snake body growing
    snake_body.insert(0, list(snake_pos))
    if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
        score += 1
        food_spawn = False
    else:
        snake_body.pop()

    # Food Spawn
    if food_spawn == False:
        food_pos = [random.randrange(1,50)*10,random.randrange(1,50)*10]
    food_spawn = True

    # Background
    screen.fill(white)

    # Draw Snake
    for pos in snake_body:
        pygame.draw.rect(screen, black, pygame.Rect(pos[0],pos[1],10,10))

    pygame.draw.rect(screen, red, pygame.Rect(food_pos[0],food_pos[1],10,10))

    # Game Over Conditions
    if snake_pos[0] < 0 or snake_pos[0] > width or snake_pos[1] < 0 or snake_pos[1] > height:
        game_over()

    for block in snake_body[1:]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            game_over()

    show_score()
    pygame.display.flip()
    clock.tick(20)

#Feature Scope: Generate a power-up that will double the score when picked up by the snake. 

# New Feature
power_up_pos = [random.randrange(1,50)*10,random.randrange(1,50)*10]
power_up_spawn = True

def power_up_score():
    global score
    score += score

# Main Logic
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                change_to = 'RIGHT'
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                change_to = 'LEFT'
            if event.key == pygame.K_UP or event.key == ord('w'):
                change_to = 'UP'
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                change_to = 'DOWN'
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    # validation of direction
    if change_to == 'RIGHT' and not direction == 'LEFT':
        direction = 'RIGHT'
    if change_to == 'LEFT' and not direction == 'RIGHT':
        direction = 'LEFT'
    if change_to == 'UP' and not direction == 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and not direction == 'UP':
        direction = 'DOWN'

    if direction == 'RIGHT':
        snake_pos[0] += 10
    if direction == 'LEFT':
        snake_pos[0] -= 10
    if direction == 'UP':
        snake_pos[1] -= 10
    if direction == 'DOWN':
        snake_pos[1] += 10

    # Snake body growing
    snake_body.insert(0, list(snake_pos))
    if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
        score += 1
        food_spawn = False
    else:
        snake_body.pop()
        
    # Power-Up
    if snake_pos[0] == power_up_pos[0] and snake_pos[1] == power_up_pos[1]:
        score += 3
        power_up_spawn = False
    
    # Power-Up Spawn
    if power_up_spawn == False:
        power_up_pos = [random.randrange(1,50)*10,random.randrange(1,50)*10]
    power_up_spawn = True

    # Food Spawn
    if food_spawn == False:
        food_pos = [random.randrange(1,50)*10,random.randrange(1,50)*10]
    food_spawn = True

    # Background
    screen.fill(white)

    # Draw Snake
    for pos in snake_body:
        pygame.draw.rect(screen, black, pygame.Rect(pos[0],pos[1],10,10))
        
    # Draw Power-Up
    pygame.draw.rect(screen, red, pygame.Rect(power_up_pos[0],power_up_pos[1],10,10))

    pygame.draw.rect(screen, red, pygame.Rect(food_pos[0],food_pos[1],10,10))

    # Game Over Conditions
    if snake_pos[0] < 0 or snake_pos[0] > width or snake_pos[1] < 0 or snake_pos[1] > height:
        game_over()

    for block in snake_body[1:]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            game_over()

    show_score()
    pygame.display.flip()
    clock.tick(20)