"""
Noughts and Crosses
Ron Zhang, Kevin Kim
"""

from tkinter import *
from collections import Counter

mode = "Player vs Player"

#main function that will set up the window
def main():
    global canvas, window
    #Initialising window
    window = Tk()
    window.title("Noughts and Crosses")

    #Setting up the side frame
    sideFrame = Frame(window)

    #Setting up objects inside frame
    modeButton = Button(sideFrame, text="Change Mode", width=15, bg="#99ff99", activebackground="#00ff00", command=modeToggle)
    clearButton = Button(sideFrame, text="Clear", width=15, bg="#9999ff", activebackground="#5555ff", command=init)
    quitButton = Button(sideFrame, text="Quit", width=15, bg="#ff9999", activebackground="#ff0000", command=suspend)

    modeButton.pack()
    clearButton.pack()
    quitButton.pack()

    #Setting up the canvas
    canvas = Canvas(window, width=500, height=500, bg="#77eeff")

    #Packing things
    sideFrame.pack(side=RIGHT)
    canvas.pack(side=LEFT)

    #Drawing things in canvas
    init()

    window.mainloop()

#Function to draw and update the nessesary components
def init(event=None):
    global modeText, roundText, turnText, shapeX, shapeO

    clear()#Defining default variables

    #Establishing the grid inside the canvas - Border 10, Square width = 150, actual width = 140
    for y in range(3):
        for x in range(3):
            canvas.create_rectangle(
                                    25 + 150 * x, 25 + 150 * y,
                                    175 + 150 * x, 175 + 150 * y,
                                    width=10
                                    )

    #Creating the display text at the top
    modeText = canvas.create_text(20, 10, text="Mode = {}".format(mode), anchor=W)
    turnText = canvas.create_text(250, 10, text="Turn = {}".format(turn))
    roundText = canvas.create_text(480, 10, text="Round = {}".format(gameRound), anchor=E)


    #Drawing the shapes for the first time
    initCoords = [-100, -100, -100, -100]
    #Setting coords outside the canvas so that the variable exists, and can be modified later

    colour = "#53a6b2"
    shapeX = canvas.create_polygon(initCoords, fill=colour) #variable for the shape X
    shapeO = canvas.create_oval(initCoords, width="15", outline=colour) #variable for the shape Y

    #Binding the mouse
    canvas.bind("<Motion>", hoverLoc)

    if mode == "Player vs Player":
        canvas.bind("<Button-1>", clickLoc)
    elif mode == "Player vs AI":
        canvas.bind("<Button-1>", Ai)

#Update display
def display():
    canvas.itemconfig(modeText, text="Mode = {}".format(mode))
    canvas.itemconfig(turnText, text="Turn = {}".format(turn))
    canvas.itemconfig(roundText, text="Round = {}".format(gameRound))

def modeToggle():
    global mode, canvas
    if mode == "Player vs Player":
        mode = "Player vs AI"
    elif mode == "Player vs AI":
        mode = "Player vs Player"

    init()

def clear():
    global turn, gameRound, gridShape
    turn = "x"
    gameRound = 0
    gridShape = [["","",""],["","",""],["","",""]]

    canvas.delete(ALL)

def suspend():
    window.destroy()

def hoverLoc(motion):
    #Defining x and y
    x = motion.x
    y = motion.y

    #Converting x and y into grid coords
    grid = gridCalc(x, y)

    #If mouse is inside a valid grid, and there are no previous inputs in that grid
    if grid != "MouseOutOfGrid" and gridShape[grid[1]][grid[0]] == "":
        coord = objectLoc(grid)#Defining the the coordinate of the object

        #moving object to position
        if turn == 'x':
            canvas.coords(shapeX, coord)
        elif turn == "o":
            canvas.coords(shapeO, coord)


