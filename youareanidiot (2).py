import pygame
import random
import sys
import time
import os
import math
from pygame.locals import *

def main():
    pygame.init()
    pygame.mixer.init()

    # Set up the window
    info = pygame.display.Info()
    screen_width, screen_height = info.current_w, info.current_h
    flags = FULLSCREEN | NOFRAME
    screen = pygame.display.set_mode((screen_width, screen_height), flags)
    pygame.display.set_caption("You are an idiot!")

    # Create font for download button
    button_font = pygame.font.SysFont('Arial', 24)
    download_button = pygame.Rect(screen_width - 200, screen_height - 50, 180, 40)

    # Set up the clock
    clock = pygame.time.Clock()

    # Load sound
    try:
        sound_path = os.path.join("attached_assets", "sounds.mp3")
        sound = pygame.mixer.Sound(sound_path)
    except:
        print("Could not load sound file.")
        sound = None

    # Set up colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)

    # Set up fonts
    font = pygame.font.SysFont('Comic Sans MS', 48)

    # Create smile faces
    def create_smile(color, bg_color, size):
        surf = pygame.Surface((size, size))
        surf.fill(bg_color)

        # Draw the circle (face)
        pygame.draw.circle(surf, color, (size//2, size//2), size//2 - 5)

        # Draw the eyes
        eye_size = size // 8
        eye_pos_y = size // 3
        left_eye_pos = (size // 3, eye_pos_y)
        right_eye_pos = (size - size // 3, eye_pos_y)

        pygame.draw.circle(surf, bg_color, left_eye_pos, eye_size)
        pygame.draw.circle(surf, bg_color, right_eye_pos, eye_size)

        # Draw the smile
        smile_rect = pygame.Rect(size//4, size//2, size//2, size//3)
        pygame.draw.arc(surf, bg_color, smile_rect, 0, math.pi, 5)

        return surf

    # Create black and white smiles
    smile_size = 100
    black_smile = create_smile(BLACK, WHITE, smile_size)
    white_smile = create_smile(WHITE, BLACK, smile_size)

    # Set up window parameters
    window_size = (400, 300)
    windows = []
    num_windows = 5

    # Create initial windows
    for i in range(num_windows):
        x = random.randint(0, screen_width - window_size[0])
        y = random.randint(0, screen_height - window_size[1])
        dx = random.choice([-4, -3, 3, 4])
        dy = random.choice([-4, -3, 3, 4])
        windows.append({
            'rect': pygame.Rect(x, y, *window_size), 
            'dx': dx, 
            'dy': dy,
            'flash_state': random.choice([True, False]),  # True for white, False for black
            'flash_timer': 0
        })

    # Set up flash timer
    flash_interval = 15  # frames between flashes

    # Set up text message
    text = font.render("YOU ARE AN IDIOT!", True, BLACK, YELLOW)
    text_rect = text.get_rect()

    # Play sound
    if sound:
        sound.play(-1)  # Loop the sound

    running = True
    frame_count = 0

    while running:
        frame_count += 1

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        # Clear screen
        screen.fill(BLACK)

        # Update and draw windows
        for window in windows:
            # Move the window
            window['rect'].x += window['dx']
            window['rect'].y += window['dy']

            # Bounce off edges
            if window['rect'].left < 0 or window['rect'].right > screen_width:
                window['dx'] *= -1
            if window['rect'].top < 0 or window['rect'].bottom > screen_height:
                window['dy'] *= -1

            # Handle flashing
            window['flash_timer'] += 1
            if window['flash_timer'] >= flash_interval:
                window['flash_state'] = not window['flash_state']
                window['flash_timer'] = 0

            # Choose background color based on flash state
            bg_color = WHITE if window['flash_state'] else BLACK
            border_color = RED

            # Draw the window
            pygame.draw.rect(screen, bg_color, window['rect'])
            pygame.draw.rect(screen, border_color, window['rect'], 3)

            # Draw the smile
            smile = white_smile if window['flash_state'] else black_smile
            smile_rect = smile.get_rect(center=window['rect'].center)
            screen.blit(smile, smile_rect)

            # Draw text above smile
            text = font.render("YOU ARE AN IDIOT!", True, 
                              BLACK if window['flash_state'] else WHITE, 
                              YELLOW)
            text_rect = text.get_rect(centerx=window['rect'].centerx, 
                                     bottom=smile_rect.top - 10)
            screen.blit(text, text_rect)

        # Draw download button
        pygame.draw.rect(screen, (0, 0, 255), download_button) # Blue button
        button_text = button_font.render("Download Site", True, (255, 255, 255)) # White text
        text_rect = button_text.get_rect(center=download_button.center)
        screen.blit(button_text, text_rect)


        pygame.display.flip()
        clock.tick(60)

    # Clean up
    if sound:
        sound.stop()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()