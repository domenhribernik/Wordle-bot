import tkinter as tk
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
        self.rectangle_box = rectangle_box

        print(self.rectangle_box)

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
        return {word.lower() for word in self.word_list if len(word) == 5}

    def start_solver(self):
        word_list = words.words()
        arr = []
        for word in word_list:
            if len(word) == 5:
                arr.append(word.lower())

        word_set = set(arr)
        print(len(word_set))
        green_letters = ["", "", "", "", ""]
        yellow_letters = [[], [], [], [], []]
        wrong_letters = []
        colors_count_len = []
        time.sleep(self.setup_time)
        guess_word = self.start_phrase
        index = 0
        while index < 6:
            time.sleep(0.2)
            pyautogui.typewrite(guess_word, interval=0.1)
            pyautogui.press("enter")
            time.sleep(1.7)
            image = pyautogui.screenshot(region=self.rectangle_box)
            image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            cv2.imwrite("game.png", image)
            #cv2.imshow("image", image)

            image = cv2.imread("game.png")
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            gray = cv2.bilateralFilter(gray, 11, 17, 17)
            blur = cv2.blur(gray, (1,1))
            ret, thresh = cv2.threshold(blur, 50, 255, cv2.THRESH_BINARY)

            contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            output = cv2.drawContours(image, contours, -1, (0, 0, 255), 2)

            colors = []
            for contour in contours:
                y = contour[0][0][1] + 15
                x = contour[0][0][0] + 15
                (b, g, r) = output[y, x]
                # print(str(b) + " " + str(g) + " " + str(r))
                cv2.circle(output, (x, y), 2, (255, 0, 0), 2)
                text = ""
                if(b == 60 and g == 58 and r == 58):
                    text = "gray"
                elif(b == 59 and g == 159 and r == 181):
                    text = "yellow"  
                elif(b == 78 and g == 141 and r == 83):
                    text = "green"
                elif(b == 19 and g == 18 and r == 18):
                    text = "empty"
                cv2.putText(output, text, (x+10, y), cv2.FONT_HERSHEY_COMPLEX, 0.4, (255, 0, 0), 1, cv2.LINE_AA)
                #cv2.putText(output, guess_word[0],(x+37, y+45), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA) #TODO add letters on output
                if text != "empty":
                    colors.insert(0, text)
                
            print("len: " + str(len(colors)))
            if(not colors_count_len):
                colors_count_len.append(len(colors))
            else:
                if(len(colors) == colors_count_len[-1]):
                    print ("bad guess")
                    for i in range (0, len(word)):
                        pyautogui.press("backspace")
                    print("before len: " + str(len(word_set)))
                    word_set.remove(guess_word)
                    print("words: " + str(len(word_set)))
                    guess_word = list(word_set)[random.randint(0, len(word_set)-1)]
                    print("word: " + guess_word + " " + str(index))
                    #time.sleep(2)
                    continue
                else:
                    colors_count_len.append(len(colors))
            tmp = []
            for i in range(len(colors)-5, len(colors)):
                tmp.append(colors[i])
            colors = tmp.copy()

            for i in range(len(colors) - 5, len(colors)):
                if colors[i] == "empty":
                    break
                elif colors[i] == "green":
                    if green_letters[i] == "":
                        green_letters[i] = guess_word[i]
                        if guess_word[i] in wrong_letters: #TODO fix double letters
                            wrong_letters.remove(guess_word[i])
                    print(str(i) + " " + guess_word[i] + " is green", end="")
                elif colors[i] == "yellow":
                    yellow_letters[i].append(guess_word[i])
                    if guess_word[i] in wrong_letters: #TODO fix double letters
                        wrong_letters.remove(guess_word[i])
                    print(str(i), end=" ")
                    for j in range(0, len(yellow_letters[i])):
                        print(yellow_letters[i][j], end=" ")
                    print("is yellow", end="")
                elif colors[i] == "gray":
                    if guess_word[i] not in wrong_letters: 
                        wrong_letters.append(guess_word[i])
                    for j in range(0, len(yellow_letters[i])): #TODO fix double letters
                        if guess_word[i] in wrong_letters and guess_word[i] in yellow_letters[i][j]:
                            wrong_letters.remove(guess_word[i])
                    if guess_word[i] in green_letters: #TODO fix double letters
                        wrong_letters.remove(guess_word[i])
                    # if guess_word[i] not in wrong_letters:
                    #     wrong_letters.append(guess_word[i])    
                    print("Wrong letters:", end=" ")
                    for j in range(0, len(wrong_letters)):
                        print(wrong_letters[j], end = " ")
                print("")
            if "" not in green_letters:
                print("You Win")
                break
            elif index == 5:
                print("You Lose")
                break
            tmp = word_set.copy()
            print("before len: " + str(len(word_set)))
            for word in word_set:
                for i in range(0, len(green_letters)):
                    if green_letters[i] != "":
                        if word[i] != green_letters[i]:
                            tmp.discard(word)
                for letter in wrong_letters:
                    if letter in word:
                        for i in range(0, len(word)):
                            if green_letters[i] == "":
                                tmp.discard(word)
                            else:
                                if green_letters[i] != word[i]:
                                    tmp.discard(word)
                for i in range(0, len(yellow_letters)):
                    if not yellow_letters[i]:
                        continue
                    for j in range(0, len(yellow_letters[i])):
                        if yellow_letters[i][j] in word:
                            if word[i] == yellow_letters[i][j]:
                                tmp.discard(word)
                        else:
                            tmp.discard(word)
            print("before len: " + str(len(word_set)))
            print("words: " + str(len(tmp)))
            word_set = tmp.copy()
            # for word in word_set:
            #   print(word)
            print("words: " + str(len(word_set)))
            guess_word = list(word_set)[random.randint(0, len(word_set)-1)]
            print("word: " + guess_word + " " + str(index))
            index += 1

        cv2.imwrite("results/game"+str(datetime.date.today())+".png", output) #"-"+str(random.randint(100,999))+
        cv2.imshow("Output", output)
        cv2.waitKey()
        cv2.destroyAllWindows()







        # # Check if rectangle_box is valid
        # if not self.rectangle_box or len(self.rectangle_box) != 4:
        #     tk.messagebox.showerror("Error", "Invalid rectangle selected!")
        #     return

    #     print(f"Total words: {len(self.word_set)}")
    #     time.sleep(self.setup_time)

    #     while self.index < 6:
    #         time.sleep(0.2)
    #         pyautogui.typewrite(self.guess_word, interval=0.1)
    #         pyautogui.press("enter")
    #         time.sleep(1.7)

    #         # Capture and process the screenshot
    #         x, y, w, h = self.rectangle_box
    #         image = pyautogui.screenshot(region=(x, y, w, h))
    #         image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    #         cv2.imwrite("game.png", image)
    #         processed_colors = self.process_image(image)

    #         # Analyze the colors and update letter data
    #         self.update_letter_data(processed_colors)
            
    #         # Check for win or loss
    #         if "" not in self.green_letters:
    #             print("You Win!")
    #             break
    #         elif self.index == 5:
    #             print("You Lose!")
    #             break
            
    #         # Refine the word set and select the next guess
    #         self.refine_word_set()
    #         self.index += 1

    #     # Save the final output image
    #     cv2.imwrite(f"results/game{datetime.date.today()}.png", image)
    #     cv2.imshow("Output", image)
    #     cv2.waitKey()
    #     cv2.destroyAllWindows()

    # def process_image(self, image):
    #     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #     gray = cv2.bilateralFilter(gray, 11, 17, 17)
    #     blur = cv2.blur(gray, (1, 1))
    #     ret, thresh = cv2.threshold(blur, 50, 255, cv2.THRESH_BINARY)

    #     contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #     output = cv2.drawContours(image.copy(), contours, -1, (0, 0, 255), 2)

    #     colors = []
    #     for contour in contours:
    #         x, y, w, h = cv2.boundingRect(contour)
    #         x, y = x + w // 2, y + h // 2
    #         (b, g, r) = output[y, x]
            
    #         color = self.detect_color(b, g, r)
    #         if color != "empty":
    #             colors.insert(0, color)
    #     return colors

    # @staticmethod
    # def detect_color(b, g, r):
    #     if abs(b - 60) <= 10 and abs(g - 58) <= 10 and abs(r - 58) <= 10:
    #         return "gray"
    #     elif abs(b - 59) <= 10 and abs(g - 159) <= 10 and abs(r - 181) <= 10:
    #         return "yellow"
    #     elif abs(b - 78) <= 10 and abs(g - 141) <= 10 and abs(r - 83) <= 10:
    #         return "green"
    #     elif abs(b - 19) <= 10 and abs(g - 18) <= 10 and abs(r - 18) <= 10:
    #         return "empty"
    #     return ""

    # def update_letter_data(self, colors):
    #     for i in range(len(colors) - 5, len(colors)):
    #         if colors[i] == "empty":
    #             break
    #         elif colors[i] == "green":
    #             self.green_letters[i] = self.guess_word[i]
    #         elif colors[i] == "yellow":
    #             self.yellow_letters[i].append(self.guess_word[i])
    #         elif colors[i] == "gray":
    #             if self.guess_word[i] not in self.wrong_letters:
    #                 self.wrong_letters.append(self.guess_word[i])

    # def refine_word_set(self):
    #     tmp = self.word_set.copy()
    #     for word in self.word_set:
    #         # Ensure green letters match
    #         for i, letter in enumerate(self.green_letters):
    #             if letter and word[i] != letter:
    #                 tmp.discard(word)
    #         # Ensure no wrong letters are in the word
    #         for wrong_letter in self.wrong_letters:
    #             if wrong_letter in word:
    #                 tmp.discard(word)
    #         # Ensure yellow letters are present but not in the wrong position
    #         for i, yellow_letters in enumerate(self.yellow_letters):
    #             for yellow_letter in yellow_letters:
    #                 if yellow_letter not in word or word[i] == yellow_letter:
    #                     tmp.discard(word)
    #     self.word_set = tmp
    #     self.guess_word = random.choice(list(self.word_set))
