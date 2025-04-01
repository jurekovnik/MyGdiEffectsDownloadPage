from win32api import *
from win32gui import *
import win32con
import time
import random

def main():
    # Initial position
    x, y = 100, 100
    # Movement direction
    signX, signY = 1, 1
    # Speed of movement
    incrementor = 5
    # Circle radius
    radius = 40
    
    try:
        while True:
            # Get screen dimensions and device context
            w, h = GetSystemMetrics(0), GetSystemMetrics(1)
            hdc = GetDC(0)
            
            # Generate random color
            color = random.randint(0, 255) | (random.randint(0, 255) << 8) | (random.randint(0, 255) << 16)
            
            # Create and select a brush with the random color
            brush = CreateSolidBrush(color)
            old_brush = SelectObject(hdc, brush)
            
            # Draw the circle
            Ellipse(hdc, x - radius, y - radius, x + radius, y + radius)
            
            # Clean up GDI resources
            SelectObject(hdc, old_brush)
            DeleteObject(brush)
            ReleaseDC(0, hdc)
            
            # Update position
            x += incrementor * signX
            y += incrementor * signY
            
            # Bounce off screen edges
            if y >= h - radius or y <= radius:
                signY *= -1
            if x >= w - radius or x <= radius:
                signX *= -1
                
            # Short delay
            time.sleep(0.01)
    
    except KeyboardInterrupt:
        # Allow for clean exit with Ctrl+C
        pass
    finally:
        # Clean up any remaining resources
        if 'hdc' in locals() and 'old_brush' in locals():
            SelectObject(hdc, old_brush)
        if 'brush' in locals():
            DeleteObject(brush)
        if 'hdc' in locals():
            ReleaseDC(0, hdc)

# Add a warning message before starting
def show_warning():
    MessageBox(0, 
               "This program will display a bouncing circle effect on your screen.\n\n"
               "Press Ctrl+C in the terminal window to exit the program.", 
               "GDI Effect Warning", 
               win32con.MB_OK | win32con.MB_ICONINFORMATION)

if __name__ == "__main__":
    show_warning()
    main()