import pygame
import random
import os
pygame.init()
pygame.mixer.init()  # Ensure mixer is initialized


# Colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)

# Screen dimensions
screen_width = 900
screen_height = 600

gameWindow = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("SnakeWithDeep")
pygame.display.update()

# background image

bgimg = pygame.image.load("bg.jpeg")
bgimg = pygame.transform.scale(bgimg, (screen_width, screen_height)).convert_alpha()

# Initialize font globally
font = pygame.font.SysFont(None, 55)

# Check if high score file exists, if not, create it
if not os.path.exists("hs.txt"):
    with open("hs.txt", "w") as f:
        f.write("0")

# Read high score from file
with open("hs.txt", "r") as f:
    highscore = f.read()

# Load and play background music
try:
    pygame.mixer.music.load("saaho_bgm.mp3")  # Ensure the file path is correct
    pygame.mixer.music.set_volume(0.5)  # Set volume (0.0 to 1.0)
    pygame.mixer.music.play(-1)  # Play music in a loop
except pygame.error as e:
    print(f"Error loading background music: {e}")

# Load blast sound effect
try:
    blast_sound = pygame.mixer.Sound("blast.mp3")  # Ensure the file path is correct
    blast_sound.set_volume(0.7)  # Set volume (0.0 to 1.0)
except pygame.error as e:
    print(f"Error loading blast sound: {e}")

def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])

def plot_snake(gameWindow, black, snk_list, snake_size):
    for x in snk_list:
        pygame.draw.rect(gameWindow, black, [x[0], x[1], snake_size, snake_size])

def welcome():
    exit_game = False
    while not exit_game:
        # Fill the game window with white color
        gameWindow.fill(white)
        
        # Display welcome messages
        text_screen("Welcome to Snake Game", black, 260, 250)
        text_screen("Press Space Bar to Play", red, 237, 290)
        
        # Update the display
        pygame.display.update()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True  # Exit the game

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit_game = True  # Exit the game

                if event.key == pygame.K_SPACE:  # Start the game when Space is pressed
                    gameloop()  # Call the game loop
def gameloop():
    # Game variables
    exit_game = False
    game_over = False
    blast_played = False  # Flag to ensure blast sound plays only once

    snake_x = 45
    snake_y = 55
    velocity_x = 0
    velocity_y = 0
    init_velocity = 5
    score = 0

    snake_size = 10
    fps = 60

    # Use highscore instead of hiscore
    global highscore
    highscore = int(highscore)  # Convert highscore to integer

    # Initialize food position
    food_x = random.randint(0, screen_width - snake_size)
    food_y = random.randint(0, screen_height - snake_size)

    # Initialize snake variables
    snk_list = []
    snk_length = 1  # Initialize snake length

    clock = pygame.time.Clock()

    while not exit_game:
        if game_over:
            # Stop background music and play blast sound only once
            if not blast_played:
                pygame.mixer.music.stop()
                blast_sound.play()  # Play the blast sound once
                blast_played = True  # Set the flag to True after playing the sound

            # Write high score to file
            with open("hs.txt", "w") as f:
                f.write(str(highscore))
                
            gameWindow.fill(white)
            gameWindow.blit(bgimg, (0, 0))  # Draw the background image
            text_screen("Game Over! Press Enter to Play Again", black, 100, 250)
            text_screen("Score: " + str(score), red, 100, 300)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # Restart game on Enter key
                        pygame.mixer.music.play(-1)  # Restart background music
                        gameloop()

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0  # Reset vertical velocity

                    if event.key == pygame.K_LEFT:
                        velocity_x = -init_velocity
                        velocity_y = 0  # Reset vertical velocity

                    if event.key == pygame.K_UP:
                        velocity_y = -init_velocity
                        velocity_x = 0  # Reset horizontal velocity

                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0  # Reset horizontal velocity
                        
                    if event.key == pygame.K_q:
                        score += 600    

            # Update snake position
            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y

            # Check for collision with food
            if abs(snake_x - food_x) < 6 and abs(snake_y - food_y) < 6:
                score += 10
                print("Score: ", score)
                
                food_x = random.randint(0, screen_width - snake_size)
                food_y = random.randint(0, screen_height - snake_size)
                snk_length += 5  # Increase snake length

                # Update high score
                if score > highscore:
                    highscore = score
              
            # Check for collision with boundaries (game over condition)
            if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
                game_over = True
                print("Game Over!")

            # Fill the game window with white color
            gameWindow.fill(white)
            text_screen("Score: " + str(score) + "  Hiscore: " + str(highscore), red, 5, 5)
            # Draw the food
            pygame.draw.rect(gameWindow, black, [food_x, food_y, snake_size, snake_size])
            
            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list) > snk_length:
                del snk_list[0]
                
            if head in snk_list[:-1]:
                game_over = True
                print("Game Over!")    

            # Draw the snake
            plot_snake(gameWindow, black, snk_list, snake_size)

            # Update the display
            pygame.display.update()

            # Control the frame rate
            clock.tick(fps)

    pygame.quit()
    quit()

welcome()