def clickLoc(event):
    global turn, gameRound

    #Defining x and y coordinate of mouse
    x = event.x
    y = event.y

    grid = gridCalc(x, y)# Translating the x y coords into grid coords

    #If mouse is inside a valid grid, and there are no previous inputs in that grid
    if grid != "MouseOutOfGrid" and gridShape[grid[1]][grid[0]] == "":

        coord = objectLoc(grid) #translating grid coord to object coord
        gameRound += 1 #Adding one to round

        if turn == "x":
            canvas.create_polygon(coord)
            gridShape[grid[1]][grid[0]] = "x"
            game = gameChecker(grid)

            turn = "o"
            display()

        elif turn == "o":
            canvas.create_oval(coord, width="15")
            gridShape[grid[1]][grid[0]] = "o"
            game = gameChecker(grid)

            turn = "x"
            display()

    if 'game' in locals():
        if game == "fin":
            canvas.bind("<Button-1>", init)

def Ai(event):
    global turn, gameRound

    #Defining x and y coordinate of mouse
    x = event.x
    y = event.y

    grid = gridCalc(x, y)# Translating the x y coords into grid coords

    #If mouse is inside a valid grid, and there are no previous inputs in that grid
    if grid != "MouseOutOfGrid" and gridShape[grid[1]][grid[0]] == "":

        coord = objectLoc(grid) #translating grid coord to object coord

        gameRound += 1 #Adding one to round

        canvas.create_polygon(coord) #No need to check to see if turn == "x" as turn is going to be "x"
        gridShape[grid[1]][grid[0]] = "x"
        game = gameChecker(grid)
        turn = "o"
        display()

        stopGame = 0

        if 'game' in locals():
            if game == "fin":
                canvas.bind("<Button-1>", init)
                stopGame = 1

        if stopGame == 0:
            grid = priorities()
            coord = objectLoc(grid)

            canvas.create_oval(coord, width="15")
            gridShape[grid[1]][grid[0]] = "o"
            game = gameChecker(grid)

            turn = "x"
            display()

        if 'game' in locals():
            if game == "fin":
               canvas.bind("<Button-1>", init)

