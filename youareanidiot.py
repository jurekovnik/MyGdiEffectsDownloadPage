import pygame
import random
import sys
import time
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
    
    # Set up the clock
    clock = pygame.time.Clock()
    
    # Load sound
    try:
        # Create a text-to-speech message
        from gtts import gTTS
        
        # Generate the audio file
        tts = gTTS("you are an idiot! ha ha ha ha ha ha ha ha ha ha!")
        tts.save("idiot_sound.mp3")
        
        # Load the sound
        sound = pygame.mixer.Sound("idiot_sound.mp3")
    except:
        # If text-to-speech fails, just print a message
        print("Could not create sound file. Run 'pip install gtts' to enable sound.")
        sound = None
    
    # Set up colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)
    
    # Set up fonts
    font = pygame.font.SysFont('Comic Sans MS', 48)
    
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
        windows.append({'rect': pygame.Rect(x, y, *window_size), 'dx': dx, 'dy': dy})
    
    # Set up text message
    text = font.render("YOU ARE AN IDIOT!", True, BLACK, YELLOW)
    text_rect = text.get_rect()
    
    # Play sound
    if sound:
        sound.play(-1)  # Loop the sound
    
    running = True
    while running:
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
            
            # Draw the window
            pygame.draw.rect(screen, WHITE, window['rect'])
            pygame.draw.rect(screen, RED, window['rect'], 3)
            
            # Position text in window
            text_rect.center = window['rect'].center
            screen.blit(text, text_rect)
        
        pygame.display.flip()
        clock.tick(60)
    
    # Clean up
    if sound:
        sound.stop()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()