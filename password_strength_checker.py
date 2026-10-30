import tkinter as tk
from tkinter import ttk
import re


COMMON_PASSWORDS = {
    "password", "password123", "123456", "12345678",
    "qwerty", "admin", "letmein", "welcome"
}


def assess_password(password):
    score = 0
    suggestions = []

    if not password:
        return 0, "Very Weak", ["Enter a password."]

    if len(password) >= 12:
        score += 2
    else:
        suggestions.append("Use at least 12 characters.")

    if re.search(r"[a-z]", password):
        score += 1
    else:
        suggestions.append("Add lowercase letters.")

    if re.search(r"[A-Z]", password):
        score += 1
    else:
        suggestions.append("Add uppercase letters.")

    if re.search(r"\d", password):
        score += 1
    else:
        suggestions.append("Add numbers.")

    if re.search(r"[^a-zA-Z0-9]", password):
        score += 1
    else:
        suggestions.append("Add special characters.")

    if password.lower() in COMMON_PASSWORDS:
        score = 0
        suggestions.append("Avoid commonly used passwords.")

    if re.search(r"(.)\1{2,}", password):
        score = max(0, score - 2)
        suggestions.append("Avoid repeated characters.")

    if re.search(
        r"1234|abcd|qwer|password|9876",
        password.lower()
    ):
        score = max(0, score - 2)
        suggestions.append("Avoid predictable sequences.")

    if score <= 1:
        strength = "Very Weak"
    elif score <= 2:
        strength = "Weak"
    elif score <= 3:
        strength = "Fair"
    elif score <= 4:
        strength = "Strong"
    else:
        strength = "Very Strong"

    return score, strength, suggestions


def check_password(*args):
    password = password_entry.get()
    score, strength, suggestions = assess_password(password)

    strength_label.config(text="Strength: " + strength)
    progress["value"] = (score / 6) * 100

    if suggestions:
        suggestion_text = "\n".join(
            "- " + item for item in suggestions
        )
    else:
        suggestion_text = "Your password meets all the checks!"

    suggestions_label.config(text=suggestion_text)


def toggle_password():
    if show_password.get():
        password_entry.config(show="")
    else:
        password_entry.config(show="*")


def clear_password():
    password_entry.delete(0, tk.END)
    strength_label.config(text="Strength: ")
    progress["value"] = 0
    suggestions_label.config(text="")


root = tk.Tk()
root.title("Password Strength Checker")
root.geometry("500x400")
root.resizable(False, False)

title = tk.Label(
    root,
    text="Password Strength Checker",
    font=("Arial", 18, "bold")
)
title.pack(pady=20)

instruction = tk.Label(
    root,
    text="Enter a password to check its strength:",
    font=("Arial", 11)
)
instruction.pack(pady=5)

password_entry = tk.Entry(
    root,
    width=35,
    font=("Arial", 12),
    show="*"
)
password_entry.pack(pady=10)
password_entry.bind("<KeyRelease>", check_password)

show_password = tk.BooleanVar()

show_checkbox = tk.Checkbutton(
    root,
    text="Show Password",
    variable=show_password,
    command=toggle_password
)
show_checkbox.pack()

strength_label = tk.Label(
    root,
    text="Strength: ",
    font=("Arial", 13, "bold")
)
strength_label.pack(pady=15)

progress = ttk.Progressbar(
    root,
    length=300,
    maximum=100
)
progress.pack(pady=5)

suggestions_label = tk.Label(
    root,
    text="",
    font=("Arial", 10),
    justify="left",
    wraplength=430
)
suggestions_label.pack(pady=15)

clear_button = tk.Button(
    root,
    text="Clear",
    command=clear_password,
    width=15
)
clear_button.pack(pady=10)

root.mainloop()