def priorities():
        rowCheck = [gridShape[0], gridShape[1], gridShape[2]]
        columnCheck = [list(x) for x in zip(rowCheck[0], rowCheck[1], rowCheck[2])]
        leftRightCheck = [gridShape[0][0], gridShape[1][1], gridShape[2][2]]
        rightLeftCheck = [gridShape[0][2], gridShape[1][1], gridShape[2][0]]

        for rowN, row in enumerate(rowCheck):
            obCount = Counter(row)
            if obCount["o"] == 2 and ("" in row): # Checking to see if AI is 1 move away from winning in rows
                grid = [row.index(""), rowN]
                return(grid)

        for columnN, column in enumerate(columnCheck): # Checking to see if AI is 1 move away from winning in
            obCount = Counter(column)
            if obCount["o"] == 2 and ("" in column):
                grid = [columnN, column.index("")]
                return(grid)

        obCount = Counter(leftRightCheck) # Checking to see if Ai is 1 move away from winning in \
        if obCount["o"] == 2 and ("" in leftRightCheck):
            listLoc = leftRightCheck.index("")
            if listLoc == 0:
                grid = [0, 0]
            elif listLoc == 1:
                grid = [1, 1]
            elif listLoc == 2:
                grid = [2, 2]
            return(grid)

        obCount = Counter(rightLeftCheck)
        if obCount["o"] == 2 and ("" in rightLeftCheck): # Checking to see if Ai is 1 move away from winning in /
            listLoc = rightLeftCheck.index("")
            if listLoc == 0: # Defining the locations at which "" exists
                grid = [2, 0]
            elif listLoc == 1:
                grid = [1, 1]
            elif listLoc == 2:
                grid = [0, 2]
            return(grid)

        for rowN, row in enumerate(rowCheck):
            obCount = Counter(row)
            if obCount["x"] == 2 and ("" in row):  # Checking to see if player is 1 move away from winning in rows
                grid = [row.index(""), rowN]
                return(grid)

        for columnN, column in enumerate(columnCheck):  # Checking to see if player is 1 move away from winning in
            obCount = Counter(column)
            if obCount["x"] == 2 and ("" in column):
                grid = [columnN, column.index("")]
                return(grid)

        obCount = Counter(leftRightCheck)  # Checking to see if player is 1 move away from winning in \
        if obCount["x"] == 2 and ("" in leftRightCheck):
            listLoc = leftRightCheck.index("")
            if listLoc == 0:
                grid = [0, 0]
            elif listLoc == 1:
                grid = [1, 1]
            elif listLoc == 2:
                grid = [2, 2]
            return(grid)

        obCount = Counter(rightLeftCheck)
        if obCount["x"] == 2 and ("" in rightLeftCheck):  # Checking to see if player is 1 move away from winning in /
            listLoc = rightLeftCheck.index("")
            if listLoc == 0:  # Defining the locations at which "" exists
                grid = [2, 0]
            elif listLoc == 1:
                grid = [1, 1]
            elif listLoc == 2:
                grid = [0, 2]
            return(grid)
        # If middle not taken. take the middle
        if gridShape[1][1] == "":
            grid = [1, 1]
            return(grid)

        # Accounting for 2 middle grids of adjacent sides being filled, which can result in player win
        if rowCheck[0][1] == "x" and columnCheck[0][1] == "x" and gridShape[0][0] == "":
            grid = [0, 0]
            return (grid)

        if rowCheck[0][1] == "x" and columnCheck[2][1] == "x" and gridShape[0][2] == "":
            grid = [2, 0]
            return (grid)

        if rowCheck[2][1] == "x" and columnCheck[0][1] == "x" and gridShape[2][0] == "":
            grid = [0, 2]
            return (grid)

        if rowCheck[2][1] == "x" and columnCheck[2][1] == "x" and gridShape[2][2] == "":
            grid = [2, 2]
            return (grid)

        # Going to compare each corner, then each side grid in terms of the possible future wins. Then choose the side
        # With the highest chance of wins
        elif gridShape[1][1] != "":
            option1 = [0, 0, 0] # Top left corner
            option2 = [0, 0, 0] # Bottom right corner
            option3 = [0, 0, 0] # Top right corner
            option4 = [0, 0, 0] # Bottom left corner

            option5 = [0, 0] # Top side
            option6 = [0, 0] # Bottom side
            option7 = [0, 0] # Left side
            option8 = [0, 0] # Right side

            if gridShape[0][0] == "": # Top left corner
                if Counter(leftRightCheck)["x"] == 0:
                    option1[0] = 1
                if Counter(rowCheck[0])["x"] == 0:
                    option1[1] = 1
                if Counter(columnCheck[0])["x"] == 0:
                    option1[2] = 1

            if gridShape[2][2] == "": # Bottom right corner
                if Counter(leftRightCheck)["x"] == 0:
                    option2[0] = 1
                if Counter(rowCheck[2])["x"] == 0:
                    option2[1] = 1
                if Counter(columnCheck[2])["x"] == 0:
                    option2[2] = 1

            if gridShape[0][2] == "": # Top right corner
                if Counter(rightLeftCheck)["x"] == 0:
                    option3[0] = 1
                if Counter(rowCheck[0])["x"] == 0:
                    option3[1] = 1
                if Counter(columnCheck[2])["x"] == 0:
                    option3[2] = 1

            if gridShape[2][0] == "": # Bottom left corner
                if Counter(rightLeftCheck)["x"] == 0:
                    option4[0] = 1
                if Counter(rowCheck[2])["x"] == 0:
                    option4[1] = 1
                if Counter(columnCheck[0])["x"] == 0:
                    option4[2] = 1

            if gridShape[0][1] == "": # Top side
                if Counter(rowCheck[0])["x"] == 0:
                    option5[0] = 1
                if Counter(columnCheck[1])["x"] == 0:
                    option5[1] = 1

            if gridShape[2][1] == "": # Bottom side
                if Counter(rowCheck[2])["x"] == 0:
                    option6[0] = 1
                if Counter(columnCheck[1])["x"] == 0:
                    option6[1] = 1

            if gridShape[1][0] == "": # Left side
                if Counter(rowCheck[1])["x"] == 0:
                    option7[0] = 1
                if Counter(columnCheck[0])["x"] == 0:
                    option7[1] = 1

            if gridShape[1][2] == "": # Right side
                if Counter(rowCheck[1])["x"] == 0:
                    option8[0] = 1
                if Counter(columnCheck[2])["x"] == 0:
                    option8[1] = 1

            # AI can be defeated when player has one x in each adjacent side. Accounting for this.
            # Top and left
            if Counter(rowCheck[0])["x"] == 1 and Counter(columnCheck[0])["x"] == 1 and (gridShape[0][1] == "" or gridShape[1][0] == ""):
                if max(sum(option5), sum(option7)) != 0:
                    if sum(option5) >= sum(option7):#If the top side has more options
                        grid = [1, 0]
                        return (grid)
                    if sum(option7) >= sum(option5):
                        grid = [0, 1]
                        return (grid)

            # Top and right
            if Counter(rowCheck[0])["x"] == 1 and Counter(columnCheck[2])["x"] == 1 and (gridShape[0][1] == "" or gridShape[1][2] == ""):
                if max(sum(option5), sum(option8)) != 0:
                    if sum(option5) >= sum(option8):#If the top side has more options
                        grid = [1, 0]
                        return (grid)
                    if sum(option8) >= sum(option5):
                        grid = [2, 1]
                        return (grid)

            # Bottom and Left
            if Counter(rowCheck[2])["x"] == 1 and Counter(columnCheck[0])["x"] == 1 and (gridShape[2][1] == "" or gridShape[1][0] == ""):
                if max(sum(option6), sum(option7)) != 0:
                    if sum(option6) >= sum(option7):#If the top side has more options
                        grid = [1, 2]
                        return (grid)
                    if sum(option7) >= sum(option6):
                        grid = [0, 1]
                        return (grid)

            # Bottom and right
            if Counter(rowCheck[2])["x"] == 1 and Counter(columnCheck[2])["x"] == 1 and (gridShape[2][1] == "" or gridShape[1][2] == ""):
                if max(sum(option6), sum(option8)) != 0:
                    if sum(option6) >= sum(option8):#If the top side has more options
                        grid = [1, 2]
                        return (grid)
                    if sum(option8) >= sum(option6):
                        grid = [2, 1]
                        return(grid)

    # If none of the scenarios above apply, compare choices based on the number of wins that taking that grid can offer
            if max([sum(option1), sum(option2), sum(option3), sum(option4)]) != 0:
                if sum(option1) >= sum(option2) and sum(option1) >= sum(option3) and sum(option1) >= sum(option4):
                    grid = [0, 0]
                    return (grid)
                elif sum(option2) >= sum(option1) and sum(option2) >= sum(option3) and sum(option2) >= sum(option4):
                    grid = [2, 2]
                    return (grid)
                elif sum(option3) >= sum(option1) and sum(option3) >= sum(option2) and sum(option3) >= sum(option4):
                    grid = [2, 0]
                    return (grid)
                elif sum(option4) >= sum(option1) and sum(option4) >= sum(option2) and sum(option4) >= sum(option3):
                    grid = [0, 2]
                    return(grid)

            # Corners will most likely be favorable, but if none of them are valid options, go for the sides
            if max([sum(option5), sum(option6), sum(option7), sum(option8)]) != 0:
                if sum(option5) >= sum(option6) and sum(option5) >= sum(option7) and sum(option5) >= sum(option8):
                    grid = [0, 1]
                    return (grid)
                elif sum(option6) >= sum(option5) and sum(option6) >= sum(option7) and sum(option6) >= sum(option8):
                    grid = [2, 1]
                    return (grid)
                elif sum(option7) >= sum(option5) and sum(option7) >= sum(option6) and sum(option7) >= sum(option8):
                    grid = [1, 0]
                    return (grid)
                elif sum(option8) >= sum(option5) and sum(option8) >= sum(option6) and sum(option8) >= sum(option7):
                    grid = [1, 2]
                    return(grid)

        # If there are no favorable anything, is most likely going to be tied game, just take the first grid available.
            else:
                for y in range(3):
                    for x in range(3):
                        if gridShape[y][x] == "":
                            return(x, y)

