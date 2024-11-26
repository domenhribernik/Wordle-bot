import tkinter as tk
from tkinter import Button, Label
import pyautogui
import cv2
import numpy as np

class RectangleSelectorApp:
    def __init__(self, root, switch_to_menu, save_rectangle_callback):
        self.root = root
        self.switch_to_menu = switch_to_menu  # Function to switch back to the menu
        self.save_rectangle_callback = save_rectangle_callback  # Callback to save the rectangle
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-alpha', 0.3)  # Makes the background semi-transparent
        self.root.configure(background='black')
        self.root.bind('<Escape>', self.exit_app)  # Press 'Esc' to close the app

        self.start_x = None
        self.start_y = None
        self.rectangle = None
        self.rectangle_box = None
        self.cropped_image = None  # To store the cropped image

        self.canvas = tk.Canvas(root, bg="black", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=tk.YES)
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<Motion>", self.on_motion)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

        # Add buttons for "Save", "Retry", and "Back to Menu"
        self.button_frame = tk.Frame(root, bg="black")
        self.button_frame.pack(side=tk.BOTTOM, fill=tk.X)
        self.save_button = Button(self.button_frame, text="Save", command=self.save_rectangle, state=tk.DISABLED)
        self.save_button.pack(side=tk.LEFT, padx=10, pady=5)
        self.retry_button = Button(self.button_frame, text="Retry", command=self.retry, state=tk.DISABLED)
        self.retry_button.pack(side=tk.LEFT, padx=10, pady=5)
        self.menu_button = Button(self.button_frame, text="Back to Menu", command=self.switch_to_menu)
        self.menu_button.pack(side=tk.LEFT, padx=10, pady=5)

        self.info_label = Label(self.button_frame, text="Draw a rectangle and click Save or Retry.", bg="black", fg="white")
        self.info_label.pack(side=tk.LEFT, padx=10)

    def on_click(self, event):
        self.start_x = event.x
        self.start_y = event.y
        if self.rectangle:
            self.canvas.delete(self.rectangle)

    def on_motion(self, event):
        if self.start_x is not None and self.start_y is not None:
            if self.rectangle:
                self.canvas.delete(self.rectangle)
            # Draw a rectangle as the user moves the mouse
            self.rectangle = self.canvas.create_rectangle(
                self.start_x, self.start_y, event.x, event.y, outline="red", width=5
            )

    def on_release(self, event):
        end_x, end_y = event.x, event.y

        if end_x == self.start_x or end_y == self.start_y:
            self.info_label.config(text="Invalid selection: Please select a valid area.")
            return
        
        x = min(self.start_x, end_x)
        y = min(self.start_y, end_y)
        width = abs(self.start_x - end_x)
        height = abs(self.start_y - end_y)

        self.rectangle_box = (x, y, width, height)

        screenshot = pyautogui.screenshot()
        screenshot = np.array(screenshot)
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2RGB)

        self.cropped_image = screenshot[min(self.start_y, end_y):max(self.start_y, end_y),
                                        min(self.start_x, end_x):max(self.start_x, end_x)]
        
        cv2.imshow("Selected Region", self.cropped_image)
        self.save_button.config(state=tk.NORMAL)
        self.retry_button.config(state=tk.NORMAL)

    def save_image(self):
        if self.cropped_image is not None:
            file_name = "cropped_image.png"
            cv2.imwrite(file_name, cv2.cvtColor(self.cropped_image, cv2.COLOR_RGB2BGR))
            self.info_label.config(text=f"Image saved as {file_name}")

    def save_rectangle(self):
        if self.rectangle_box:
            cv2.destroyAllWindows()
            self.save_rectangle_callback(self.rectangle_box)
        else:
            self.info_label.config(text="No rectangle to save.")

    def retry(self):
        if self.rectangle:
            self.canvas.delete(self.rectangle)
            self.rectangle = None
        self.start_x, self.start_y = None, None
        self.cropped_image = None
        self.save_button.config(state=tk.DISABLED)
        self.retry_button.config(state=tk.DISABLED)
        cv2.destroyAllWindows()

    def exit_app(self, event=None):
        cv2.destroyAllWindows()
        self.root.destroy()