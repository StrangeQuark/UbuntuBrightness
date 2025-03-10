import subprocess
import tkinter as tk
from tkinter import ttk

def get_connected_displays():
    query = subprocess.check_output(["xrandr", "--query"], universal_newlines=True)
    return [line.split()[0] for line in query.splitlines() if "connected" in line]

def get_current_brightness():
    query = subprocess.check_output(["xrandr", "--verbose"], universal_newlines=True)
    # Find the line with the brightness value and return it
    for line in query.splitlines():
        if "Brightness" in line:
            return float(line.split(":")[1].strip())
    return 1.0  # Default to 100% if not found

def set_brightness(brightness):
    for device in get_connected_displays():
        # Set the brightness of each connected display
        subprocess.run(["xrandr", "--output", device, "--brightness", str(brightness)])

def on_slider_change(value):
    brightness = float(value) / 100  # Convert slider value to a percentage (0-1 range)
    set_brightness(brightness)

def set_100_percent():
    slider.set(100)  # Set the slider to 100%
    set_brightness(1.0)  # 100% brightness

def set_75_percent():
    slider.set(75)  # Set the slider to 75%
    set_brightness(0.75)  # 75% brightness

def set_50_percent():
    slider.set(50)  # Set the slider to 50%
    set_brightness(0.5)  # 50% brightness

def set_25_percent():
    slider.set(25)  # Set the slider to 25%
    set_brightness(0.25)  # 25% brightness

def on_slider_value_change(value):
    # Don't allow the slider to go below 10
    if float(value) < 10:
        value = 10
    # Update brightness based on slider value (without recursively setting the slider)
    on_slider_change(value)

# Create the main window
root = tk.Tk()
root.title("Brightness Controller")

# Create a label
label = tk.Label(root, text="Adjust Brightness:")
label.pack(pady=10)

# Get the current brightness at the time of launching
current_brightness = get_current_brightness()
slider_value = current_brightness * 100  # Convert to a percentage

# Create the slider for adjusting brightness
slider = ttk.Scale(root, from_=10, to=100, orient="horizontal", command=on_slider_value_change)
slider.set(slider_value)  # Set the slider to the current brightness level
slider.pack(pady=10)

# Create buttons for 100%, 75%, 50%, and 25% brightness
button_100 = tk.Button(root, text="100%", command=set_100_percent)
button_100.pack(side="left", padx=10, pady=10)

button_75 = tk.Button(root, text="75%", command=set_75_percent)
button_75.pack(side="left", padx=10, pady=10)

button_50 = tk.Button(root, text="50%", command=set_50_percent)
button_50.pack(side="left", padx=10, pady=10)

button_25 = tk.Button(root, text="25%", command=set_25_percent)
button_25.pack(side="right", padx=10, pady=10)

# Run the Tkinter event loop
root.mainloop()
