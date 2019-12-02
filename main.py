import sys
import time
import keyboard

import tkinter as tk


class Application(tk.Frame):

    def __init__(self, root):

        tk.Frame.__init__(self, root)
        self.root = root
        self.widgetList = dict()
        self.defPad = 5
        self.putTitle("mainTitle", "Spelunky 1000 death achievement")
        description = ("This program is a loop automating the death of the spelunker.\n"
                       "Each loop takes about 11 seconds, it will take about 3 hours to die that many times.\n"
                       "Once you hit start, launch the game and get in the first level, just wait for the death to begin\n")
        self.putText("description", description)
        self.putInput("loop", "Number of loop")
        self.putInput("down", "Down key")
        self.putInput("bomb", "Bomb key")
        self.putInput("whip", "Whip key")

    def getContainer(self):
        # background="red"
        container = tk.Frame(height=2, bd=1)
        container.pack(padx=5, pady=5, expand=True, fill=tk.X)
        return container

    def putTitle(self, label, text):
        labelElem = tk.Label(self.getContainer(), text=text,
                             font=("Arial", 18, "bold"))
        labelElem.pack(
            side=tk.LEFT, padx=self.defPad, pady=self.defPad)
        self.widgetList[label] = labelElem

    def putText(self, label, text):
        msgElem = tk.Message(self.getContainer(), text=text,
                             anchor=tk.NW, width=380)
        msgElem.pack(
            side=tk.LEFT, padx=self.defPad, pady=self.defPad, expand=True, fill=tk.X)
        self.widgetList[label] = msgElem

    def putInput(self, label, name):
        container = self.getContainer()
        labelElem = tk.Label(container, text=name, width=15, anchor=tk.W)
        labelElem.pack(
            side=tk.LEFT, padx=self.defPad, pady=self.defPad)
        inputElem = tk.Entry(container)
        inputElem.pack(
            side=tk.LEFT, padx=self.defPad, pady=self.defPad, expand=True, fill=tk.X)
        self.widgetList[label] = labelElem
        self.widgetList[label+"Input"] = inputElem


def guiInit():
    root = tk.Tk()
    root.minsize(450, 150)
    root.title('Parameter for the Spelunky Achievement')
    result = Application(root)
    root.mainloop()


def killLoop(loop, downKey, bombKey, resetKey):
    for x in range(0, int(loop)):
        print(downKey + bombKey + resetKey)
        keyboard.press(downKey)
        time.sleep(0.5)
        print("bomb")
        keyboard.press(bombKey)
        time.sleep(0.1)
        keyboard.release(bombKey)
        time.sleep(0.1)
        keyboard.release(downKey)
        time.sleep(8)
        print("Reset")
        keyboard.press(resetKey)
        time.sleep(0.1)
        keyboard.release(resetKey)
        time.sleep(2.5)


def main():
    try:
        gameKey = sys.argv[2:]
        loop, down, bomb, reset = gameKey
    except IndexError:
        print("An error occured while retrieving the necessary argument")

    # Select the window with the game running
    print("Open the game and enter the first level, press enter to start killing")
    time.sleep(15)
    killLoop(loop, down, bomb, reset)


def usage():
    doc = """ 
    Usage of this program :
    Wait for you to open Spelunky and kills you how many times you want :
        - main.py run loopNbr downKey bombKey resetKey

    View all command of program
        - main.py help
    """
    print(doc)


def handleOptions(argument):
    switcher = {
        "help": usage,
        "run": main,
        "gui": guiInit,
    }
    return switcher.get(argument, usage)


if __name__ == "__main__":
    # execute only if run as a script
    try:
        handleOptions(sys.argv[1])()
    except IndexError:
        print("Error, Please specify an argument for help type 'main.py help'")
