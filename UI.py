import tkinter as tk
from tkinter import PhotoImage
from spell import correction  # Import the correction function from spell.py

# Function to handle button click and show the corrected word
def on_button_click():
    global message_label  # Declare message_label as a global variable
    # Read the text from the entry widget
    entered_text = entry_var.get()
    # Get the corrected word using the spell correction function
    corrected_word = correction(entered_text)
    # Destroy the previous message label, if it exists
    if message_label:
        message_label.destroy()
    # Create a label with the corrected word
    message_label = tk.Label(frame, text=corrected_word, font=("Helvetica", 14), bg="#E6E6FA", fg="#f0f0f0")
    message_label.pack(pady=(10, 0))
    fade_in(message_label)

# Function to gradually change the color of the label
def fade_in(widget, step=0):
    new_color = f"#{step:02x}{step:02x}{step:02x}"
    widget.config(fg=new_color)
    if step < 0xFF:
        widget.after(50, fade_in, widget, step + 10)

# Create the main application window
root = tk.Tk()
root.title("Word Entry App")

# Set the minimum size of the window
root.minsize(400, 200)

# Create a frame for better layout management
frame = tk.Frame(root, bg="#E6E6FA")  # Lavender background color
frame.pack(fill=tk.BOTH, expand=True)

# Create a label to prompt the user
label = tk.Label(frame, text="Enter a word:", font=("Helvetica", 14), bg="#E6E6FA")  # Lavender background color
label.pack(pady=(10, 5))

# Create a StringVar to hold the entry text
entry_var = tk.StringVar()

# Create an entry widget for user input
entry = tk.Entry(frame, textvariable=entry_var, width=50, font=("Helvetica", 12))
entry.pack(pady=(5, 10))

# Create a global variable to hold the message label
message_label = None

# Create a button and assign the click handler
button = tk.Button(frame, text="Submit", font=("Helvetica", 12), bg="#4CAF50", fg="white", activebackground="#45a049", command=on_button_click)
button.pack(pady=(10, 20))

# Run the application
root.mainloop()
