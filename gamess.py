import pygame
import sys
import random
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
NAVY = (0,0,128)  # New color for text
IVORYBLACK = (41,36,33)  # New color for numbers

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Stock the Shelves - Coordinate Game")

# Load images
try:
    # Background images for intro, win, and fail screens
    intro_image = pygame.image.load("intro.png")  # Intro screen image
    intro_image = pygame.transform.scale(intro_image, (WIDTH, HEIGHT))
    win_image = pygame.image.load("win.png")  # Win screen image
    win_image = pygame.transform.scale(win_image, (WIDTH, HEIGHT))
    fail_image = pygame.image.load("fail.png")  # Fail screen image
    fail_image = pygame.transform.scale(fail_image, (WIDTH, HEIGHT))
    
    # Background image for the game
    background_image = pygame.image.load("intro_bg.png")  # Game background image
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
    
    # Load unique images for each product
    product_images = {
        "pizza": pygame.image.load("pizza.png"),
        "bread": pygame.image.load("bread.png"),
        "donut": pygame.image.load("donut.png"),
        "noodle": pygame.image.load("noodle.png"),
        "pie": pygame.image.load("pie.png"),
        "coffee": pygame.image.load("coffee.png"),
        "banana": pygame.image.load("banana.png"),
        "steak": pygame.image.load("steak.png"),
        "egg": pygame.image.load("egg.png"),
        "fries": pygame.image.load("fries.png"),
        "pancakes": pygame.image.load("pancakes.png"),
        "cake": pygame.image.load("cake.png"),
        "milktea": pygame.image.load("milktea.png"),
        "sandwich": pygame.image.load("sandwich.png"),
        "soda": pygame.image.load("soda.png"),
        "sushi": pygame.image.load("sushi.png"),
        "tacos": pygame.image.load("tacos.png"),
        "hotdog": pygame.image.load("hotdog.png"),
        "chocolate": pygame.image.load("chocolate.png"),
        "adobo": pygame.image.load("adobo.png"),
    }
    
    # Scale images to a consistent size
    for name, image in product_images.items():
        product_images[name] = pygame.transform.scale(image, (40, 40))
except pygame.error as e:
    print(f"Error loading image: {e}")
    sys.exit()

# Load sounds
try:
    pygame.mixer.music.load("background_music.mp3")  # Background music
    tap_sound = pygame.mixer.Sound("tap_sound.wav")  # Tap sound effect
except pygame.error as e:
    print(f"Error loading sound: {e}")
    sys.exit()

# Clock
clock = pygame.time.Clock()
FPS = 60

# Time limit for the game (in seconds)
time_limit = 120  # Set the time limit to 120 seconds (2 minutes)

# Convert Cartesian to screen coordinates
def cartesian_to_screen(x, y):
    screen_x = WIDTH // 2 + x * 50
    screen_y = HEIGHT // 2 - y * 50
    return screen_x - 20, screen_y - 20