#Translates xy coords to  grid coords
def gridCalc(x, y):
    if y in range(30, 170): #Row 1
        gridY = 0
        if x in range(30, 170):
            gridX = 0
        elif x in range(180, 320):
            gridX = 1
        elif x in range(330, 470):
            gridX = 2
        else:
            return("MouseOutOfGrid")

    elif y in range(180, 320): #Row 2
        gridY = 1
        if x in range(30, 170):
            gridX = 0
        elif x in range(180, 320):
            gridX = 1
        elif x in range(330, 470):
            gridX = 2
        else:
            return("MouseOutOfGrid")

    elif y in range(330, 470): #Row 3
        gridY = 2
        if x in range(30, 170):
            gridX = 0
        elif x in range(180, 320):
            gridX = 1
        elif x in range(330, 470):
            gridX = 2
        else:
            return("MouseOutOfGrid")

    else:
        return("MouseOutOfGrid")

    return([gridX, gridY])

#Function to translate grid coords to object coords
def objectLoc(grid):
    #Polygon points
    pointX = [#Points for X
                35+150*grid[0], 35+150*grid[1], #P1
                80+150*grid[0], 100+150*grid[1], #P2
                35+150*grid[0], 165+150*grid[1], #P3
                75+150*grid[0], 165+150*grid[1], #P4
                100+150*grid[0], 130+150*grid[1], #P5
                125+150*grid[0], 165+150*grid[1], #P6
                165+150*grid[0], 165+150*grid[1], #P7
                120+150*grid[0], 100+150*grid[1], #P8
                165+150*grid[0], 35+150*grid[1], #P9
                125+150*grid[0], 35+150*grid[1], #P10
                100+150*grid[0], 70+150*grid[1], #P11
                75+150*grid[0], 35+150*grid[1] #P12
            ]
    #Points for the circle
    pointO = [
                40+150*grid[0], 40+150*grid[1], #P1
                160+150*grid[0], 160+150*grid[1] #P2
            ]

    #returning points
    if turn == "o":
        return(pointO)
    elif turn == "x":
        return(pointX)

