import numpy as np
import pyautogui
import time
import random
import datetime
import cv2
from nltk.corpus import words


class WordleSolverApp:
    def __init__(self, root, rectangle_box, switch_to_menu):
        self.root = root
        self.switch_to_menu = switch_to_menu  # Function to switch back to the menu
        self.setup_ui()

        # Initialize variables
        self.word_list = words.words()
        self.arr = []
        self.start_phrase = "crane"
        self.setup_time = 3
        self.word_set = self.create_word_set()
        self.green_letters = ["", "", "", "", ""]
        self.yellow_letters = [[], [], [], [], []]
        self.wrong_letters = []
        self.colors_count_len = []
        self.guess_word = self.start_phrase
        self.index = 0

    def setup_ui(self):
        self.root.attributes('-fullscreen', False)
        self.root.configure(background="white")
        
        # Label
        self.label = tk.Label(
            self.root, 
            text="Wordle Solver", 
            font=("Arial", 24), 
            bg="white", 
            fg="black"
        )
        self.label.pack(pady=20)

        # Start button
        self.start_button = tk.Button(
            self.root, 
            text="Start Solver", 
            command=self.start_solver
        )
        self.start_button.pack(pady=10)

        # Back to menu button
        self.menu_button = tk.Button(
            self.root, 
            text="Back to Menu", 
            command=self.switch_to_menu
        )
        self.menu_button.pack(pady=10)

    def create_word_set(self):
        # Filter word list to include only 5-letter words
        arr = [word.lower() for word in self.word_list if len(word) == 5]
        return set(arr)

    def start_solver(self):
        # Check if rectangle_box is valid
        if not self.rectangle_box or len(self.rectangle_box) != 4:
            tk.messagebox.showerror("Error", "Invalid rectangle selected!")
            return

        print(f"Total words: {len(self.word_set)}")
        time.sleep(self.setup_time)

        while self.index < 6:
            time.sleep(0.2)
            pyautogui.typewrite(self.guess_word, interval=0.1)
            pyautogui.press("enter")
            time.sleep(1.7)

            # Capture and process the screenshot
            x, y, w, h = self.rectangle_box
            image = pyautogui.screenshot(region=(x, y, w - x, h - y))
            image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            cv2.imwrite("game.png", image)
            processed_colors = self.process_image(image)

            # Analyze the colors and update letter data
            self.update_letter_data(processed_colors)
            
            # Check for win or loss
            if "" not in self.green_letters:
                print("You Win!")
                break
            elif self.index == 5:
                print("You Lose!")
                break
            
            # Refine the word set and select the next guess
            self.refine_word_set()
            self.index += 1

        # Save the final output image
        cv2.imwrite(f"results/game{datetime.date.today()}.png", image)
        cv2.imshow("Output", image)
        cv2.waitKey()
        cv2.destroyAllWindows()

    def process_image(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.bilateralFilter(gray, 11, 17, 17)
        blur = cv2.blur(gray, (1, 1))
        ret, thresh = cv2.threshold(blur, 50, 255, cv2.THRESH_BINARY)

        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        output = cv2.drawContours(image.copy(), contours, -1, (0, 0, 255), 2)

        colors = []
        for contour in contours:
            y = contour[0][0][1] + 15
            x = contour[0][0][0] + 15
            (b, g, r) = output[y, x]
            
            color = self.detect_color(b, g, r)
            if color != "empty":
                colors.insert(0, color)
        return colors

    @staticmethod
    def detect_color(b, g, r):
        if b == 60 and g == 58 and r == 58:
            return "gray"
        elif b == 59 and g == 159 and r == 181:
            return "yellow"
        elif b == 78 and g == 141 and r == 83:
            return "green"
        elif b == 19 and g == 18 and r == 18:
            return "empty"
        return ""

    def update_letter_data(self, colors):
        for i in range(len(colors) - 5, len(colors)):
            if colors[i] == "empty":
                break
            elif colors[i] == "green":
                self.green_letters[i] = self.guess_word[i]
            elif colors[i] == "yellow":
                self.yellow_letters[i].append(self.guess_word[i])
            elif colors[i] == "gray":
                if self.guess_word[i] not in self.wrong_letters:
                    self.wrong_letters.append(self.guess_word[i])

    def refine_word_set(self):
        tmp = self.word_set.copy()
        for word in self.word_set:
            for i, letter in enumerate(self.green_letters):
                if letter and word[i] != letter:
                    tmp.discard(word)
            for wrong_letter in self.wrong_letters:
                if wrong_letter in word:
                    tmp.discard(word)
            for i, yellow_letters in enumerate(self.yellow_letters):
                for yellow_letter in yellow_letters:
                    if yellow_letter not in word or word[i] == yellow_letter:
                        tmp.discard(word)
        self.word_set = tmp
        self.guess_word = random.choice(list(self.word_set))