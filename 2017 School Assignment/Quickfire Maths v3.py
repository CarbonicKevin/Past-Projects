from tkinter import *
from random import choice, randint

class windowSetup():
    """
    Class which is responsible for all GUI elements. No processes.
    """
    def __init__(self):
        """
        Creating everything that every method will need.
        Each method after will simply create a window on the canvas using the widgets created in this class
        """
        ########## General Stuff ##########
        self.window = Tk()
        self.window.title("Quickfire Maths")

        self.canvas = Canvas(self.window, width=600, height=600)  # Creating a canvas
        self.canvas.pack()

        # Importing image for welcome screen, question screen, and final screen
        self.bImage = PhotoImage(file="images/welcome_screen.gif")

        self.quitButton = Button(self.window,
                                bg="#ff2222", relief=GROOVE,
                                text="Quit", font="Courier 15",
                                width=4,
                                command=self.window.destroy
                                )

        ########## welcomeScreen() Stuff ##########
        self.rFrame = Frame(self.window,  # Making the frame in which the radio buttons and their label will reside
                            bg="#7ad7ff"  # Light blue
                            )
        self.cFrame = Frame(self.window,  # Making the frame in which the check buttons and their label will reside
                            bg="#7ad7ff"  # Light blue
                            )

        self.modeVar = IntVar()  # Making the variable for the radio buttons
        self.addVar = IntVar()  # Making the variable for check buttons
        self.subVar = IntVar()
        self.multVar = IntVar()

        self.modeVar.set(1)# Setting the default value of radio buttons
        self.addVar.set(1)# Setting the default value of check buttons
        self.subVar.set(1)
        self.multVar.set(1)

        # Creating the radio buttons & label.
        self.rLabel = Label(self.rFrame,
                            bg="#7ad7ff",  # Light blue background
                            text="Please choose a mode", font="Courier 12 italic"
                            )

        self.roundButton = Radiobutton(self.rFrame, bg="#7ad7ff",  # Light blue background
                                       text="Round Mode", font="Courier 10",
                                       variable=self.modeVar, value=1,
                                       command=lambda: self.roundEntry.config(state=NORMAL)
                                       )

        self.unlimitedButton = Radiobutton(self.rFrame, bg="#7ad7ff",  # Light blue background
                                           text="Unlimited Mode", font="Courier 10",
                                           variable=self.modeVar, value=2,
                                           command=lambda: self.roundEntry.config(state=DISABLED)
                                           )

        # Creating the round entry box & label
        self.roundEntry = Entry(self.rFrame, width=2)
        self.rEntryLabel = Label(self.rFrame,
                                 text="No. Rounds:",
                                 font="Courier 8 italic", bg="#7ad7ff"  # Light blue background
                                 )

        # Creating the check buttons & label
        self.cLabel = Label(self.cFrame,
                            bg="#7ad7ff", text="Please choose question types", font="Courier 12 italic"
                            )
        self.addButton = Checkbutton(self.cFrame,
                                     bg="#7ad7ff", text="Addition", font="Courier 10", variable=self.addVar
                                     )
        self.subButton = Checkbutton(self.cFrame, bg="#7ad7ff",
                                     text="Subtraction", font="Courier 10", variable=self.subVar
                                     )
        self.multButton = Checkbutton(self.cFrame, bg="#7ad7ff",
                                      text="Multiplication", font="Courier 10", variable=self.multVar
                                      )

        # Creating the start button (Command will be configured in process class)
        self.startButton = Button(self.window,
                                  bg="#7ad7ff", relief=GROOVE,
                                  text="START", font="Courier 20",
                                  width=10,
                                  command=None
                                  )

        self.tip = Label(self.window,  # Creating tip
                         text="Tip:\n"
                              "You can check your score in round mode\n"
                              "at any time by presssing Right Click",
                         font="Courier 10", bg="#7ad7ff"
                         )

        # Packing the radio buttons & labels
        self.rLabel.grid(row=0, column=0, columnspan=3)
        self.roundButton.grid(row=1, column=0, columnspan=2, sticky=W)

        self.roundEntry.grid(row=2, column=1, padx=5, pady=7)
        self.rEntryLabel.grid(row=2, column=0, pady=20)

        self.unlimitedButton.grid(row=1, column=2, padx=20)

        # Packing the check buttons & labels
        self.cLabel.grid(row=0, column=0, columnspan=3)
        self.addButton.grid(row=1, column=0)
        self.subButton.grid(row=1, column=1)
        self.multButton.grid(row=1, column=2)

        ########## questionScreen() WIDGETS ##########
        self.inputVar = StringVar()  # Dummy variable to be used to stop the program for inputButton
        self.inputBox = Entry(self.window, width=10, font="Courier 30")  # Entry for use to input answer
        self.inputButton = Button(self.window,  # Button for user to submit answer
                                  bg="#7ad7ff", relief=GROOVE,
                                  text="SUBMIT", font="Courier 20",
                                  width=10,
                                  command=lambda: self.inputVar.set(self.inputBox.get())
                                  )

        ########## answerScreen() WIDGETS ##########
        # Importing background images
        self.correctImage = PhotoImage(file="images/correct_screen.gif")
        self.falseImage = PhotoImage(file="images/false_screen.gif")

        self.nextVar = IntVar()  # Dummy variable to be used to stop the program for nextButton
        self.nextButton = Button(self.window,  # Button to move onto the next question
                                  bg="#7ad7ff", relief=GROOVE,
                                  text="Next", font="Courier 20",
                                  width=10,
                                  command=lambda: self.nextVar.set(1)
                                  )

        ########## finalScreen() WIDGETS ##########
        self.restartButton = Button(self.window,  # Button to restart game (Command will be configured in process class)
                                  bg="#7ad7ff", relief=GROOVE,
                                  text="Restart?", font="Courier 20",
                                  width=10,
                                  command=None
                                  )

        ########## overlayCreate() WIDGETS ##########
        self.overlayFrame = Frame(self.window,  # Frame to house all the labels for the overlay
                                  bg="#c9efff",
                                  width=500, height=500
                                  )

        ########## Error Messages ##########
        # welcomeScreen()
        self.gameTypeError = Label(self.cFrame,  # Error message: user has not selected any game types
                                   text="You must choose at least one",
                                   font="Courier 15",
                                   foreground="#ff0000", bg="#7ad7ff"  # Red text on Light blue background
                                   )
        self.roundEntryError = Label(self.rFrame,  # Error message: user input invalid rounds.
                                     text="Must be an integer."
                                          "\nMust be greater or equal to"
                                          "\nthe number of gametypes."
                                          "\nMust be less than 20.",
                                     font="Courier 7",
                                     foreground="#ff0000", bg="#7ad7ff"  # Red text on Light blue background
                                     )

        # questionScreen()
        self.inputError = Label(self.window,
                                text="Incorrect Input",  # If it can't be integers
                                font="Courier 15",
                                foreground="#ff0000", bg="#7ad7ff"
                                )
        self.tooLongError = Label(self.window,
                                  text="Cannot be longer than 12 digits",
                                  font="Courier 15", foreground="#ff0000", bg="#7ad7ff"
                                  )

        # overlayCreate()
        self.noneError = Label(self.overlayFrame, # Error message: display if there are no results
                               text="You have yet to answer any questions",
                               font="Courier 10 italic",
                               bg="#c9efff"  # Lighter blue background
                               )

    def welcomeScreen(self):
        """
        Method to display the welcome screen
        MUST BE INITIALISED FIRST
        """
        self.canvas.delete("all")  # Clear the screen
        self.roundEntryError.grid_forget()

        self.canvas.create_image(300, 300, image=self.bImage)  # Displaying the background image
        self.canvas.create_text(300, 50, text="Welcome to Quick Maths", font="Courier 30 italic", fill="#ff0000")

        self.canvas.create_window(300, 300, window=self.rFrame)  # Displaying the radio buttons
        self.canvas.create_window(300, 400, window=self.cFrame)  # Displaying the check buttons

        self.canvas.create_window(180, 140, window=self.tip)  # Displaying a tip

        self.roundEntry.config(state=NORMAL)  # Activating the entry box
        self.canvas.create_window(300, 490, window=self.startButton)  # Displaying the start button
        self.canvas.create_window(560, 570, window=self.quitButton)  # Displaying the quit button

    def questionScreen(self, question, questionNo):
        """
        Method to display the question screen
        Takes a question in terms of a string, and a questionNo in terms of a int
        """
        self.canvas.delete("all")  # Clear the screen

        self.canvas.create_image(300, 300, image=self.bImage)  # Displaying the background image

        self.canvas.create_text(300, 50,  # Displaying question number
                                text="Question {}".format(questionNo),
                                font="Courier 30 italic", fill="#ff0000"
                                )
        self.canvas.create_text(300, 250,  # Displaying question
                                text=question,
                                font="Courier 50 italic", fill="#00ff00"
                                )

        self.canvas.create_window(300, 400, window=self.inputBox)  # Displaying the entry button
        self.canvas.create_window(300, 490, window=self.inputButton)  # Displaying the button to move on

        self.canvas.create_window(560, 570, window=self.quitButton)  # Displaying the quit button


    def answerScreen(self, question, uInput, correct):
        """
        Need to create background images
        Takes a question in terms of a string, uInput in terms of a string, and correct in terms of a boolean
        """
        self.canvas.delete("all")  # Clear the screen

        if correct:  # If user is correct, display the correct background and text
            self.canvas.create_image(300, 300, image=self.correctImage)
            self.canvas.create_text(300, 50, text="You Were Right!", font="Courier 30 italic")
            colour = "#9effb0"  # LightGreen
        else:  # If user is incorrect, display the incorrect background and text
            self.canvas.create_image(300, 300, image=self.falseImage)
            self.canvas.create_text(300, 50, text="You Were Wrong!", font="Courier 30 italic")
            colour = "#ff9ead"  # LightRed

        self.canvas.create_text(300, 250,  # Displaying question
                                text="Question: {}".format(question), font="Courier 30 italic"
                                )
        self.canvas.create_text(300, 350,  # Displaying user input
                                text="Your Input: {}".format(uInput), font="Courier 30 italic"
                                )
        self.canvas.create_text(300, 400,  # Displaying correct answer
                                text="Answer: {}".format(eval(question)), font="Courier 30 italic"
                                )

        self.nextButton.config(bg=colour)  # Changing the colour of the button to match the background
        self.canvas.create_window(300, 490, window=self.nextButton)  # Displaying next button
        self.canvas.create_window(560, 570, window=self.quitButton)  # Displaying quit button

    def finalScreen(self, score, totalQuestions):
        """
        Need to create background images
        Takes the final score in terms of int, takes the total questions in terms of int.
        """
        self.canvas.delete("all")  # Clear the screen

        self.canvas.create_image(300, 300, image=self.bImage)  # Displaying background image
        self.canvas.create_text(300, 50,  # Displaying title of the window
                                text="Your Final Score", font="Courier 30 italic"
                                )
        self.canvas.create_text(300, 350,  # Displaying score over the final score.
                                text="{}/{}".format(score, totalQuestions),
                                font="Courier 70 italic", fill="#ff00aa"
                                )  # Purple

        self.canvas.create_window(300, 490, window=self.restartButton)  # Display restart button (To welcomeScreen())
        self.canvas.create_window(560, 570, window=self.quitButton)  # Display quit button

    def overlayCreate(self, event, qaDict):
        """
        Method to create an overlay which will display the past questions and user's input
        will be called by bind. requires an unused event variable
        also requires a dictionary of questions with a list of user input (str) and correct (bool) as value
        """

        # Create a top row of headings for each column
        for x, text in enumerate(["Question", "Your Answer", "Actual Answer"]):
            Label(self.overlayFrame,
                  text=text, font="Courier 10 italic",
                  bg="#c9efff"  # Lighter blue background
                  ).grid(row=0, column=x)

        # If there are no inputs yet, display non error message.
        if len(qaDict) == 0:
            self.noneError.grid(row=1, columnspan=3, pady=200)

        for y, question in enumerate(qaDict):
            self.noneError.grid_forget()  # if there are inputs (for loop will only run with stuff in dict) clear error
            colour = "#9effb0" if qaDict[question][1] else "#ff9ead"  # light green if correct, else light red
            displayList = [question, qaDict[question][0], eval(question)]  # list: question, user input, real answer

            for x, values in enumerate(displayList):  # Displaying everything in the list as a label
                Label(self.overlayFrame,
                      text=values, bg=colour,
                      height=1, width=19,  # Defining width of and height of the label to ensure correct formatting
                      font="Courier 10 italic"
                      ).grid(row=y+1, column=x, pady=0)  # pady to make sure that the space between is 0

        self.overlayFrame.grid_propagate(0)  # Ensuring that the frame is of the specified size
        self.overlayFrame.grid_anchor(N)  # Centering the grid
        self.overlayFrame.place(x=50, y=50)
        self.overlayFrame.lift(aboveThis=None)

    def overlayRemove(self, event):
        """
        Method to remove the overlay created by overlayCreate()
        Is called by a bind, requires an unused event
        """
        self.overlayFrame.place_forget()  # hide the frame

