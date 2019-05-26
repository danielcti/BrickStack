import pygame
import time
import random
from brick import Brick
from hand import Hand
##################
#
#  CRIAR O HAND.CONTACT_X PRA SER DO CENTRO DO BLOCO
#
#
###################
pygame.init()

WIDTH = 800
HEIGHT = 600
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BRIGHTED_RED = (200,0,0)
BRIGHTED_GREEN = (0,200,0)

gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))
background = pygame.image.load('resources/background.png')
pygame.display.set_caption('Falling blocks')
levelSound = pygame.mixer.Sound('resources/levelUp.wav')
scoreSound = pygame.mixer.Sound('resources/score.wav')
loseSound = pygame.mixer.Sound('resources/game_over.wav')
clock = pygame.time.Clock()
brickList = []
actualBrick = 0

def collision(hand,difficulty):
    global brickList, actualBrick
    
    brickList[actualBrick].speed = 0
    brickList[actualBrick].collide = True
    hand.contactPoint = hand.y - len(brickList) * brickList[actualBrick].height

    newBrick = Brick(random.randrange(0,WIDTH-60),-600,5 + 2*difficulty) # adiciona o proximo e empilha
    actualBrick += 1
    brickList.append(newBrick)

def brickMove():
    brickList[actualBrick].y += brickList[actualBrick].speed
    for brick in brickList:
        gameDisplay.blit(brick.sprite, (brick.x, brick.y))

def handMove(hand):

    hand.x += hand.speed
    if hand.side == 'right':
        gameDisplay.blit(hand.right_sprite, (hand.x,hand.y))
    elif hand.side == 'left':
        gameDisplay.blit(hand.left_sprite, (hand.x,hand.y))
    for i, brick in enumerate(brickList, start=0):
        if brick.collide == True: # se esta parado passa a acompanhar a mao
            brick.x = hand.x + 0.25*hand.width # para e coloca no meio da mao
            brick.y = hand.y - brick.height - (i*brick.height) # para empilhar certinho

def text_objects(text, font):
    textSurf = font.render(text,True, BLACK)
    return textSurf, textSurf.get_rect()

def bricks_stacked(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Score: " + str(count), True, (255,0,0))
    gameDisplay.blit(text, (0,0))

def print_Time(time):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Time alive: " + str(time), True, (255,0,0))
    gameDisplay.blit(text, (WIDTH * 0.83,0))

def message_display(text,size,x,y):
    largeText = pygame.font.Font('freesansbold.ttf', size)
    textSurf, textRect = text_objects(text, largeText)
    textRect.center = (x,y)
    gameDisplay.blit(textSurf, textRect)

    pygame.display.update()

    time.sleep(1)

def init_game():
    hand_x = WIDTH * 0.45 # initial x
    hand_y = HEIGHT - 100 # initial y
    newHand = Hand(hand_x,hand_y,0) # o 0 eh a velocidade, pois a mao comeca parada
    myBrick = Brick(random.randrange(0,WIDTH-60),-600,5)
    brickList.append(myBrick)
    return newHand

def isCollision(hand):
    bx,by,bh,bw = brickList[actualBrick].x,brickList[actualBrick].y,brickList[actualBrick].height,brickList[actualBrick].width
    hx,hy,hw,hc = hand.x,hand.y,hand.width,hand.contactPoint
    if len(brickList) == 1:
        if(bx > hx and bx+bw < hx+hw):
            if(by+bh < hy+10) and (by+bh > hy-10):
                return True
    else:
        if(by+bh < hc+10) and (by+bh > hc-10):
            if(bx > hx and bx+bw < hx+hw):
                return True
    return False

def levelUp(difficulty):
    global brickList
    del brickList[:]
    
    myBrick = Brick(random.randrange(0,WIDTH-60),-600,5 + 2*difficulty)
    brickList.append(myBrick)
    
    global actualBrick 
    actualBrick = 0
    
    levelSound.play()

def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    # print(click)
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac,(x,y,w,h))

        if click[0] == 1 and action != None:
            action()         
    else:
        pygame.draw.rect(gameDisplay, ic,(x,y,w,h))

    smallText = pygame.font.SysFont("comicsansms",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    gameDisplay.blit(textSurf, textRect)

def quitgame():
    pygame.quit()
    quit()

def pause():
    while True:
        for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_p:
                            return
    
def game_intro():

    intro = True

    while intro:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        gameDisplay.fill(WHITE)
        largeText = pygame.font.SysFont("comicsansms",115)
        TextSurf, TextRect = text_objects("Falling blocks", largeText)
        TextRect.center = ((WIDTH/2),(HEIGHT/2))
        gameDisplay.blit(TextSurf, TextRect)

        button("GO!",150,450,100,50,GREEN,BRIGHTED_GREEN,game_loop)
        button("Quit",550,450,100,50,RED,BRIGHTED_RED,quitgame)

        pygame.display.update()
        clock.tick(15)

def lose(score, time):
    loseSound.play()
    message_display('You survived {} seconds. Better luck next time!'.format(time),30,WIDTH/2,HEIGHT*0.3)
    message_display('Press r to restart again',30,WIDTH/2,HEIGHT*0.6)
    global brickList, actualBrick
    actualBrick = 0
    del brickList[:]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game_loop()

def game_loop():
    hand = init_game() # funcao que adiciona o primeiro bloco e adiciona a mao
    start_time = time.time()
    score = 0 # quantidade de blocos empilhados
    difficulty = 0
    playing = True
 
    while playing:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    hand.speed = -10
                    hand.side = 'left'
                elif event.key == pygame.K_RIGHT:
                    hand.speed = 10
                    hand.side = 'right'
                elif event.key == pygame.K_p:
                    pause()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    hand.speed = 0
    
        gameDisplay.fill(WHITE)
        gameDisplay.blit(background, (0,0))
        brickMove()
        handMove(hand)
        actualTime = time.time() - start_time
        print_Time(round(actualTime, 2))
        bricks_stacked(score)
        # # o bloco chegou ao fim da tela
        if brickList[actualBrick].y > HEIGHT:
            score -= 2
            # loseSound.play()
            brickList[actualBrick].y = 0 - brickList[actualBrick].height
            brickList[actualBrick].x = random.randrange(0, WIDTH)
        # #o brick tocou na mao
        if isCollision(hand):
            collision(hand,difficulty)
            score += 1
            scoreSound.play()
            # print(stack)
        if len(brickList) == 6:
            difficulty += 1
            # time.sleep(0.5)
            levelUp(difficulty)
            score += 2
            message_display('BONUS! +2',115,WIDTH/2,HEIGHT/2)
            print('level up, difficulty = ' + str(difficulty))
        if score < 0: # lose
            lose(score,round(actualTime,2))
        pygame.display.update() # atualiza tudo na tela

        clock.tick(60) # FPS


game_intro()
game_loop() # main loop