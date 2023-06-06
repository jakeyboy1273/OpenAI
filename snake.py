import pygame
import random

# Initialize pygame
pygame.init()

# Set the game window dimensions
window_width = 500
window_height = 500
game_window = pygame.display.set_mode((window_width, window_height))

# Set the game window title
pygame.display.set_caption("Snake Game")

# Set the game clock
clock = pygame.time.Clock()

# Set the game fonts
font = pygame.font.SysFont(None, 30)

# Set the snake block size
block_size = 10

# Define the function to display the message on the screen
def message_on_screen(msg, color):
    screen_text = font.render(msg, True, color)
    game_window.blit(screen_text, [window_width/6, window_height/3])

# Define the function to update the snake
def update_snake(block_size, snake_list):
    for block in snake_list:
        pygame.draw.rect(game_window, (0, 255, 0), [block[0], block[1], block_size, block_size])

# Define the game loop
def game_loop():
    game_over = False
    game_close = False

    # Set the initial snake position
    x1 = window_width/2
    y1 = window_height/2

    # Set the initial change in position
    x1_change = 0       
    y1_change = 0

    # Create the initial snake list
    snake_list = []
    length_of_snake = 1

    # Set the initial food position
    foodx = round(random.randrange(0, window_width - block_size) / 10.0) * 10.0
    foody = round(random.randrange(0, window_height - block_size) / 10.0) * 10.0

    # Start the game loop
    while not game_over:

        # Check for events
        while game_close == True:
            game_window.fill((255, 255, 255))
            message_on_screen("You lost! Press Q-Quit or C-Play Again", (255, 0, 0))
            pygame.display.update()

            # Check for key presses
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        # Check for key presses
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -block_size
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = block_size
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -block_size
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = block_size
                    x1_change = 0

        # Check for boundaries
        if x1 >= window_width or x1 < 0 or y1 >= window_height or y1 < 0:
            game_close = True

        # Update the position of the snake
        x1 += x1_change
        y1 += y1_change

        # Fill the game window
        game_window.fill((255, 255, 255))

        # Draw the food
        pygame.draw.rect(game_window, (255, 0, 0), [foodx, foody, block_size, block_size])

        # Create the snake head and body
        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_list.append(snake_head)

        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for block in snake_list[:-1]:
            if block == snake_head:
                game_close = True

        # Update the snake
        update_snake(block_size, snake_list)

        # Update the score
        pygame.display.update()

        # Check for collision with food
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, window_width - block_size) / 10.0) * 10.0
            foody = round(random.randrange(0, window_height - block_size) / 10.0) * 10.0
            length_of_snake += 1

        # Set the game clock
        clock.tick(20)

    # Quit pygame
    pygame.quit()

    # Quit the program
    quit()

# Call the game loop function
game_loop()

# Set the initial score
score = 0

# Define the function to display the score on the screen
def display_score(score):
    score_text = font.render("Score: " + str(score), True, (0, 0, 0))
    game_window.blit(score_text, [0, 0])

# Check for collision with food
if x1 == foodx and y1 == foody:
    foodx = round(random.randrange(0, window_width - block_size) / 10.0) * 10.0
    foody = round(random.randrange(0, window_height - block_size) / 10.0) * 10.0
    length_of_snake += 1
    score += 10

# Inside the game loop, call the display_score function
display_score(score)