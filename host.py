import pygame
import socket
import threading
import random
from gamePage import Game
pygame.font.init()

surface = pygame.display.set_mode((600,800))
pygame.display.set_caption('Tic-tac-toe Host')

class Button:
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 400
        self.height = 100

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("comicsans", 30)
        text = font.render(self.text, 1, (255,255,255))
        surface.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2) - round(text.get_height()/2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False

def createThread(tar):
    thread = threading.Thread(target=tar)
    thread.daemon = True
    thread.start()

host = '127.0.0.1'
port = 123
conn, addr=None,None
connectionEstablished = False
socket = socket.socket()
socket.bind((host, port))
socket.listen(1)

def receiveData():
    global player
    global playerTurn
    
    while True:
        data = conn.recv(1024).decode()
        dataList = data.split('_')
        print(dataList)
        if dataList[0] =='ready':
            game.oppReady=True
        else:
            x,y=int(dataList[0]),int(dataList[1])
            if dataList[2]=='yourturn':
                playerTurn = player
            if game.getCellValue(x,y)==0:
                if player == 1:
                    oppPlayerMark="O"
                elif player == 2:
                    oppPlayerMark="X"
                game.setCellValue(x,y,oppPlayerMark)
            if dataList[3]!='-1':
                game.winner=int(dataList[3])
                print("game ended")
                game.gameOver = True
            
        

def waitForConnection():
    global connectionEstablished
    global conn
    global addr
    conn, addr = socket.accept()
    print('Client Connected')
    connectionEstablished=True
    receiveData()




game = Game()
runing= True
run = False
playing="True"
btn = Button("Ready", 100, 400, (200,200,200))

createThread(waitForConnection)



while runing:
    for event in pygame.event.get():
        surface.fill((30,30,30))
        btn.draw(surface)
        if event.type == pygame.QUIT:
            runing = False
        if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if btn.click(pos):
                        player=int(random.choice([1,2]))
                        game.ready=True
                        sendData = (f'ready_{player}').encode()
                        conn.send(sendData)
    if game.ready == True:
        game.drawWaitingForOpponents(surface)
        
    pygame.display.flip()
    if game.oppReady and game.ready:
        game.clearGame()
        playerTurn= 1
        run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False
                runing=False
            if game.winner!=-1:
                game.gameOverScreen(surface,player)
                run = False
                game.clearGame()
            if event.type == pygame.MOUSEBUTTONDOWN and connectionEstablished:
                if pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    gridX = pos[0]// 200
                    gridY = (pos[1]-200)// 200
                    if gridX>=0 and gridY>=0 and playerTurn==player and not game.gameOver:
                        print(gridX, gridY)
                        game.getMouse(gridX, gridY, playerTurn)
                        sendData = (f'{gridX}_{gridY}_{"yourturn"}_{game.winner}').encode()
                        conn.send(sendData)
                        if game.winner!=-1:
                            game.gameOverScreen(surface,player)
                            run = False
                            game.clearGame()
                        if game.switchPlayer:
                            if playerTurn == 1:
                                playerTurn = 2
                            else: 
                                playerTurn = 1
                

                        game.printGrid()
                        
        surface.fill((0,0,0))
        game.drawGrid(surface)
        whoTurn = f'player {playerTurn}\'s turn'
        game.drawWhoTurn(surface,player,whoTurn)
        pygame.display.flip()
    