def gameChecker(grid):

    rowCheck = [gridShape[0], gridShape[1], gridShape[2]]
    columnCheck = [list(x) for x in zip(rowCheck[0], rowCheck[1], rowCheck[2])]
    leftRightCheck = [gridShape[0][0], gridShape[1][1], gridShape[2][2]]
    rightLeftCheck = [gridShape[0][2], gridShape[1][1], gridShape[2][0]]

    allCheck = []
    allCheck.extend(rowCheck)
    allCheck.extend(columnCheck)
    allCheck.append(leftRightCheck)
    allCheck.append(rightLeftCheck)

    if ["x", "x", "x"] in allCheck or ["o", "o", "o"] in allCheck:
        canvas.create_text([250, 250], text="Player {} wins!".format(turn), fill="#ee1fd0",font="CentryGothic 50 bold")
        canvas.create_text([250, 300], text="Please Click to Continue", fill="#ee1fd0", font="centrygothic 20 bold")
        return ("fin")
    elif "" not in rowCheck[0] and "" not in rowCheck[1] and "" not in rowCheck[2]:
        canvas.create_text([250, 250], text="Tied Game!", fill="#ee1fd0", font="CentryGothic 50 bold")
        canvas.create_text([250, 300], text="Please Click to Continue", fill="#ee1fd0", font="centrygothic 20 bold")
        return ("fin")
    else:
        return(None)
    
main()

