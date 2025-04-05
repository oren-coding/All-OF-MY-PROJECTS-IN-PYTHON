import pygame
import sys
import random

pygame.init()

# Set up the window
window = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Pygame")
clock = pygame.time.Clock()

# Set up the player
player = pygame.Rect(100, 100, 50, 50)
player_color = (173, 216, 230)  # Light blue color
speed = 5

# Set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)

# Set up the fonts
font = pygame.font.Font(None, 36)

# Set up the text
text = font.render("Hello, Pygame!", True, BLACK)  # Change text color to black for visibility
text_rect = text.get_rect()
text_rect.center = (400, 300)

# Button function
def draw_button(surface, color, rect, text):
    pygame.draw.rect(surface, color, rect)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=rect.center)
    surface.blit(text_surface, text_rect)

# Button rectangles
button1 = pygame.Rect(50, 500, 200, 50)
button2 = pygame.Rect(300, 500, 200, 50)
button3 = pygame.Rect(550, 500, 200, 50)
button4 = pygame.Rect(50, 400, 200, 50)

# Variable to store button press status
button_pressed = ""

# Set up the game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button1.collidepoint(event.pos):
                # Change player color to a random color
                player_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                button_pressed = "Changed Player Color!"
            elif button2.collidepoint(event.pos):
                # Reset player position
                player.x, player.y = 100, 100
                button_pressed = "Reset Player Position!"
            elif button3.collidepoint(event.pos):
                # Increase player speed
                speed += 1
                button_pressed = "Increased Speed!"
            elif button4.collidepoint(event.pos):
                # Decrease player speed
                speed = max(1, speed - 1)  # Ensure speed doesn't go below 1
                button_pressed = "Decreased Speed!"

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= speed
    if keys[pygame.K_RIGHT]:
        player.x += speed
    if keys[pygame.K_UP]:
        player.y -= speed
    if keys[pygame.K_DOWN]:
        player.y += speed

    window.fill(WHITE)  # Change window background to white
    window.blit(text, text_rect)
    pygame.draw.rect(window, player_color, player)
    
    mouse_pos = pygame.mouse.get_pos()
    player_pos = (player.x, player.y)

    # Draw buttons
    draw_button(window, GRAY, button1, "Change Color")
    draw_button(window, GRAY, button2, "Reset Position")
    draw_button(window, GRAY, button3, "Increase Speed")
    draw_button(window, GRAY, button4, "Decrease Speed")

    # Display button press status
    if button_pressed:
        status_text = font.render(button_pressed, True, BLACK)
        status_rect = status_text.get_rect(center=(400, 400))
        window.blit(status_text, status_rect)

    # Display mouse position
    mouse_pos_text = font.render(f"Mouse position: {mouse_pos}", True, BLACK)
    mouse_pos_rect = mouse_pos_text.get_rect(center=(400, 450))
    window.blit(mouse_pos_text, mouse_pos_rect)

    # Display player position
    player_pos_text = font.render(f"Player position: {player_pos}", True, BLACK)
    player_pos_rect = player_pos_text.get_rect(center=(400, 500))
    window.blit(player_pos_text, player_pos_rect)
    
    pygame.display.flip()
    clock.tick(60)