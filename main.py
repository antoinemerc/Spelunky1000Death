import sys
import time
import keyboard
import tkinter as tk
import functools

class InvalidFormError(Exception):
   """Form is invalid, check inputs"""
   pass

class MissingArgumentError(Exception):
   """argument is missing to execute function"""
   pass

class Application(tk.Frame):

    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root
        self.widgetList = dict()
        self.defPad = 5
        self.callbackFunction = None
        self.neededParameters = []
        self.availableParameters = []

    def buildSpelunkyWindow(self):
        self.putTitle("mainTitle", "Spelunky 1000 death achievement")
        description = ("This program is a loop automating the death of the spelunker.\n"
                       "Each loop takes about 11 seconds, it will take about 3 hours to die that many times.\n"
                       "Once you hit start, launch the game and get in the first level, just wait for the death to begin")
        self.putText("description", description)
        self.putText("errorField", "")
        self.widgetList["errorField"]["elem"].configure(fg="red")

        self.putInputGroup("loopInput", "Number of loop", "loopNbr", True)
        self.putInputGroup("downInput", "Down key", "downKey", True)
        self.putInputGroup("bombInput", "Bomb key", "bombKey", True)
        self.putInputGroup("whipInput", "Whip key", "whipKey", True)

        self.putButton("executeButton", "Start the killing", self.executeProgram)

    def updateText(self, textName, text):
        self.widgetList[textName]["elem"].configure(text=text)

    def getContainer(self):
        container = tk.Frame(height=2, bd=1)
        container.pack(padx=5, pady=5, expand=True, fill=tk.X)
        return container

    def putTitle(self, inputName, text):
        labelElem = tk.Label(self.getContainer(), text=text, font=("Arial", 18, "bold"))
        labelElem.pack(side=tk.LEFT, padx=self.defPad, pady=self.defPad)
        self.widgetList[inputName] = {"elem": labelElem,"type": "text"}

    def putText(self, inputName, text):
        msgElem = tk.Message(self.getContainer(), text=text, anchor=tk.NW, width=380)
        msgElem.bind("<Configure>", lambda e: msgElem.configure(width=e.width-10))
        msgElem.pack(side=tk.LEFT, expand=True, fill=tk.X)
        self.widgetList[inputName] = {"elem": msgElem,"type": "text"}

    def putInputGroup(self, inputName, label, field, mandatory):
        container = self.getContainer()
        self.putLabel(container, inputName, label, mandatory)
        self.putInput(container, inputName, field, mandatory)

    def putLabel(self, container, inputName, label, mandatory):
        labelDisplay = label + " *:" if mandatory else label + " :"
        labelElem = tk.Label(container, text=labelDisplay, width=15, anchor=tk.W)
        labelElem.pack(side=tk.LEFT, padx=self.defPad, pady=self.defPad)
        self.widgetList[inputName + "Label"] = {"elem": labelElem,"type": "text", "label": label}

    def putInput(self, container, inputName, field, mandatory):
        self.availableParameters.append({"field": field, "inputName": inputName})
        inputElem = tk.Entry(container, relief='flat', highlightthickness=1, highlightbackground="black")
        inputElem.pack(side=tk.LEFT, padx=self.defPad, pady=self.defPad, expand=True, fill=tk.X)
        self.widgetList[inputName] = {"elem": inputElem,"type": "input","field": field, "mandatory": mandatory}

    def getInputValue(self, inputName):
        return self.widgetList[inputName]["elem"].get()

    def putButton(self, inputName, label, callback):
        container = self.getContainer()
        inputElem = tk.Button(container, text=label, command=callback)
        inputElem.pack(side=tk.LEFT, padx=self.defPad, pady=self.defPad, expand=True, fill=tk.X)
        self.widgetList[inputName] = {"elem": inputElem,"type": "button"}

    def validateInputs(self, inputName):
        if self.getInputValue(inputName) == "" and self.widgetList[inputName]["mandatory"]:
            self.widgetList[inputName]["elem"].configure(highlightbackground='red', highlightcolor='red')
            error = self.widgetList[inputName + "Label"]["label"] + ": Mandatory Input was not filled"
            return {"status": False, "message": error}
        else:
            return {"status": True, "message": ""}

    def validateAll(self):
        validForm = True
        self.clearError()
        inputDict = dict(filter(lambda keyAndItem: keyAndItem[1]["type"] == "input", self.widgetList.items()))
        for inputName, inputItem in inputDict.items():
            if self.validateInputs(inputName)["status"] == False:
                validForm = False
                self.addError(self.validateInputs(inputName)["message"])
        if validForm == False:
            raise InvalidFormError

    def clearError(self):
        self.widgetList["errorField"]["elem"].configure(text="")
        inputDict = dict(filter(lambda keyAndItem: keyAndItem[1]["type"] == "input", self.widgetList.items()))
        for inputName, inputItem in inputDict.items():
            inputItem["elem"].configure(highlightbackground='black', highlightcolor='black')

    def addError(self, errorText):
        currentText = self.widgetList["errorField"]["elem"]["text"]
        self.widgetList["errorField"]["elem"].configure(text=currentText + "\n" + errorText )

    def executeProgram(self):
        try:
            self.validateAll()
            paramList = []
            for neededParam in self.neededParameters:
                paramToAdd = list(filter(lambda param: param["field"] == neededParam, self.availableParameters))
                if len(paramToAdd) > 0:
                    paramList.append(self.getInputValue(paramToAdd[0]["inputName"]))
                else:
                    raise MissingArgumentError
            callback = functools.partial(self.callbackFunction, *paramList)
            callback()
        except InvalidFormError:
            self.addError("Error in the form, cannot proceed")
        except MissingArgumentError:
            self.addError("Error in the execution parameters, fix this bug")
        except TypeError:
            self.addError("No function to execute, fix this bug")

    def setCallbackFunction(self, callback, arguments):
        self.callbackFunction = callback
        self.neededParameters = arguments

def guiInit():
    root = tk.Tk()
    root.minsize(450, 150)
    root.title("Parameter for the Spelunky Achievement")
    result = Application(root)
    result.buildSpelunkyWindow()
    result.setCallbackFunction(killLoop, ["loopNbr","downKey","bombKey","whipKey"])
    root.mainloop()

def killLoop(loop, downKey, bombKey, resetKey):
    print(loop + ", " + downKey + ", " + bombKey + ", " + resetKey)
    time.sleep(15)
    for x in range(0, int(loop)):
        print("Pressing the down key: 0.5s")
        keyboard.press(downKey)
        time.sleep(0.5)
        print("Throwing a bomb")
        keyboard.press(bombKey)
        time.sleep(0.1)
        keyboard.release(bombKey)
        time.sleep(0.1)
        keyboard.release(downKey)
        print("Waiting for death and menu: 8s")
        time.sleep(8)
        print("Resetting after the death")
        keyboard.press(resetKey)
        time.sleep(0.1)
        keyboard.release(resetKey)
        print("Waiting for restart: 2.5s")
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
    guiInit()
    # execute only if run as a script
    try:
        handleOptions(sys.argv[1])()
    except IndexError:
        print("Error, Please specify an argument for help type 'main.py help'")
