import win32gui
import win32con
import ctypes
import random
import time
import threading
import tkinter as tk
from tkinter import messagebox
import numpy as np
import pyaudio
import struct

# Make sure the process is DPI aware
user32 = ctypes.windll.user32
user32.SetProcessDPIAware()

# Get screen dimensions
sw, sh = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

# Global flag to control effects
running = True
current_effect = 1

# PyAudio setup
SAMPLE_RATE = 8000
p = pyaudio.PyAudio()

# Function to play bytebeat directly without creating files
def play_bytebeat(formula_type, duration=30):
    try:
        def callback(in_data, frame_count, time_info, status):
            if not running:
                return (None, pyaudio.paComplete)
            
            buffer = bytearray(frame_count)
            for i in range(frame_count):
                t = current_t[0]
                
                # Different formulas based on the type
                if formula_type == 1:
                    byte_value =  (t>>2)*(t>>5)|t>>5
                else:
                    byte_value =   2*(t>>5&t)-(t>>5)+t*(t>>14&14)
                
                buffer[i] = byte_value & 0xFF
                current_t[0] += 1
            
            return (bytes(buffer), pyaudio.paContinue)
        
        # Reset the time counter
        current_t[0] = 0
        
        # Open stream
        stream = p.open(
            format=pyaudio.paUInt8,
            channels=1,
            rate=SAMPLE_RATE,
            output=True,
            stream_callback=callback
        )
        
        stream.start_stream()
        print(f"Started bytebeat type {formula_type}")
        
        return stream
        
    except Exception as e:
        print(f"Error playing bytebeat: {e}")
        return None

# First GDI effect function (small shifts with NOTSRCCOPY)
def run_first_effect(duration=10):
    print("Starting first effect...")
    global current_effect
    current_effect = 1
    
    hdc = win32gui.GetDC(0)
    start_time = time.time()
    
    while time.time() - start_time < duration and running:
        try:
            win32gui.BitBlt(
                hdc,
                0,
                0,
                sw,
                sh,
                hdc,
                random.randrange(-3, 4),
                random.randrange(-3, 4),
                win32con.NOTSRCCOPY,
            )
            time.sleep(0.01)
        except Exception as e:
            print(f"Error in first effect: {e}")
            break
    
    win32gui.ReleaseDC(0, hdc)
    print("First effect completed")

# Second GDI effect function (larger random shifts with SRCCOPY)
def run_second_effect():
    print("Starting second effect...")
    global current_effect
    current_effect = 2
    
    while running:
        try:
            hdc = win32gui.GetDC(0)
            win32gui.BitBlt(
                hdc, 
                random.randint(-500, 500), 
                random.randint(-500, 500), 
                sw, 
                sh, 
                hdc, 
                random.randint(-500, 500), 
                random.randint(-500, 500), 
                win32con.SRCCOPY
            )
            win32gui.ReleaseDC(0, hdc)
            time.sleep(0.01)
        except Exception as e:
            print(f"Error in second effect: {e}")
            time.sleep(0.1)

# Main function to run the effects
def run_main():
    global running, current_t
    
    try:
        # Counter for the bytebeat generation
        current_t = [0]
        
        # Start first bytebeat
        stream1 = play_bytebeat(1)
        
        # Run first effect
        run_first_effect(10)
        
        # Close first stream and start second
        if stream1:
            stream1.stop_stream()
            stream1.close()
        
        # Start second bytebeat
        stream2 = play_bytebeat(2)
        
        # Run second effect
        run_second_effect()
        
        # Clean up
        if stream2:
            stream2.stop_stream()
            stream2.close()
            
    except Exception as e:
        print(f"Error in main function: {e}")
    finally:
        running = False
        p.terminate()

# Function to stop everything on exit
def cleanup():
    global running
    running = False
    try:
        p.terminate()
    except:
        pass

# Warning dialog
def show_warning():
    root = tk.Tk()
    root.withdraw()
    
    response = messagebox.askquestion(
        "Warning",
        "This program will create visual effects that rapidly change the screen's appearance and play sounds.\n\n"
        "Warning: These effects may potentially trigger seizures for people with photosensitive epilepsy.\n\n"
        "Do you want to continue?",
        icon='warning'
    )
    
    root.destroy()
    
    if response == 'yes':
        print("Starting effects...")
        # Run in a new thread
        thread = threading.Thread(target=run_main)
        thread.daemon = True
        thread.start()
        return True
    else:
        print("Program terminated by user.")
        return False

# Run the program
if __name__ == "__main__":
    try:
        if show_warning():
            # Keep the main thread alive
            try:
                while running:
                    time.sleep(0.1)
            except KeyboardInterrupt:
                print("Program terminated by user.")
    finally:
        cleanup()