# Convert screen to Cartesian coordinates
def screen_to_cartesian(screen_x, screen_y):
    x = round((screen_x - WIDTH // 2) / 50)
    y = round((HEIGHT // 2 - screen_y) / 50)
    return x, y

# Draw Cartesian grid
def draw_cartesian_plane():
    for x in range(-8, 9):
        screen_x = WIDTH // 2 + x * 50
        pygame.draw.line(screen, WHITE, (screen_x, 0), (screen_x, HEIGHT), 1)
        label = font.render(str(x), True, IVORYBLACK)  
        screen.blit(label, (screen_x - 10, HEIGHT // 2 + 5))

    for y in range(-6, 7):
        screen_y = HEIGHT // 2 - y * 50
        pygame.draw.line(screen, WHITE, (0, screen_y), (WIDTH, screen_y), 1)
        label = font.render(str(y), True, IVORYBLACK)  
        screen.blit(label, (WIDTH // 2 + 5, screen_y - 10))

    # Draw axes
    pygame.draw.line(screen, RED, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 2)
    pygame.draw.line(screen, RED, (0, HEIGHT // 2), (WIDTH, HEIGHT // 2), 2)

# Font
font = pygame.font.SysFont(None, 35)
input_font = pygame.font.SysFont(None, 30)

# Intro screen
def show_intro():
    intro = True
    while intro:
        screen.blit(intro_image, (0, 0))  # Display the intro image

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                intro = False

        pygame.display.flip()
        clock.tick(FPS)

# Game Over Outro
def game_over_outro(success):
    outro = True
    while outro:
        if success:
            screen.blit(win_image, (0, 0))  # Display the win image
        else:
            screen.blit(fail_image, (0, 0))  # Display the fail image

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Restart the game
                    return True
                if event.key == pygame.K_q:  # Quit the game
                    return False

        pygame.display.flip()
        clock.tick(FPS)

# Game variables
def reset_game():
    global shelves, found_products, start_time
    shelves = {
        "pizza": [random.randint(-5, 5), random.randint(-5, 5)],
        "bread": [random.randint(-5, 5), random.randint(-5, 5)],
        "donut": [random.randint(-5, 5), random.randint(-5, 5)],
        "noodle": [random.randint(-5, 5), random.randint(-5, 5)],
        "pie": [random.randint(-5, 5), random.randint(-5, 5)],
        "coffee": [random.randint(-5, 5), random.randint(-5, 5)],
        "banana": [random.randint(-5, 5), random.randint(-5, 5)],
        "steak": [random.randint(-5, 5), random.randint(-5, 5)],
        "egg": [random.randint(-5, 5), random.randint(-5, 5)],
        "fries": [random.randint(-5, 5), random.randint(-5, 5)],
        "pancakes": [random.randint(-5, 5), random.randint(-5, 5)],
        "cake": [random.randint(-5, 5), random.randint(-5, 5)],
        "milktea": [random.randint(-5, 5), random.randint(-5, 5)],
        "sandwich": [random.randint(-5, 5), random.randint(-5, 5)],
        "soda": [random.randint(-5, 5), random.randint(-5, 5)],
        "sushi": [random.randint(-5, 5), random.randint(-5, 5)],
        "tacos": [random.randint(-5, 5), random.randint(-5, 5)],
        "hotdog": [random.randint(-5, 5), random.randint(-5, 5)],
        "chocolate": [random.randint(-5, 5), random.randint(-5, 5)],
        "adobo": [random.randint(-5, 5), random.randint(-5, 5)],
    }
    found_products = {name: False for name in shelves}
    start_time = time.time()

def product_placement_phase():
    placement = True
    current_product_index = 0
    product_names = list(shelves.keys())

    # Play background music
    pygame.mixer.music.play(-1)  # -1 means loop indefinitely

    while placement:
        screen.blit(background_image, (0, 0))  # Display the game background image
        draw_cartesian_plane()

        # Calculate remaining time
        elapsed_time = time.time() - start_time
        remaining_time = max(0, time_limit - int(elapsed_time))
        timer_text = font.render(f"Time Left: {remaining_time} seconds", True, NAVY)  
        screen.blit(timer_text, (WIDTH - 200, 10))

        # Display current product and its coordinates
        current_product = product_names[current_product_index]
        product_coords = shelves[current_product]
        coord_text = font.render(f"Stock {current_product} at ({product_coords[0]}, {product_coords[1]})", True, NAVY)  # Change text color to YELLOW
        screen.blit(coord_text, (10, 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                clicked_x, clicked_y = screen_to_cartesian(mouse_x, mouse_y)
                print(f"Clicked coordinates: ({clicked_x}, {clicked_y})")
                # Play tap sound effect
                tap_sound.play()
                # Check if clicked coordinate matches the current product location
                if (clicked_x, clicked_y) == (product_coords[0], product_coords[1]):
                    print(f"Correct! You stocked {current_product} at ({product_coords[0]}, {product_coords[1]})")
                    found_products[current_product] = True
                    current_product_index += 1
                    if current_product_index >= len(product_names):
                        placement = False
                        break

        # Draw stocked products if they have been found
        for name, (x, y) in shelves.items():
            if found_products[name]:
                screen.blit(product_images[name], cartesian_to_screen(x, y))

        # End game if time runs out
        if remaining_time <= 0:
            print("Time's up! Game over.")
            placement = False

        pygame.display.flip()
        clock.tick(FPS)

    # Stop background music when the game ends
    pygame.mixer.music.stop()

    # Check if the player won or lost
    if all(found_products.values()):
        return True  # Player won
    else:
        return False  # Player lost

# Main game loop
def main():
    while True:
        show_intro()
        reset_game()
        success = product_placement_phase()
        if not game_over_outro(success):
            break  # Exit the game if the player chooses to quit

    pygame.quit()

# Run the game
if __name__ == "__main__":
    main()