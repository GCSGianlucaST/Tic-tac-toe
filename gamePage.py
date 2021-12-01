import pygame
import os

letterX = pygame.image.load(os.path.join('images','letterX.png'))
letterO = pygame.image.load(os.path.join('images','letterO.png'))

pygame.font.init()

class Game:
    def __init__(self):
        self.ready=False
        self.oppReady=False
        self.gameOver = False
        self.gridLines = [ #(Start of line),(End of line)
                            ((0,400),(600,400)),
                           ((0,600),(600,600)),
                            ((200,200),(200,800)),
                            ((400,200),(400,800))]

        self.grid = [[0 for x in range(3)] for y in range(3)]
        self.switchPlayer = True
         #check direction  top    top-R   R   bot-R  bot   bot-L    L    top-L
        self.searchDir = [(0,-1),(1,-1),(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1)]
        self.winner = -1
        
    def drawWaitingForOpponents(self,surface):
        font = pygame.font.SysFont("comicsans", 30)
        surface.fill((30,30,30))
        waitingText = font.render("Waiting for opponent", True, (200,200,200) )
        surface.blit(waitingText,(150,400))

    def drawGrid(self, surface):

        for line in self.gridLines:
            pygame.draw.line(surface, (200,200,200), line[0],line[1], 2)

            for y in range (len(self.grid)):
                for x in range(len(self.grid[y])):
                    if self.getCellValue(x,y) == "X":
                        surface.blit(letterX,(x*200,y*200+200))
                    if self.getCellValue(x,y) == "O":
                        surface.blit(letterO,(x*200,y*200+200))
        
    def drawWhoTurn(self, surface,playerID,whoTurn):
        font = pygame.font.SysFont("comicsans", 30)
        displayID = font.render("You are player " + str(playerID), True, (200,200,200) )
        displayTurn = font.render("It is currently player " + str(whoTurn), True, (200,200,200) )
        surface.blit(displayID,(200,20))
        surface.blit(displayTurn,(40,100))

    def getCellValue(self,x,y):
        return self.grid[y][x]

    def setCellValue(self, x,y,value):
        self.grid[y][x]= value

    def getMouse(self, x, y, playerTurn):
        if self.getCellValue(x,y)==0:
            self.switchPlayer=True
            if playerTurn == 1:
                self.setCellValue(x,y,"X")
            elif playerTurn == 2:
                self.setCellValue(x,y,"O")
            self.checkWin(x,y,playerTurn)
        else:
            self.switchPlayer=False

    def boxExists(self,x,y):
        return x>=0 and x<3 and y>=0 and y<3

    # to check each direction and see if there is a matching mark
    # and if there is then it continues to look in that direction for 3 marks in a line
    # and returns the winner
    def checkWin(self,x,y,player):
        count = 1
        if player == 1: playerMark = "X"
        else: playerMark = "O"
        for index,(dX, dY) in enumerate(self.searchDir):
            if self.boxExists(x+dX,y+dY) and self.getCellValue(x+dX,y+dY)==playerMark:
                count+=1
                xx=x+dX
                yy=y+dY
                if self.boxExists(xx+dX, yy+dY) and self.getCellValue(xx+dX,yy+dY)== playerMark:
                    count+=1
                    if count==3:break
                if count < 3: 
                    newDir=0
                    #checking opp dir
                    if index == 0: newDir=self.searchDir[4] #top to bot
                    elif index == 1: newDir=self.searchDir[5] #top-R to bot-L
                    elif index == 2: newDir=self.searchDir[6] #R to L
                    elif index == 3: newDir=self.searchDir[7] #bot-R to top-L
                    elif index == 4: newDir=self.searchDir[0] #bot to top
                    elif index == 5: newDir=self.searchDir[1] #bot-L to top-R
                    elif index == 6: newDir=self.searchDir[2] #L to R
                    elif index == 7: newDir=self.searchDir[3] #top-L to bot-R

                    if self.boxExists(x+newDir[0], y+newDir[1]) and self.getCellValue(x+newDir[0], y+newDir[1]) == playerMark:
                        count +=1
                        if count == 3:break
                    else: 
                        count=1
        
        if count ==3:
            print(player,"wins")
            self.winner=player
            self.gameOver= True

        #check for a tie
        elif (0 not in self.grid[0]) and (0 not in self.grid[1]) and (0 not in self.grid[2]):
            print("is tie")
            self.winner=0
            self.gameOver= True

    def gameOverScreen(self,surface,player):
        self.drawGrid(surface)
        font = pygame.font.SysFont("comicsans", 40)
        surface.fill((0,0,0))

        #if there is a tie
        if self.winner==0: 
            text = font.render(("Its a tie"), True, (150,150,200) )
        elif self.winner==player:
            #if there is a winner
            text = font.render(("Player "+str(player)+" wins!"), True, (150,150,200) )
        else: 
            text = font.render(("You lose"), True, (200,150,150) )

        surface.blit(text,(600/2-text.get_width()/2,400))
        pygame.display.update()
        pygame.time.delay(2000)
        

    def clearGame(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                self.setCellValue(x,y,0)

        self.winner=-1
        self.ready=False
        self.oppReady=False
        self.gameOver=False

    def printGrid(self):
        for row in self.grid:
            print(row)

