import tkinter as tk

class MenuApp:
    def __init__(self, root, switch_to_rectangle_selector, switch_to_wordle_solver):
        self.root = root
        self.root.configure(bg="white")
        self.root.attributes('-fullscreen', False)
        self.root.attributes('-alpha', 1)  # Reset the transparency

        # Title
        self.label = tk.Label(
            root,
            text="Main Menu",
            font=("Arial", 24),
            bg="white",
            fg="black"
        )
        self.label.pack(pady=20)

        # Rectangle Selector button
        self.rectangle_button = tk.Button(
            root,
            text="Select Rectangle",
            command=switch_to_rectangle_selector
        )
        self.rectangle_button.pack(pady=10)

        # Wordle Solver button
        self.wordle_solver_button = tk.Button(
            root,
            text="Solve Wordle",
            command=switch_to_wordle_solver
        )
        self.wordle_solver_button.pack(pady=10)