class processes(windowSetup):
    """
    Class responsible for all processes, checking answer validity, correctness, running the actual game etc.
    """
    def __init__(self):
        """
        Method that initialises the windowSetup class
        Configuring the buttons of the windowSetup class with the proper methods
        Calling the welcomeScreen method to start the game
        """
        windowSetup.__init__(self)

        # Configuring buttons with correct functions
        self.startButton.config(command=self.gameStart)
        self.restartButton.config(command=self.welcomeScreen)

        self.welcomeScreen()  # Starting the game

    def gameStart(self):
        """
        Method which is called by the startButton
        In general is responsible for running every method
        Runs the setting check button, resets scores and Dicts
        Decides based on mode setting whether to run while or for loop
        Runs the windowSequence method multiple times to create multiple questions
        """

        for widget in self.overlayFrame.winfo_children():  # Clearing things inside the overlay (Incase of restart)
            widget.grid_forget()

        self.score = 0  # resetting the score and the dict of questions
        self.qaDict = {}

        # Binding right click and right click release to functions
        self.canvas.bind("<Button-3>", lambda event: self.overlayCreate(event, self.qaDict))  # Create on click
        self.canvas.bind("<ButtonRelease-3>", self.overlayRemove)  # Destroy on click

        if self.settingCheck():  # If settingCheck == 1; All of the settings are correct
            if self.modeVar.get() == 1:  # If it is round mode
                # Disable the round entry
                # (accounting for bug in which the user could still type into entry even after has gone)
                self.roundEntry.config(state=DISABLED)

                # Running the windowSequence the number of times specified by user
                for n in range(1, int(self.roundEntry.get())+1):
                    self.windowSequence(n)   # running a sequence which will display question and ans screen

                # Displaying final screen at the end
                self.finalScreen(self.score, int(self.roundEntry.get()))

            elif self.modeVar.get() == 2:  # If it is unlimited mode
                # Cannot have an infinate number of questions listed, hence unbind overlay
                self.canvas.unbind("<Button-3>")
                self.canvas.unbind("<ButtonRelease-3>")

                questionNo = 0  # defining variable to count the num of questions
                while 1:
                    questionNo += 1  # adding one to count
                    self.windowSequence(questionNo)  # running a sequence which will display question and ans screen

        # if settings are not correct
        else:
            self.canvas.unbind("<Button-3>")
            self.canvas.unbind("<ButtonRelease-3>")

    def windowSequence(self, questionNumber):
        """
        A method which will call the questionScreen, then subsequently, the answerScreen
        """
        self.inputBox.delete(0, "end")  # Clearing the input box of any previous inputs
        self.questionCaller()  # generating a question
        self.questionScreen(self.question, questionNumber)  # Display questionScreen

        while 1:
            self.inputButton.wait_variable(self.inputVar)  # Wait until inputVar is updated
            if self.inputCheck(self.inputVar.get()):  # Check if inputVar is valid
                break  # If valid continue with code
            continue  # If invalid stop code wait again
        correctOrFalse = self.answerCheck(question=self.question, input=self.inputVar.get())  # Check if ans is correct
        self.answerScreen(question=self.question,  # Display answerScreen
                            uInput=self.inputVar.get(),
                            correct=correctOrFalse
                            )

        self.qaDict[self.question] = [self.inputVar.get(), correctOrFalse]  # add question userinput and correct to dict

        self.nextButton.wait_variable(self.nextVar)  # Waiting for nextButton press

    def settingCheck(self):
        """
        Method to check validity of settings
        """
        validSetting = 1  # Assume setting is correct
        # Create dictionary of game types and the output of the corresponding radio buttons
        self.settings = {"addition":self.addVar.get(),
                         "subtraction":self.subVar.get(),
                         "multiplication":self.multVar.get()
                         }
        # Dictionary of enabled settings, set to 0 to denote that the question type has not been asked
        self.sDict = {variable: 0 for variable in self.settings if self.settings[variable]}

        if self.modeVar.get() == 1:  # if round mode (overlay should not work in unlimited)
            try:
                int(self.roundEntry.get())  # Check if round input can be integer
            except:  # If not, display error
                self.roundEntryError.grid(row=2, column=2)
                validSetting = 0  # declare settings to be invalid
            else:  # If round input is an integer
                # Check to see if input is at least the same as the number of inputs
                if int(self.roundEntry.get()) > 20 or int(self.roundEntry.get()) < len(self.sDict):
                    self.roundEntryError.grid(row=2, column=2)
                    validSetting = 0
                else:
                    self.roundEntryError.grid_forget()

        elif self.modeVar.get() == 2:  # If unlimited mode destroy round error message
            if self.roundEntryError in self.rFrame.winfo_children():
                self.roundEntryError.grid_forget()

        if len(self.sDict) == 0:  # If nothing in the enabled dictionary, kick up an error
            self.gameTypeError.grid(row=3, column=0, columnspan=3)
            validSetting = 0

        else:  # If something in dictionary, erase the error
            if self.gameTypeError in self.cFrame.winfo_children():
                self.gameTypeError.grid_forget()

        return(validSetting)  # Return the boolean to declare setting valid or invalid

    def inputCheck(self, input):
        """
        Method to check validity of input
        Takes input as str
        """
        try:  # Check if input can be turned into a string
            int(input)
        except:
            self.canvas.create_window(300, 360, window=self.inputError)  # Display input error
            return(0)  # Stop, and return false
        if len(input) > 12:
            self.canvas.create_window(300, 435, window=self.tooLongError)  # Display too long error
            return(0)  # Stop, and return false
        return(1)  # Stop, and return true

    def answerCheck(self, input, question):
        """
        Method to check answer
        Takes user input and question. both as str
        """
        if eval(question) != eval(input):  # if uInput is not correct
            return(0)  # Return false
        self.score += 1  # Add one to score
        return(1)  # Return true

    def questionCaller(self):
        """
        Method to create question
        """
        if 0 in self.sDict.values():  # If something has not been played
            # Choose a random question type from gameType that have not been played
            nextQuestion = choice([key for key in self.sDict.keys() if self.sDict[key]==0])
            self.sDict[nextQuestion] = 1  # Denote question type as having been performed
        else:  # If everything has been played, choose randomly
            nextQuestion = choice([key for key in self.sDict.keys()])  # If all the questions were asked at least once generate random question

        # Calling appropriate functions
        if nextQuestion == "addition":
            self.addCreator()
        elif nextQuestion == "subtraction":
            self.subCreator()
        elif nextQuestion == "multiplication":
            self.multCreator()

    def addCreator(self):
        """
        Method to define self.question randomly (addition)
        """
        # define self.question as as a string with 2 random numbers
        self.question = "{}+{}".format(randint(10, 99), randint(2, 99))

    def subCreator(self):
        """
        Method to define self.quesiton randomly (subtraction)
        """
        firstNumber = randint(10, 99)
        while 1:
            secondNumber = randint(5, 98)
            if secondNumber >= firstNumber:
                continue
            break
        # second number must be greater than the first
        self.question = "{}-{}".format(firstNumber, secondNumber)

    def multCreator(self):
        """
        Method to define self.question randomly (multiplication)
        """
        self.question = "{}*{}".format(randint(2, 9), randint(2, 9))

start = processes()
start.window.mainloop()