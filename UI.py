import tkinter as tk
from tkinter import messagebox
from collections import Counter
import re

# ---------------------- Spelling Logic ----------------------

# Extracts all lowercase words from text
def words(text):
    return re.findall(r'\w+', text.lower())

# Read words from a text file and count their frequencies
with open('D:\\python\\spell cheaker\\test.txt', 'r') as file:
    WORDS = Counter(words(file.read()))

# Probability of a word appearing in the dataset
def P(word, N=sum(WORDS.values())):
    return WORDS[word] / N

# Returns the most probable correction for a given word
def correction(word):
    return max(candidates(word), key=P)

# Generates all possible spelling candidates for a word
def candidates(word):
    return known([word]) or known(edits1(word)) or known(edits2(word)) or [word]

# Filters the list to only include known words from the dataset
def known(words):
    return set(w for w in words if w in WORDS)

# Generates all edits that are one edit away from the input word
def edits1(word):
    letters = 'abcdefghijklmnopqrstuvwxyz'
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [L + R[1:] for L, R in splits if R]                     # Delete one letter
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]  # Swap adjacent letters
    replaces = [L + c + R[1:] for L, R in splits if R for c in letters]     # Replace a letter
    inserts = [L + c + R for L, R in splits for c in letters]               # Insert a letter
    return set(deletes + transposes + replaces + inserts)

# Generates edits that are two edits away from the word
def edits2(word):
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))

# ---------------------- UI Functions ----------------------

# Triggered when "Correct" button is pressed
def correct_spelling():
    input_word = entry.get()
    if not input_word:
        messagebox.showwarning("Input Error", "Please enter a word.")
        return
    corrected_word = correction(input_word)
    result_label.config(text=f"✅ Corrected: {corrected_word}", fg="#1a936f")

# Shows suggestion list as user types
def show_suggestions(event):
    typed_word = entry.get()
    suggestion_listbox.delete(0, tk.END)

    if typed_word.strip():
        sugg = list(candidates(typed_word))[:5]  # Show top 5 suggestions
        for word in sugg:
            suggestion_listbox.insert(tk.END, word)
        suggestion_listbox.place(x=entry.winfo_x(), y=entry.winfo_y() + entry.winfo_height() + 2)
    else:
        suggestion_listbox.place_forget()

# Fills the entry box when a suggestion is clicked
def fill_suggestion(event):
    if suggestion_listbox.curselection():
        selected = suggestion_listbox.get(suggestion_listbox.curselection())
        entry.delete(0, tk.END)
        entry.insert(0, selected)
        suggestion_listbox.place_forget()

# ---------------------- UI Setup ----------------------

# Main window setup
root = tk.Tk()
root.title("🧠 AI Spelling Corrector")
root.geometry("600x450")  # Set window size
root.config(bg="#f4f4f4")  # Set background color

# Title label
title_label = tk.Label(root, text="🔍 Spell Checker with Suggestions", font=("Helvetica", 18, "bold"), bg="#f4f4f4", fg="#114b5f")
title_label.pack(pady=10)

# Main content frame
card = tk.Frame(root, bg="#ffffff", bd=2, relief="groove")
card.pack(padx=20, pady=10, fill="both", expand=True)

# Label for entry
entry_label = tk.Label(card, text="Enter a word:", font=("Arial", 12), bg="#ffffff")
entry_label.pack(pady=(20, 5))

# Entry box for user input
entry = tk.Entry(card, font=("Arial", 14), width=30, justify="center", relief="solid", bd=1)
entry.pack()

# Suggestion listbox
suggestion_listbox = tk.Listbox(card, font=("Arial", 12), height=5, width=30)
suggestion_listbox.bind("<<ListboxSelect>>", fill_suggestion)
entry.bind("<KeyRelease>", show_suggestions)

# Spacer to create gap before button
tk.Label(card, text="", bg="#ffffff").pack(pady=40)

# Button hover effects
def on_enter(e): correct_button.config(bg="#333", fg="#fff")
def on_leave(e): correct_button.config(bg="#1a936f", fg="#fff")

# "Correct" button
correct_button = tk.Button(
    card, text="Correct", font=("Arial", 12, "bold"),
    bg="#1a936f", fg="white", padx=10, pady=5,
    relief="flat", activebackground="#114b5f", activeforeground="white",
    command=correct_spelling
)
correct_button.pack()
correct_button.bind("<Enter>", on_enter)
correct_button.bind("<Leave>", on_leave)

# Label to show result
result_label = tk.Label(card, text="", font=("Arial", 14, "bold"), bg="#ffffff", fg="#1a936f")
result_label.pack(pady=(20, 20))

# Run the GUI application
root.mainloop()
