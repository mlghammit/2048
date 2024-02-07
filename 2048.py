###################
### 2048 Remake ###
### Hamza K     ###
###################

# Importing libaries
import tkinter as tk
import random

# Defining Game class, inherit tk.Tk for GUI 
class Game(tk.Tk):
    # Static variables
    board = [] # Hold game board matrix 
    newTileSelection = [2] * 6 + [4] # Probability for new tiles
    score = 0 # Tracker
    highscore = 0 # Tracker
    scoreString = 0 # UI display
    highscoreString = 0 # UI display


    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)

        self.scoreString = tk.StringVar(self, "0")
        self.highscoreString = tk.StringVar(self, "0")

        # Buttons & Labels
        self.createWidgets()

        # Canvas where game board will be drawn
        self.canvas = tk.Canvas(self, width = 410, height = 410, borderwidth = 5, highlightthickness = 0)
        self.canvas.pack(side="top", fill="both", expand=False)

        self.newGame()

    def addNewTile(self):
        index = random.randint(0,6)
        x, y = -1, -1
        while self.isFull() == False:
            x, y = random.randint(0,3), random.randint(0,3)
            if (self.board[x][y] == 0):
                self.board[x][y] = self.newTileSelection[index]
                # Drawing tile on canvas
                x1, y1 = y * 105, x * 105
                x2, y2 = x1 + 100, y1 + 100
                num = self.board[x][y]
                if num == 2:
                    self.square[x,y] = self.canvas.create_rectangle(x1,y1,x2,y2, fill="#e0f2f8", tags="rectangle", outline="", width=0)
                    self.canvas.create_text((x1 + x2)/2, (y1+y2)/2, font=("Arial", 36), fill="#ffb459", text="2")
                elif num == 4:
                    self.square[x,y] = self.canvas.create_rectangle(x1,y1,x2,y2, fill="#b8dbe5", tags="rectangle", outline="", width=0)
                    self.canvas.create_text((x1 + x2)/2, (y1+y2)/2, font=("Arial", 36), fill="#ffb459", text="4")
                break

    def isFull(self):
        return all(self.board[x][y] != 0 for x in range(4) for y in range(4)) 
   

    ## Designing the board

    def printBoard(self):
        cell_width, cell_height = 105, 105 # Dimensions for each tile
        self.square = {} # Directory for tiles

        # Clear existing tile 
        self.canvas.delete("rectangle")

        # Color mapping for numbers
        color_map = {
            0: "#CCC0B3",
            2: "#EEE4DA",
            4: "#EDE0DA",
            8: "#F2B179",
            16: "#F59563",
            32: "#F67C5F",
            64: "#F65E3B",
            128: "#EDCF72",
            256: "#EDCC61",
            512: "#EDC850",
            1024: "#EDC53F",
            2048: "#EDC22E",
        }

        # Drawing on canvas
        for row in range(4):
            for column in range(4):
                num = self.board[row][column]
                x1, y1 = column * 105, row * 105
                x2, y2 = x1 + 100, y1 + 100

                #For any tile not listed in color_map, fill black
                fill_color = color_map.get(num, "#000000")
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color, tags="rectangle", outline="")
                if num != 0:
                    font_size = 36 if num < 126 else 30 
                    self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, font=("Arial", font_size), fill = "#494949", text=str(num))

    def createWidgets(self):
        # Packing and filling frame to hold button
        button_frame = tk.Frame(self)
        button_frame.pack(side="top", fill="x")

        # Start game
        tk.Button(button_frame, text="New Game", command=self.newGame).pack(side="left")
        
        # Label displaying current score
        tk.Label(button_frame, text="Score:").pack(side="left")
        self.scoreString = tk.StringVar(self, "0") # StringVar to update dynamically
        tk.Label(button_frame, textvariable=self.scoreString).pack(side="left")
        
        # Label displaying high score
        tk.Label(button_frame, text="High Score:").pack(side="left")
        self.highscoreString = tk.StringVar(self, "0") # StringVar to update dynamically
        tk.Label(button_frame, textvariable=self.highscoreString).pack(side="left")

    ### Movement


    def keyPressed(self,event):
        shift = 0
        # Logic to handle moving down, moves every piece it can down, repeat with each step. merging where possible
        # Update score each merge, Resets shift each round, similar logic for Right, Left, Up
        if event.keysym == 'Down':
            for j in range(0,4):
                shift = 0
                for i in range(3,-1,-1):
                    if self.board[i][j] == 0:
                        shift += 1
                    else:
                        if i - 1 >= 0 and self.board[i-1][j] == self.board[i][j]:
                            self.board[i][j] *= 2
                            self.score += self.board[i][j]
                            self.board[i-1][j] = 0
                        elif i - 2 >= 0 and self.board[i-1][j] == 0 and self.board[i-2][j] == self.board[i][j]:
                            self.board[i][j] *= 2
                            self.score += self.board[i][j]
                            self.board[i-2][j] = 0
                        elif i == 3 and self.board[2][j] + self.board[1][j] == 0 and self.board[0][j] == self.board[3][j]:
                            self.board[3][j] *= 2
                            self.score += self.board[3][j]
                            self.board[0][j] = 0
                        if shift > 0:
                            self.board[i+shift][j] = self.board[i][j]
                            self.board[i][j] = 0
            self.printBoard()
            self.addNewTile()
            self.isOver()
        elif event.keysym == 'Right':
            for i in range(0,4):
                shift = 0
                for j in range(3,-1,-1):
                    if self.board[i][j] == 0:
                        shift += 1
                    else:
                        if j - 1 >= 0 and self.board[i][j-1] == self.board[i][j]:
                            self.board[i][j] *= 2
                            self.score += self.board[i][j]
                            self.board[i][j-1] = 0
                        elif j - 2 >= 0 and self.board[i][j-1] == 0 and self.board[i][j-2] == self.board[i][j]:
                            self.board[i][j] *= 2
                            self.score += self.board[i][j]
                            self.board[i][j-2] = 0
                        elif j == 3 and self.board[i][2] + self.board[i][1] == 0 and self.board[0][j] == self.board[3][j]:
                            self.board[i][3] *= 2
                            self.score += self.board[i][3]
                            self.board[i][0] = 0
                        if shift > 0:
                            self.board[i][j+shift] = self.board[i][j]
                            self.board[i][j] = 0
            self.printBoard()
            self.addNewTile()
            self.isOver()
        elif event.keysym == 'Left':
            for i in range(0,4):
                shift = 0
                for j in range(0,4):
                    if self.board[i][j] == 0:
                        shift += 1
                    else:
                        if j + 1 < 4 and self.board[i][j+1] == self.board[i][j]:
                            self.board[i][j] *= 2
                            self.score += self.board[i][j]
                            self.board[i][j+1] = 0
                        elif j + 2 < 4 and self.board[i][j+1] == 0 and self.board[i][j+2] == self.board[i][j]:
                            self.board[i][j] *= 2
                            self.score += self.board[i][j]
                            self.board[i][j+2] = 0
                        elif j == 0 and self.board[i][1] + self.board[i][2] == 0 and self.board[i][3] == self.board[i][0]:
                            self.board[i][0] *= 2
                            self.score += self.board[i][0]
                            self.board[i][3] = 0
                        if shift > 0:
                            self.board[i][j-shift] = self.board[i][j]
                            self.board[i][j] = 0
            self.printBoard()
            self.addNewTile()
            self.isOver()
        elif event.keysym == 'Up':
            for j in range(0,4):
                shift = 0
                for i in range(0,4):
                    if self.board[i][j] == 0:
                        shift += 1
                    else:
                        if i + 1 < 4 and self.board[i+1][j] == self.board[i][j]:
                            self.board[i][j] *= 2
                            self.score += self.board[i][j]
                            self.board[i+1][j] = 0
                        elif i + 2 < 4 and self.board[i+1][j] == 0 and self.board[i+2][j] == self.board[i][j]:
                            self.board[i][j] *= 2
                            self.score += self.board[i][j]
                            self.board[i+2][j] = 0
                        elif i == 0 and self.board[1][j] + self.board[2][j] == 0 and self.board[3][j] == self.board[0][j]:
                            self.board[0][j] *= 2
                            self.score += self.board[0][j]
                            self.board[3][j] = 0
                        if shift > 0:
                            self.board[i-shift][j] = self.board[i][j]
                            self.board[i][j] = 0
            self.printBoard()
            self.addNewTile()
            self.isOver()
        self.scoreString.set(str(self.score))
        if self.score > self.highscore:
            self.highscore = self.score
            self.highscoreString.set(str(self.highscore))
    ### New game

    def newGame (self):
        self.score = 0 # Reset score
        self.scoreString.set("0") # Update score display
        self.board = [[0 for _ in range(4)] for _ in range(4)] # Resets board
        
        # Place initial tile
        while True:
            x = random.randint(0,3)
            y = random.randint(0,3)
            if (self.board[x][y] == 0):
                self.board[x][y] = 2
                break
        index = random.randint(0,6)
        # Add second tile
        while self.isFull() == False:
            x = random.randint(0,3)
            y = random.randint(0,3)
            if (self.board[x][y] == 0):
                self.board[x][y] = self.newTileSelection[index]
                break
        self.printBoard()

    def isOver(self):
    #Check for empty space
        for i in range(4):
            for j in range(4):
                if self.board[i][j] == 0:
                    return False
                
                #Check for merges
                if (j < 3 and self.board[i][j] == self.board[i][j + 1]) or (i < 3 and self.board[i][j] == self.board[i + 1][j]):
                    return False
                
        #Print game over if no empty and no merges
        self.GameOverScreen()
        return True
    def GameOverScreen(self):
        self.canvas.create_text(205, 205, text="GAME OVER", font=("Arial", 46, "bold"), fill="#48D1CC", tags="gameover" )

                

if __name__ == "__main__":
    app = Game()
    app.bind_all('<Key>', app.keyPressed)
    app.wm_title("2048")
    app.minsize(420, 450)
    app.maxsize(420, 450)
    app.mainloop()