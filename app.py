from menu import *
from rectangle_selector import *
from wordle_solver import *
import tkinter as tk
from tkinter import messagebox

app_data = {"rectangle_box": None}


def switch_to_rectangle_selector(root):
    for widget in root.winfo_children():
        widget.destroy()

    # Callback to save the rectangle
    def save_rectangle(box):
        app_data["rectangle_box"] = box
        switch_to_menu(root)

    RectangleSelectorApp(root, lambda: switch_to_menu(root), save_rectangle)


def switch_to_wordle_solver(root):
    for widget in root.winfo_children():
        widget.destroy()

    # Check if rectangle_box is valid
    if app_data["rectangle_box"] is None:
        messagebox.showerror("Error", "No valid rectangle selected. Please select a rectangle first.")
        switch_to_menu(root)  # Return to menu if invalid
        return

    WordleSolverApp(root, app_data["rectangle_box"], lambda: switch_to_menu(root))


def switch_to_menu(root):
    for widget in root.winfo_children():
        widget.destroy()

    MenuApp(root, lambda: switch_to_rectangle_selector(root), lambda: switch_to_wordle_solver(root))


if __name__ == "__main__":
    root = tk.Tk()
    switch_to_menu(root)
    root.mainloop()
