#-------------------------------Import--------------------------------------  
from tkinter import *
import pyodbc
import os
import tkinter
import PIL.Image, PIL.ImageTk
import urllib.request
import re
import pytube
import pygame
from tkinter import filedialog
import time
from tkinter import Tk,ttk,Button
from tkinter import messagebox
from random import randint
import pygame, sys, random
import random 
import sys 
from pygame.locals import *
import pygame as pg 

def btn_clicked():
    print("Button Clicked")
#-------------------------------Flappt Bird Hard Game-------------------------
def fbhard():
    def draw_floor():
        screen.blit(floor,(floor_x_pos,650))
        screen.blit(floor,(floor_x_pos+432,650))
    def create_pipe():
        random_pipe_pos = random.choice(pipe_height)
        bottom_pipe = pipe_surface.get_rect(midtop =(500,random_pipe_pos))
        top_pipe = pipe_surface.get_rect(midtop =(500,random_pipe_pos-650))
        return bottom_pipe, top_pipe
    def move_pipe(pipes):
        for pipe in pipes :
            pipe.centerx -= 5
        return pipes
    def draw_pipe(pipes):
        for pipe in pipes:
            if pipe.bottom >= 600 : 
                screen.blit(pipe_surface,pipe)
            else:
                flip_pipe = pygame.transform.flip(pipe_surface,False,True)
                screen.blit(flip_pipe,pipe)
    def check_collision(pipes):
        for pipe in pipes:
            if bird_rect.colliderect(pipe):
                hit_sound.play()
                return False
        if bird_rect.top <= -75 or bird_rect.bottom >= 650:
                return False
        return True 
    def rotate_bird(bird1):
        new_bird = pygame.transform.rotozoom(bird1,-bird_movement*3,1)
        return new_bird
    def bird_animation():
        new_bird = bird_list[bird_index]
        new_bird_rect = new_bird.get_rect(center = (100,bird_rect.centery))
        return new_bird, new_bird_rect
    def score_display(game_state):
        if game_state == 'main game':
            score_surface = game_font.render(str(int(score)),True,(255,255,255))
            score_rect = score_surface.get_rect(center = (216,100))
            screen.blit(score_surface,score_rect)
        if game_state == 'game_over':
            score_surface = game_font.render(f'Score: {int(score)}',True,(255,255,255))
            score_rect = score_surface.get_rect(center = (216,100))
            screen.blit(score_surface,score_rect)

            high_score_surface = game_font.render(f'High Score: {int(high_score)}',True,(255,255,255))
            high_score_rect = high_score_surface.get_rect(center = (216,630))
            screen.blit(high_score_surface,high_score_rect)
    def update_score(score,high_score):
        if score > high_score:
            high_score = score
        return high_score
    pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
    pygame.init()
    screen= pygame.display.set_mode((432,768))
    clock = pygame.time.Clock()
    game_font = pygame.font.Font('All Game/Flappy Bird/FBHard/04B_19.ttf',35)
    #Tạo các biến cho trò chơi
    gravity = 0.25
    bird_movement = 0
    game_active = True
    score = 0
    high_score = 0
    #chèn background
    bg = pygame.image.load('All Game/Flappy Bird/FBHard/assets/background-night.png').convert()
    bg = pygame.transform.scale2x(bg)
    #chèn sàn
    floor = pygame.image.load('All Game/Flappy Bird/FBHard/assets/floor.png').convert()
    floor = pygame.transform.scale2x(floor)
    floor_x_pos = 0
    #tạo chim
    bird_down = pygame.transform.scale2x(pygame.image.load('All Game/Flappy Bird/FBHard/assets/yellowbird-downflap.png').convert_alpha())
    bird_mid = pygame.transform.scale2x(pygame.image.load('All Game/Flappy Bird/FBHard/assets/yellowbird-midflap.png').convert_alpha())
    bird_up = pygame.transform.scale2x(pygame.image.load('All Game/Flappy Bird/FBHard/assets/yellowbird-upflap.png').convert_alpha())
    bird_list= [bird_down,bird_mid,bird_up] #0 1 2
    bird_index = 0
    bird = bird_list[bird_index]
    #bird= pygame.image.load('assets/yellowbird-midflap.png').convert_alpha()
    #bird = pygame.transform.scale2x(bird)
    bird_rect = bird.get_rect(center = (100,384))

    #tạo timer cho bird
    birdflap = pygame.USEREVENT + 1
    pygame.time.set_timer(birdflap,200)
    #tạo ống
    pipe_surface = pygame.image.load('All Game/Flappy Bird/FBHard/assets/pipe-green.png').convert()
    pipe_surface = pygame.transform.scale2x(pipe_surface)
    pipe_list =[]
    #tạo timer
    spawnpipe= pygame.USEREVENT
    pygame.time.set_timer(spawnpipe, 1200)
    pipe_height = [200,300,400]
    #Tạo màn hình kết thúc
    game_over_surface = pygame.transform.scale2x(pygame.image.load('All Game/Flappy Bird/FBHard/assets/message.png').convert_alpha())
    game_over_rect = game_over_surface.get_rect(center=(216,384))
    #Chèn âm thanh
    flap_sound = pygame.mixer.Sound('All Game/Flappy Bird/FBHard/sound/sfx_wing.wav')
    hit_sound = pygame.mixer.Sound('All Game/Flappy Bird/FBHard/sound/sfx_hit.wav')
    score_sound = pygame.mixer.Sound('All Game/Flappy Bird/FBHard/sound/sfx_point.wav')
    score_sound_countdown = 100
    #while loop của trò chơi
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_active:
                    bird_movement = 0
                    bird_movement =-11
                    flap_sound.play()
                if event.key == pygame.K_SPACE and game_active==False:
                    game_active = True 
                    pipe_list.clear()
                    bird_rect.center = (100,384)
                    bird_movement = 0 
                    score = 0 
            if event.type == spawnpipe:
                pipe_list.extend(create_pipe())
            if event.type == birdflap:
                if bird_index < 2:
                    bird_index += 1
                else:
                    bird_index =0 
                bird, bird_rect = bird_animation()    
                
        screen.blit(bg,(0,0))
        if game_active:
            #chim
            bird_movement += gravity
            rotated_bird = rotate_bird(bird)       
            bird_rect.centery += bird_movement
            screen.blit(rotated_bird,bird_rect)
            game_active= check_collision(pipe_list)
            #ống
            pipe_list = move_pipe(pipe_list)
            draw_pipe(pipe_list)
            score += 0.01
            score_display('main game')
            score_sound_countdown -= 1
            if score_sound_countdown <= 0:
                score_sound.play()
                score_sound_countdown = 100
        else:
            screen.blit(game_over_surface,game_over_rect)
            high_score = update_score(score,high_score)
            score_display('game_over')
        #sàn
        floor_x_pos -= 1
        draw_floor()
        if floor_x_pos <= -432:
            floor_x_pos =0
        
        pygame.display.update()
        clock.tick(120)
#-------------------------------Flappt Bird Ez Game---------------------------
def fbez():
    FPS = 32
    SCREENWIDTH = 289
    SCREENHEIGHT = 511
    SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    GROUNDY = SCREENHEIGHT * 0.8
    GAME_SPRITES = {}
    GAME_SOUNDS = {}
    PLAYER = 'All Game/Flappy Bird/FBEz/gallery/sprites/bird.png'
    BACKGROUND = 'All Game/Flappy Bird/FBEz/gallery/sprites/background.png'
    PIPE = 'All Game/Flappy Bird/FBEz/gallery/sprites/pipe.png'

    def welcomeScreen():
        """
        Shows welcome images on the screen
        """

        playerx = int(SCREENWIDTH/5)
        playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2)
        messagex = int((SCREENWIDTH - GAME_SPRITES['message'].get_width())/2)
        messagey = int(SCREENHEIGHT*0.13)
        basex = 0
        while True:
            for event in pygame.event.get():
                # if user clicks on cross button, close the game
                if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()

                # If the user presses space or up key, start the game for them
                elif event.type==KEYDOWN and (event.key==K_SPACE or event.key == K_UP):
                    return
                else:
                    SCREEN.blit(GAME_SPRITES['background'], (0, 0))    
                    SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))    
                    SCREEN.blit(GAME_SPRITES['message'], (messagex,messagey ))    
                    SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))    
                    pygame.display.update()
                    FPSCLOCK.tick(FPS)

    def mainGame():
        score = 0
        playerx = int(SCREENWIDTH/5)
        playery = int(SCREENWIDTH/2)
        basex = 0

        # Create 2 pipes for blitting on the screen
        newPipe1 = getRandomPipe()
        newPipe2 = getRandomPipe()

        # my List of upper pipes
        upperPipes = [
            {'x': SCREENWIDTH+200, 'y':newPipe1[0]['y']},
            {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[0]['y']},
        ]
        # my List of lower pipes
        lowerPipes = [
            {'x': SCREENWIDTH+200, 'y':newPipe1[1]['y']},
            {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[1]['y']},
        ]

        pipeVelX = -4

        playerVelY = -9
        playerMaxVelY = 10
        playerMinVelY = -8
        playerAccY = 1

        playerFlapAccv = -8 # velocity while flapping
        playerFlapped = False # It is true only when the bird is flapping


        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                    if playery > 0:
                        playerVelY = playerFlapAccv
                        playerFlapped = True
                        GAME_SOUNDS['wing'].play()


            crashTest = isCollide(playerx, playery, upperPipes, lowerPipes) # This function will return true if the player is crashed
            if crashTest:
                return     

            #check for score
            playerMidPos = playerx + GAME_SPRITES['player'].get_width()/2
            for pipe in upperPipes:
                pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
                if pipeMidPos<= playerMidPos < pipeMidPos +4:
                    score +=1
                    print(f"Your score is {score}") 
                    GAME_SOUNDS['point'].play()


            if playerVelY <playerMaxVelY and not playerFlapped:
                playerVelY += playerAccY

            if playerFlapped:
                playerFlapped = False            
            playerHeight = GAME_SPRITES['player'].get_height()
            playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)

            # move pipes to the left
            for upperPipe , lowerPipe in zip(upperPipes, lowerPipes):
                upperPipe['x'] += pipeVelX
                lowerPipe['x'] += pipeVelX

            # Add a new pipe when the first is about to cross the leftmost part of the screen
            if 0<upperPipes[0]['x']<5:
                newpipe = getRandomPipe()
                upperPipes.append(newpipe[0])
                lowerPipes.append(newpipe[1])

            # if the pipe is out of the screen, remove it
            if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
                upperPipes.pop(0)
                lowerPipes.pop(0)
            
            # Lets blit our sprites now
            SCREEN.blit(GAME_SPRITES['background'], (0, 0))
            for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
                SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
                SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

            SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
            SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
            myDigits = [int(x) for x in list(str(score))]
            width = 0
            for digit in myDigits:
                width += GAME_SPRITES['numbers'][digit].get_width()
            Xoffset = (SCREENWIDTH - width)/2

            for digit in myDigits:
                SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCREENHEIGHT*0.12))
                Xoffset += GAME_SPRITES['numbers'][digit].get_width()
            pygame.display.update()
            FPSCLOCK.tick(FPS)

    def isCollide(playerx, playery, upperPipes, lowerPipes):
        if playery> GROUNDY - 25  or playery<0:
            GAME_SOUNDS['hit'].play()
            return True
        
        for pipe in upperPipes:
            pipeHeight = GAME_SPRITES['pipe'][0].get_height()
            if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
                GAME_SOUNDS['hit'].play()
                return True

        for pipe in lowerPipes:
            if (playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
                GAME_SOUNDS['hit'].play()
                return True

        return False

    def getRandomPipe():
        """
        Generate positions of two pipes(one bottom straight and one top rotated ) for blitting on the screen
        """
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        offset = SCREENHEIGHT/3
        y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height()  - 1.2 *offset))
        pipeX = SCREENWIDTH + 10
        y1 = pipeHeight - y2 + offset
        pipe = [
            {'x': pipeX, 'y': -y1}, #upper Pipe
            {'x': pipeX, 'y': y2} #lower Pipe
        ]
        return pipe

    if __name__ == "__main__":
        # This will be the main point from where our game will start
        pygame.init() # Initialize all pygame's modules
        FPSCLOCK = pygame.time.Clock()
        pygame.display.set_caption('Flappy Bird by CodeWithHarry')
        GAME_SPRITES['numbers'] = ( 
            pygame.image.load('All Game/Flappy Bird/FBEz/gallery/sprites/0.png').convert_alpha(),
            pygame.image.load('All Game/Flappy Bird/FBEz/gallery/sprites/1.png').convert_alpha(),
            pygame.image.load('All Game/Flappy Bird/FBEz/gallery/sprites/2.png').convert_alpha(),
            pygame.image.load('All Game/Flappy Bird/FBEz/gallery/sprites/3.png').convert_alpha(),
            pygame.image.load('All Game/Flappy Bird/FBEz/gallery/sprites/4.png').convert_alpha(),
            pygame.image.load('All Game/Flappy Bird/FBEz/gallery/sprites/5.png').convert_alpha(),
            pygame.image.load('All Game/Flappy Bird/FBEz/gallery/sprites/6.png').convert_alpha(),
            pygame.image.load('All Game/Flappy Bird/FBEz/gallery/sprites/7.png').convert_alpha(),
            pygame.image.load('All Game/Flappy Bird/FBEz/gallery/sprites/8.png').convert_alpha(),
            pygame.image.load('All Game/Flappy Bird/FBEz/gallery/sprites/9.png').convert_alpha(),
        )

        GAME_SPRITES['message'] =pygame.image.load('All Game/Flappy Bird/FBEz/gallery/sprites/message.png').convert_alpha()
        GAME_SPRITES['base'] =pygame.image.load('All Game/Flappy Bird/FBEz/gallery/sprites/base.png').convert_alpha()
        GAME_SPRITES['pipe'] =(pygame.transform.rotate(pygame.image.load( PIPE).convert_alpha(), 180), 
        pygame.image.load(PIPE).convert_alpha()
        )

        # Game sounds
        GAME_SOUNDS['die'] = pygame.mixer.Sound('All Game/Flappy Bird/FBEz/gallery/audio/die.wav')
        GAME_SOUNDS['hit'] = pygame.mixer.Sound('All Game/Flappy Bird/FBEz/gallery/audio/hit.wav')
        GAME_SOUNDS['point'] = pygame.mixer.Sound('All Game/Flappy Bird/FBEz/gallery/audio/point.wav')
        GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('All Game/Flappy Bird/FBEz/gallery/audio/swoosh.wav')
        GAME_SOUNDS['wing'] = pygame.mixer.Sound('All Game/Flappy Bird/FBEz/gallery/audio/wing.wav')

        GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
        GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()

        while True:
            welcomeScreen() # Shows welcome screen to the user until he presses a button
            mainGame() # This is the main game function 
#-------------------------------Snake Hard Game------------------------------- 
def snakehard():
    try:
        import pygame
        pygame.init()
    except:
        print("----<error>-----\nSomething wrong with pygame\nPlz run with Python 3 and make sure pygame is installed")
        input()
        exit()
    a = False
    b = False
    try:
        import random
        a = True
        import time
        b = True
    except:
        print("----<error>-----\nProblem with imported modules\nModules|Imported\nrandom |"+str(a)+"\ntime   |"+str(b)+"\nPlease fix")
    class vr:
        #grid width
        gw = 16
        #grid height
        gh = 16
        #square size
        pxl = 32
        #screen width
        sw = 0
        #screen height
        sh = 0
        #wall loop
        wl = False
        #points
        points = 0
        #color offset
        coloroffset = 8
        #is the game over
        done = False
        
    vr.sw = vr.gw*vr.pxl
    vr.sh = vr.gh*vr.pxl
    #setup
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((vr.sw, vr.sh))
    #pressed = pygame.key.get_pressed()
    c = 0;
    class apple:
        x = random.randint(1,vr.gw-2)
        y = random.randint(1,vr.gh-2)
        lvl = 0
        def place():
            apple.x = random.randint(1,vr.gw-2)
            apple.y = random.randint(1,vr.gh-2)
            while not(gamef.check(apple.x, apple.y)):
                apple.x = random.randint(1,vr.gw-2)
                apple.y = random.randint(1,vr.gh-2)
        
    class snake:
        ##x first then y
        leng = 4
        x = 5
        x = random.randint(1,vr.gw-2)
        y = random.randint(1,vr.gh-2)
        y = 16
        dire = 1
        speed = 60
        tailx = []
        taily = []
        death=0
    class bomb:
        x = random.randint(1,vr.gw-2)
        y = random.randint(1,vr.gh-2)
        def place():
            bomb.x = random.randint(1,vr.gw-2)
            bomb.y = random.randint(1,vr.gh-2)
            while not(gamef.check(apple.x, apple.y)):
                bomb.x = random.randint(1,vr.gw-2)
                bomb.y = random.randint(1,vr.gh-2)    
    class gamef:
        def check(x,y):
            for i in range(len(snake.tailx)):
                if(x == snake.tailx[i]):
                    if(y == snake.taily[i]):
                        return False
            return True
        def death():
            snake.leng = 4
            snake.x = random.randint(1,vr.gw-2)
            snake.y = random.randint(1,vr.gh-2)
            snake.dire = 5
            snake.speed = 10
            snake.tailx = []
            snake.taily = []
            snake.death +=1;
            time.sleep(0.5)
            snake.dire = 5
        def grid():
            ty = False
            for x in range(int(vr.sw/vr.pxl)):
                for y in range(int(vr.sh/vr.pxl)):
                    of = 0
                    if (y%2)==0:
                        of = 1
                    if (((x+of)%2)==0):
                        pygame.draw.rect(screen, (32,32,32),pygame.Rect(x*vr.pxl,y*vr.pxl,vr.pxl,vr.pxl))
                        
                    else:
                        pygame.draw.rect(screen, (64,64,64),pygame.Rect(x*vr.pxl,y*vr.pxl,vr.pxl,vr.pxl))
                    ty = not ty
                
        def draw():
            #Framerate of 10
            pygame.draw.rect(screen, (8,8,8),pygame.Rect(0,0,vr.pxl,vr.sh))
            pygame.draw.rect(screen, (8,8,8),pygame.Rect(vr.sw-vr.pxl,0,vr.pxl,vr.sh))
            pygame.draw.rect(screen, (8,8,8),pygame.Rect(0,0,vr.sw,vr.pxl))
            pygame.draw.rect(screen, (8,8,8),pygame.Rect(0,vr.sh-vr.pxl,vr.sw,vr.pxl))
            color=(255,0,0)
            pygame.draw.rect(screen, color, pygame.Rect(vr.pxl*bomb.x+2,vr.pxl*bomb.y+2, vr.pxl-4, vr.pxl-4))
            color=(0,255,0)
            pygame.draw.rect(screen, color, pygame.Rect(vr.pxl*apple.x+2,vr.pxl*apple.y+2, vr.pxl-4, vr.pxl-4))
            os = vr.coloroffset
            col = len(snake.tailx)*os
            print(col)
            os = vr.coloroffset
            
            for i in range(len(snake.tailx)):
                if((col-os) <= 0):
                    os=255
                else:
                    col-=os

                color = (col,col,192)
                pygame.draw.rect(screen, color, pygame.Rect(vr.pxl*snake.tailx[i],vr.pxl*snake.taily[i], vr.pxl, vr.pxl))
            color=(0,0,192)
            pygame.draw.rect(screen, color, pygame.Rect(vr.pxl*snake.x,vr.pxl*snake.y, vr.pxl, vr.pxl))
        def keyd():
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_UP]:
                snake.dire=0
            if pressed[pygame.K_RIGHT]:
                snake.dire=1
            if pressed[pygame.K_DOWN]:
                snake.dire=2
            if pressed[pygame.K_LEFT]:
                snake.dire=3
        def ref():
            gamef.tails()
            if (snake.dire == 0):
                gamef.move(0,-1)
                #snake.y -=1
            elif (snake.dire == 1):
                gamef.move(1,0)
                #snake.x+=1
            elif (snake.dire == 2):
                #snake.y+=1
                gamef.move(0,1)
            elif (snake.dire == 3):
                gamef.move(-1,0)
                #snake.x-=1
        def move(x,y):
            #x check
            if (snake.x+x)>= vr.gw-1:
                print ("out of bounds")
                snake.x = 1;
            elif(snake.x+x)<= 0:
                print ("out of bounds")
                snake.x = vr.gw-2;
            else:
                snake.x+=x
            #y check
            if (snake.y+y)>= vr.gh-1:
                print ("out of bounds")
                snake.y = 1;
            elif(snake.y+y)<= 0:
                print ("out of bounds")
                snake.y = vr.gh-2;
            else:
                snake.y+=y
            #apple
            if (snake.x == apple.x) and (snake.y == apple.y):
                snake.leng+=1
                apple.lvl+=1

                apple.place()
                bomb.place()
            elif (snake.x == bomb.x) and (snake.y == bomb.y):
                gamef.death()
                bomb.x = random.randint(1,vr.gw-2)
                bomb.y = random.randint(1,vr.gh-2)
                #print("Apple pos:\nX - "+str(apple.x)+"\nY - "+str(apple.y))
            
            
                
        def tails():
            snake.tailx.append(snake.x)
            snake.taily.append(snake.y)
            if (len(snake.tailx) > snake.leng):
                snake.tailx.pop(0)
                snake.taily.pop(0)
            
            
    while not vr.done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                vr.done = True
                exit()
                quit()

        gamef.grid()
        gamef.keyd()
        c+=1
        gamef.draw()
        if (c >= (100/snake.speed)):
            gamef.ref()
            c=0
            snake.speed+=1
        if not(snake.dire  == 5):
            pygame.display.set_caption("Snake!!!|Score: "+str(snake.leng-4))
        pygame.display.flip()
        clock.tick(40)
#-------------------------------Snake Ez Game---------------------------------
def snakeez():
    #initialize all imported pygame modules
    pg.init()

    #Our Colors
    white = (255, 255, 255)
    black = (0, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    red = (255, 0, 0)
    ceil = (19, 229, 240)
    yellow = (255, 255, 25)
    red2 = (219.3,2.6,14.27)

    #Size of Display Window
    display_width = 1000
    display_height = 680

    #Initialize a window or screen for display
    gameDisplay = pg.display.set_mode((display_width, display_height))

    #Set the current window caption
    pg.display.set_caption('Snake')


    gameExit = True

    snake_length = 10
    snake_width = 10
    snakeLen = 1

    block_size = 20
    AppleThickness = 30

    FPS = 15
    Screen_FPS = 20

    clock = pg.time.Clock()

    smallfont = pg.font.SysFont('comicsansms', 25)
    uppersmallfont = pg.font.SysFont('comicsansms', 35)
    medfont = pg.font.SysFont('comicsansms', 50)
    largefont = pg.font.SysFont('comicsansms', 75)


    img = pg.image.load('All Game/Snake/EzMenu/Snake Head.png')
    apple_img = pg.image.load('All Game/Snake/EzMenu/Apple.png')
    tail_img = pg.image.load('All Game/Snake/EzMenu/Snake Tail.png')

    icon = pg.image.load('All Game/Snake/EzMenu/Snake Head.png')
    pg.display.set_icon(icon)

    direction = 'up'


    def rotate_tail(x1, y1, x2, y2):
        x = x1 - x2
        y = y1 - y2
        if x > 0:
            return pg.transform.rotate(tail_img, 90)
        elif x < 0:
            return pg.transform.rotate(tail_img, 270)
        elif y > 0:
            return pg.transform.rotate(tail_img, 360)
        elif y < 0:
            return pg.transform.rotate(tail_img, 180)


    def snake(block_size, snakeList, snakeTail):
        tail = tail_img

        if direction == 'up':
            head = img
        elif direction == 'right':
            head = pg.transform.rotate(img, 270)
        elif direction == 'left':
            head = pg.transform.rotate(img, 90)
        elif direction == 'down':
            head = pg.transform.rotate(img, 180)


        gameDisplay.blit(head, (snakeList[-1][0], snakeList[-1][1]))
        count = 0
        for XnY in snakeList[:-1]:
            
            if count == 0:
                tail = rotate_tail(snakeList[0][0], snakeList[0][1], snakeList[1][0], snakeList[1][1])
                gameDisplay.blit(tail, (snakeList[0][0], snakeList[0][1]))
                count += 1
            else:
                pg.draw.rect(gameDisplay,red2, [XnY[0], XnY[1], block_size, block_size])

    def Apple_Gen(snakeList):
        Valid = False
        while Valid == False:
            appleX = random.randrange(0, display_width - AppleThickness, AppleThickness)
            appleY = random.randrange(0, display_height - AppleThickness, AppleThickness)
            appleXY = [appleX, appleY]
            Valid = Valid_apple(appleXY, snakeList)

        return appleX, appleY


    def Valid_apple(appleXY, snakeList):
        for eachpiece in snakeList[:-1]:
            if eachpiece == appleXY:
                return False
        return True


    def intro_screen():
        intro = True

        while intro:
            gameDisplay.fill(white)
            msg_to_screen('...Welcome to Snake game...', green, -150, 'large')
            msg_to_screen('Don\'t Think More , Just Do it ' , green, -100, 'medium')
            msg_to_screen('We Here To Eat,Just Feed Us', black, -30, 'medium')
            #msg_to_screen('if U hit edges or yourself, U die.', black, -0, 'upsmall')
            msg_to_screen('...Press C to play ,P to pause ,Q to Quit...', blue, 60, 'medium')
            msg_to_screen('...Press Escape at anytime to Leave...', blue, 100, 'medium')
            pg.display.update()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_c:
                        intro = False
                    elif event.key == pg.K_q or event.key == pg.K_ESCAPE:
                        pg.quit()
                        quit()

            clock.tick(Screen_FPS)


    def score(score):
        show = uppersmallfont.render("Score: " + str(score), True,ceil)
        gameDisplay.blit(show, (10, 10))


    def pause():
        paused = True

        msg_to_screen('Paused', red, -60, 'large')
        msg_to_screen('Let\'s Continue,Just Press C', black, -20, 'medium')
        msg_to_screen('Press Q to Quit', red, 20, 'upsmall')

        pg.display.update()

        while paused:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_c:
                        paused = False
                    elif event.key == pg.K_q or event.key == pg.K_ESCAPE:
                        pg.quit()
                        quit()

            clock.tick(FPS)


    def textObjects(msg, body_img, size='small'):
        if size == 'small':
            textSurface = smallfont.render(msg, True, body_img)
        elif size == 'medium':
            textSurface = medfont.render(msg, True, body_img)
        elif size == 'upsmall':
            textSurface = uppersmallfont.render(msg, True, body_img)
        elif size == 'large':
            textSurface = largefont.render(msg, True, body_img)
        return textSurface, textSurface.get_rect()



    def msg_to_screen(msg, body_img, y_display=0, size='small'):
        textSurface, textRect = textObjects(msg, body_img, size)
        textRect.center = (display_width // 2), (display_height // 2) + y_display
        gameDisplay.blit(textSurface, textRect)

    def gameloop():
        gameExit = True
        gameover = True

        change_x = 0
        change_y = 0

        lead_x = display_width // 2
        lead_y = display_height // 2

        snakeList = []
        global snakeLen
        snakeLen = 1
        appleX, appleY = Apple_Gen(snakeList)

        global direction
        global Screen_FPS

        event_key_temp = ''

        while gameExit:
            if gameover == False:
                msg_to_screen('Oh No Sorry...Game Over', black, -60, 'large')
                msg_to_screen('Don\'t Give Up ,Try again Just Press C',red, 60, 'medium')
                msg_to_screen('Press Q to quit',red, 100, 'medium')
                pg.display.update()

            while not gameover:

                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        gameover = True
                        gameExit = False
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_c:
                            gameloop()
                        elif event.key == pg.K_q or event.key == pg.K_ESCAPE:
                            gameover = True
                            gameExit = False

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    gameExit = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RIGHT:
                        if event_key_temp == 'left':
                            direction = 'left'
                            change_x = -block_size
                        else:
                            direction = 'right'
                            change_x = block_size
                        change_y = 0
                    elif event.key == pg.K_LEFT:
                        if event_key_temp == 'right':
                            direction = 'right'
                            change_x = block_size
                        else:
                            direction = 'left'
                            change_x = -block_size
                        change_y = 0
                    elif event.key == pg.K_UP:
                        if event_key_temp == 'down':
                            direction = 'down'
                            change_y = block_size
                        else:
                            direction = 'up'
                            change_y = -block_size
                        change_x = 0
                    elif event.key == pg.K_DOWN:
                        if event_key_temp == 'up':
                            direction = 'up'
                            change_y = -block_size
                        else:
                            direction = 'down'
                            change_y = block_size
                        change_x = 0
                    elif event.key == pg.K_p:
                        pause()

                    event_key_temp = direction

                if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    pg.quit()
                    quit()

            if lead_x >= display_width or lead_x <= -1 or lead_y >= display_height or lead_y <= -1:
                gameover = False

            lead_x += change_x
            lead_y += change_y

            if lead_x >= appleX and lead_x <= appleX + AppleThickness or lead_x + block_size >= appleX and lead_x + block_size <= appleX + AppleThickness:
                if lead_y >= appleY and lead_y <= appleY + AppleThickness or lead_y + block_size >= appleY and lead_y + block_size <= appleY + AppleThickness:
                    appleX, appleY = Apple_Gen(snakeList)
                    snakeLen += 1

            gameDisplay.fill(white)
            gameDisplay.blit(apple_img, (appleX, appleY))

            snakeHead = [lead_x, lead_y]
            snakeTail = [lead_x, lead_y + snakeLen * 20]
            snakeList.append(snakeHead)

            if len(snakeList) > snakeLen:
                del snakeList[0]
            snake(block_size, snakeList, snakeTail)

            for eachpiece in snakeList[:-1]:
                if eachpiece == snakeHead:
                    gameover = False

            score(snakeLen - 1)

            pg.display.update()
            clock.tick(FPS)

        # uninitialize all pygame modules
        pg.quit()
        snakeezmanu()


    intro_screen()
    gameloop()
#-------------------------------Caro Free Game--------------------------------
def carofree():
    pygame.font.init()
    pygame.init()

    s_width = 750
    s_height = 750
    block_size = 50
    available_spaces = (s_height / block_size) * (s_width/block_size)

    win = pygame.display.set_mode((s_width, s_height))
    pygame.display.set_caption("TicTacToe")


    class Player:
        def __init__(self, color, score=0):
            self.color = color
            self.score = score


    def draw_text_middle(surface, text, size, color, position):
        """
        write text in the middle of the page
        :param position: x, y pos
        :param surface: window
        :param text:
        :param size:
        :param color:
        :return:
        """
        font = pygame.font.SysFont("comicsans", size, bold=True)
        label = font.render(text, 1, color)

        surface.blit(label, position)


    def create_grid():
        """
        create grid aka space
        :return: grid
        """
        grid = [[None for _ in range(int(s_height/block_size))] for _ in range(int(s_width/block_size))]
        return grid


    def draw_grid(surface, grid):
        """
        draw lines separating the grid
        :param surface:
        :param grid:
        :return:
        """
        surface.fill((255, 255, 255))
        for i in range(len(grid)):
            pygame.draw.line(surface, (0, 0, 0), (0, i * block_size), (s_width, i*block_size))
            for j in range(len(grid[i])):
                pygame.draw.line(surface, (0, 0, 0), (j*block_size, 0), (j*block_size, s_height))
        pygame.display.update()


    def check_win(locked_pos, x, y, z_up, z_down, locked_pos_x):
        """
        check if player wins or not
        :param locked_pos_x: used pos for other player
        :param locked_pos: already used pos
        :param x: cur x
        :param y: cur y
        :param z_up: cur z_up
        :param z_down: cur z_down
        :return: bool
        """
        row = [(x, y, z_up, z_down)]  # initializes current value of x,y,z to lists
        col = [(x, y, z_up, z_down)]
        dia_up = [(x, y, z_up, z_down)]
        dia_down = [(x, y, z_up, z_down)]

        for element in locked_pos:
            if element[1] == y:
                row.append(element)
            if element[0] == x:
                col.append(element)
            if element[2] == z_up:
                dia_up.append(element)
            if element[3] == z_down:
                dia_down.append(element)

        row = sorted(row, key=lambda tup: tup[0])  # sort the lists according to the element that is different
        col = sorted(col, key=lambda tup: tup[1])
        dia_up = sorted(dia_up, key=lambda tup: tup[0])
        dia_down = sorted(dia_down, key=lambda tup: tup[1])

        for i in range(len(row) - 4): # iterate to find if there is 5 consecutive squares, if it is return true

            if row[i][0] + 50 == row[i+1][0] and row[i+1][0] + 50 == row[i+2][0] and row[i+2][0] + 50 == row[i+3][0] and \
                    row[i+3][0] + 50 == row[i+4][0]:  # check if there is 5 consecutive squares

                if (row[i+4][0] + 50, row[i+4][1], row[i+4][2] + 50, row[i+4][3] + 50) in locked_pos_x and \
                        (row[i][0] - 50, row[i][1], row[i][2] - 50, row[i][3] - 50) in locked_pos_x:  # check if they are "sandwiched"

                    return False

                return True

        for i in range(len(col) - 4):

            if col[i][1] + 50 == col[i+1][1] and col[i+1][1] + 50 == col[i+2][1] and col[i+2][1] + 50 == col[i+3][1] and \
                    col[i+3][1] + 50 == col[i+4][1]:

                if (col[i + 4][0], col[i + 4][1] + 50, col[i + 4][2] + 50, col[i + 4][3] - 50) in locked_pos_x and \
                        (col[i][0], col[i][1] - 50, col[i][2] - 50, col[i][3] + 50) in locked_pos_x:

                    return False

                return True
        for i in range(len(dia_up) - 4):

            if dia_up[i][0] + 50 == dia_up[i + 1][0] and dia_up[i + 1][0] + 50 == dia_up[i + 2][0] \
                    and dia_up[i + 2][0] + 50 == dia_up[i + 3][0] and dia_up[i + 3][0] + 50 == dia_up[i + 4][0]:

                if (dia_up[i + 4][0] + 50, dia_up[i + 4][1]-50, dia_up[i + 4][2], dia_up[i + 4][3] + 100) in locked_pos_x and \
                        (dia_up[i][0] - 50, dia_up[i][1]+50, dia_up[i][2], dia_up[i][3] - 100) in locked_pos_x:

                    return False

                return True

        for i in range(len(dia_down) - 4):

            if dia_down[i][1] + 50 == dia_down[i + 1][1] and dia_down[i + 1][1] + 50 == dia_down[i + 2][1] \
                    and dia_down[i + 2][1] + 50 == dia_down[i + 3][1] and dia_down[i + 3][1] + 50 == dia_down[i + 4][1]:

                if (dia_down[i + 4][0] + 50, dia_down[i + 4][1] + 50, dia_down[i + 4][2]+100, dia_down[i + 4][3]) in locked_pos_x and \
                        (dia_down[i][0]-50, dia_down[i][1] - 50, dia_down[i][2] - 100, dia_down[i][3]) in locked_pos_x:

                    return False

                return True

        return False


    def main(circle, cross):

        turn_circle = True
        run = True
        locked_pos_cir = []
        locked_pos_cro = []
        grid = create_grid()
        draw_grid(win, grid)
        pygame.display.update()
        cross_pos = 10

        while run:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    run = False
                    pygame.display.quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x = (pygame.mouse.get_pos()[0] // block_size) * block_size  # round down the value of mouse pos to get the top left of the square
                    y = (pygame.mouse.get_pos()[1] // block_size) * block_size
                    z_up = x + y
                    z_down = x - y

                    if turn_circle:

                        if (x, y, z_up, z_down) not in locked_pos_cro and (x, y, z_up, z_down) not in locked_pos_cir:

                            pygame.draw.circle(win, circle.color, (x + (block_size/2), y + (block_size/2)), block_size/2.5, 5)
                            pygame.display.update()
                            turn_circle = False
                            if len(locked_pos_cir) >= 4:
                                if check_win(locked_pos_cir, x, y, z_up, z_down, locked_pos_cro):
                                    run = False
                                    circle.score += 1
                                    time.sleep(0.5)
                                    win.fill((255, 255, 255))
                                    draw_text_middle(win, "Circle has won !!!", 20, (255, 0, 0), (s_width / 2 - 80, s_height / 2 - 30))
                                    draw_text_middle(win, "Circle scores: " + str(circle.score), 20, (255, 0, 0), (s_width / 2 - 80, s_height / 2))
                                    draw_text_middle(win, "Cross scores: " + str(cross.score), 20, (255, 0, 0), (s_width / 2 - 80, s_height / 2 + 30))
                                    pygame.display.update()
                                    time.sleep(3)
                                    win.fill((255, 255, 255))
                                    pygame.display.update()

                            locked_pos_cir.append((x, y, z_up, z_down))

                    else:

                        if (x, y, z_up, z_down) not in locked_pos_cir and (x, y, z_up, z_down) not in locked_pos_cro:
                            pygame.draw.line(win, cross.color, (x + cross_pos, y + cross_pos), (x + block_size - cross_pos, y + block_size - cross_pos), 5)
                            pygame.draw.line(win, cross.color, (x + block_size - cross_pos, y + cross_pos), (x + cross_pos, y + block_size - cross_pos), 5)
                            pygame.display.update()
                            turn_circle = True

                            if len(locked_pos_cro) >= 4:
                                if check_win(locked_pos_cro, x, y, z_up, z_down, locked_pos_cir):
                                    run = False
                                    cross.score += 1
                                    time.sleep(0.5)
                                    win.fill((255, 255, 255))
                                    draw_text_middle(win, "Cross has won !!!", 20, (255, 0, 0), (s_width / 2 - 80, s_height / 2 - 30))
                                    draw_text_middle(win, "Circle scores: " + str(circle.score), 20, (255, 0, 0), (s_width / 2 - 80, s_height / 2))
                                    draw_text_middle(win, "Cross scores: " + str(cross.score), 20, (255, 0, 0), (s_width / 2 - 80, s_height / 2 + 30))
                                    pygame.display.update()
                                    time.sleep(3)
                                    win.fill((255, 255, 255))
                                    pygame.display.update()

                            locked_pos_cro.append((x, y, z_up, z_down))
                # check for draw:
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_r) or (event.type == pygame.MOUSEBUTTONDOWN and len(locked_pos_cir) + len(locked_pos_cro) >= available_spaces):
                    run = False
                    cross.score += 1
                    circle.score += 1
                    time.sleep(0.5)
                    win.fill((255, 255, 255))
                    draw_text_middle(win, "This round is a draw!!!", 20, (255, 0, 0), (s_width / 2 - 80, s_height / 2 - 30))
                    draw_text_middle(win, "Circle scores: " + str(circle.score), 20, (255, 0, 0), (s_width / 2 - 80, s_height / 2))
                    draw_text_middle(win, "Cross scores: " + str(cross.score), 20, (255, 0, 0), (s_width / 2 - 80, s_height / 2 + 30))
                    pygame.display.update()
                    time.sleep(3)
                    win.fill((255, 255, 255))
                    pygame.display.update()

    def main_menu():
        circle = Player((0, 0, 0))
        cross = Player((255, 0, 0))
        run = True
        win.fill((0, 0, 0))
        draw_text_middle(win, "Press any button", 20, (255, 255, 255), (s_width / 2 - 80, s_height / 2 - 30))
        draw_text_middle(win, "(You can press r and declare any round draw if both got stuck)", 15, (255, 255, 255), (s_width / 2 - 230, s_height / 2))
        pygame.display.update()
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    main(circle, cross)
                    draw_text_middle(win, "Press any button to play again", 20, (0, 0, 0), (s_width / 2 - 145, s_height / 2 - 30))
                    draw_text_middle(win, "(You can press r and declare any round draw if both got stuck)", 15, (0, 0, 0), (s_width / 2 - 230, s_height / 2))
                    pygame.display.update()

        pygame.display.quit()

    main_menu()  # run the program
#-------------------------------Caro 3x3 Game---------------------------------
def caro3x3():
    global ActivePlayer, p1, p2, mov
    ActivePlayer = 1
    p1 = []
    p2 = []
    mov = 0

    def SetLayout(id,player_symbol):
        if id==1:
            b1.config(text= player_symbol)
            b1.state(['disabled'])
        elif id==2:
            b2.config(text= player_symbol)
            b2.state(['disabled'])
        elif id==3:
            b3.config(text= player_symbol)
            b3.state(['disabled'])
        elif id==4:
            b4.config(text= player_symbol)
            b4.state(['disabled'])
        elif id==5:
            b5.config(text= player_symbol)
            b5.state(['disabled'])
        elif id==6:
            b6.config(text= player_symbol)
            b6.state(['disabled'])
        elif id==7:
            b7.config(text= player_symbol)
            b7.state(['disabled'])
        elif id==8:
            b8.config(text= player_symbol)
            b8.state(['disabled'])
        elif id==9:
            b9.config(text= player_symbol)
            b9.state(['disabled'])

    def CheckWinner():
        global mov 
        winner = -1

        if(1 in p1) and (2 in p1) and (3 in p1):
            winner = 1
        if(1 in p2) and (2 in p2) and (3 in p2):
            winner = 2

        if(4 in p1) and (5 in p1) and (6 in p1):
            winner = 1
        if(4 in p2) and (5 in p2) and (6 in p2):
            winner = 2

        if(7 in p1) and (8 in p1) and (9 in p1):
            winner = 1
        if(7 in p2) and (8 in p2) and (9 in p2):
            winner = 2

        if(1 in p1) and (4 in p1) and (7 in p1):
            winner = 1
        if(1 in p2) and (4 in p2) and (7 in p2):
            winner = 2

        if(2 in p1) and (5 in p1) and (8 in p1):
            winner = 1
        if(2 in p2) and (5 in p2) and (8 in p2):
            winner = 2

        if(3 in p1) and (6 in p1) and ( 9 in p1):
            winner = 1
        if(3 in p2) and (6 in p2) and (9 in p2):
            winner = 2

        if(1 in p1) and (5 in p1) and ( 9 in p1):
            winner = 1
        if(1 in p2) and (5 in p2) and (9 in p2):
            winner = 2

        if(3 in p1) and (5 in p1) and ( 7 in p1):
            winner = 1
        if(3 in p2) and (5 in p2) and (7 in p2):
            winner = 2

        if winner ==1:
            messagebox.showinfo(title="Congratulations.", 
                message="Player 1 is the winner")
            caro3x3menu()
        elif winner ==2:
            messagebox.showinfo(title="Congratulations.", 
                message="Player 2 is the winner")
            caro3x3menu()
        elif mov ==9:
            messagebox.showinfo(title="Draw", 
                message="It's a Draw!!")
            caro3x3menu()

    def ButtonClick(id):
        global ActivePlayer
        global p1,p2
        global mov

        if(ActivePlayer ==1):
            SetLayout(id,"X")
            p1.append(id)
            mov +=1
            root.title("Tic Tac Toe : Player 2")
            ActivePlayer =2

        elif(ActivePlayer==2):
            SetLayout(id,"O")
            p2.append(id)
            mov +=1
            root.title("Tic Tac Toe : Player 1")
            ActivePlayer =1
        CheckWinner()

    def AutoPlay():
        global p1; global p2
        Empty = []
        for cell in range(9):
            if(not((cell +1 in p1) or (cell +1 in p2))):
                Empty.append(cell+1)
        try:
            RandIndex = randint(0,len(Empty) -1)
            ButtonClick(Empty[RandIndex])
        except:
            pass

    def EnableAll():
        b1.config(text= " ")
        b1.state(['!disabled'])
        b2.config(text= " ")
        b2.state(['!disabled'])
        b3.config(text= " ")
        b3.state(['!disabled'])
        b4.config(text= " ")
        b4.state(['!disabled'])
        b5.config(text= " ")
        b5.state(['!disabled'])
        b6.config(text= " ")
        b6.state(['!disabled'])
        b7.config(text= " ")
        b7.state(['!disabled'])
        b8.config(text= " ")
        b8.state(['!disabled'])
        b9.config(text= " ")
        b9.state(['!disabled'])

    root = Tk()
    root.title("Tic Tac toe : Player 1")
    st = ttk.Style()
    st.configure("my.TButton", font=('Chiller',24,'bold'))

    b1 = ttk.Button(root, text=" ", style="my.TButton")
    b1.grid(row=1, column=0, sticky="nwse", ipadx=50,ipady=50)
    b1.config(command = lambda : ButtonClick(1))


    b2 = ttk.Button(root, text=" ",style ="my.TButton")
    b2.grid(row=1, column=1, sticky="snew", ipadx=50, ipady=50)
    b2.config(command = lambda : ButtonClick(2))

    b3= ttk.Button(root, text=" ",style="my.TButton")
    b3.grid(row=1, column=2, sticky="snew", ipadx=50,
            ipady=50)
    b3.config(command = lambda : ButtonClick(3))

    b4 = ttk.Button(root, text=" ",style="my.TButton")
    b4.grid(row=2, column=0, sticky="snew", ipadx=50,
            ipady=50)
    b4.config(command = lambda : ButtonClick(4))

    b5 = ttk.Button(root, text=" ",style="my.TButton")
    b5.grid(row=2, column=1, sticky="snew", ipadx=50,
            ipady=50)
    b5.config(command = lambda : ButtonClick(5))

    b6 = ttk.Button(root, text=" ",style="my.TButton")
    b6.grid(row=2, column=2, sticky="snew", ipadx=50,
            ipady=50)
    b6.config(command = lambda : ButtonClick(6))

    b7 = ttk.Button(root, text=" ",style="my.TButton")
    b7.grid(row=3, column=0, sticky="snew", ipadx=50,
            ipady=50)
    b7.config(command = lambda : ButtonClick(7))

    b8 = ttk.Button(root, text=" ",style="my.TButton")
    b8.grid(row=3, column=1, sticky="snew", ipadx=50,
            ipady=50)
    b8.config(command = lambda : ButtonClick(8))

    b9 = ttk.Button(root, text=" ",style="my.TButton")
    b9.grid(row=3, column=2, sticky="snew", ipadx=50,
            ipady=50)
    b9.config(command = lambda : ButtonClick(9))

    root.resizable(0,0)
    root.mainloop()
#-------------------------------Novel-----------------------------------------   
def novelmenu():
    window.title('Menu Novel')
    window.geometry("1140x700")
    window.configure(bg = "#FFFFFF")
    canvas = Canvas(
        window,
        bg = "#FFFFFF",
        height = 700,
        width = 1140,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge")
    canvas.place(x = 0, y = 0)

    background_img = PhotoImage(file = f"All Novel/Novel Menu/NMBackground.png")
    background = canvas.create_image(
        570.0, 350.0,
        image=background_img)

    img0 = PhotoImage(file = f"All Novel/Novel Menu/NM1.png")
    b0 = Button(
        image = img0,
        borderwidth = 0,
        highlightthickness = 0,
        command = novellist,
        relief = "flat")

    b0.place(
        x = 60, y = 132,
        width = 122,
        height = 173)

    img1 = PhotoImage(file = f"All Novel/Novel Menu/NM2.png")
    b1 = Button(
        image = img1,
        borderwidth = 0,
        highlightthickness = 0,
        command = btn_clicked,
        relief = "flat")

    b1.place(
        x = 209, y = 133,
        width = 122,
        height = 173)

    img2 = PhotoImage(file = f"All Novel/Novel Menu/NM3.png")
    b2 = Button(
        image = img2,
        borderwidth = 0,
        highlightthickness = 0,
        command = btn_clicked,
        relief = "flat")

    b2.place(
        x = 360, y = 133,
        width = 122,
        height = 173)

    img3 = PhotoImage(file = f"All Novel/Novel Menu/NM4.png")
    b3 = Button(
        image = img3,
        borderwidth = 0,
        highlightthickness = 0,
        command = btn_clicked,
        relief = "flat")

    b3.place(
        x = 510, y = 133,
        width = 122,
        height = 173)

    img4 = PhotoImage(file = f"All Novel/Novel Menu/NM5.png")
    b4 = Button(
        image = img4,
        borderwidth = 0,
        highlightthickness = 0,
        command = btn_clicked,
        relief = "flat")

    b4.place(
        x = 659, y = 133,
        width = 122,
        height = 173)

    img5 = PhotoImage(file = f"All Novel/Novel Menu/NM6.png")
    b5 = Button(
        image = img5,
        borderwidth = 0,
        highlightthickness = 0,
        command = btn_clicked,
        relief = "flat")

    b5.place(
        x = 808, y = 133,
        width = 122,
        height = 173)

    img6 = PhotoImage(file = f"All Novel/Novel Menu/NM7.png")
    b6 = Button(
        image = img6,
        borderwidth = 0,
        highlightthickness = 0,
        command = btn_clicked,
        relief = "flat")

    b6.place(
        x = 957, y = 134,
        width = 122,
        height = 173)

    img7 = PhotoImage(file = f"All Novel/Novel Menu/NM8.png")
    b7 = Button(
        image = img7,
        borderwidth = 0,
        highlightthickness = 0,
        command = btn_clicked,
        relief = "flat")

    b7.place(
        x = 60, y = 395,
        width = 122,
        height = 173)

    img8 = PhotoImage(file = f"All Novel/Novel Menu/NM9.png")
    b8 = Button(
        image = img8,
        borderwidth = 0,
        highlightthickness = 0,
        command = btn_clicked,
        relief = "flat")

    b8.place(
        x = 209, y = 395,
        width = 122,
        height = 173)

    img9 = PhotoImage(file = f"All Novel/Novel Menu/NM10.png")
    b9 = Button(
        image = img9,
        borderwidth = 0,
        highlightthickness = 0,
        command = btn_clicked,
        relief = "flat")

    b9.place(
        x = 358, y = 395,
        width = 122,
        height = 173)

    img10 = PhotoImage(file = f"All Novel/Novel Menu/NM11.png")
    b10 = Button(
        image = img10,
        borderwidth = 0,
        highlightthickness = 0,
        command = btn_clicked,
        relief = "flat")

    b10.place(
        x = 509, y = 395,
        width = 122,
        height = 173)

    img11 = PhotoImage(file = f"All Novel/Novel Menu/NM12.png")
    b11 = Button(
        image = img11,
        borderwidth = 0,
        highlightthickness = 0,
        command = btn_clicked,
        relief = "flat")

    b11.place(
        x = 659, y = 395,
        width = 122,
        height = 173)

    img12 = PhotoImage(file = f"All Novel/Novel Menu/NM13.png")
    b12 = Button(
        image = img12,
        borderwidth = 0,
        highlightthickness = 0,
        command = btn_clicked,
        relief = "flat")

    b12.place(
        x = 808, y = 395,
        width = 122,
        height = 173)

    img13 = PhotoImage(file = f"All Novel/Novel Menu/NM14.png")
    b13 = Button(
        image = img13,
        borderwidth = 0,
        highlightthickness = 0,
        command = btn_clicked,
        relief = "flat")

    b13.place(
        x = 957, y = 395,
        width = 122,
        height = 173)

    img14 = PhotoImage(file = f"All Novel/Novel Menu/NMBack.png")
    b14 = Button(
        image = img14,
        borderwidth = 0,
        highlightthickness = 0,
        command = truyen,
        relief = "flat")

    b14.place(
        x = 30, y = 32,
        width = 120,
        height = 69)

    window.resizable(False, False)
    window.mainloop()
def novellist():
    window.title('Novel List')
    window.geometry("1140x700")
    window.configure(bg = "#FFFFFF")
    canvas = Canvas(
        window,
        bg = "#FFFFFF",
        height = 700,
        width = 1140,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge")
    canvas.place(x = 0, y = 0)

    background_img = PhotoImage(file = f"All Novel/Novel List/NLBackground.png")
    background = canvas.create_image(
        513.5, 365.0,
        image=background_img)

    img0 = PhotoImage(file = f"All Novel/Novel List/NLBack.png")
    b0 = Button(
        image = img0,
        borderwidth = 0,
        highlightthickness = 0,
        command = novelmenu,
        relief = "flat")

    b0.place(
        x = 30, y = 32,
        width = 120,
        height = 69)

    img1 = PhotoImage(file = f"All Novel/Novel List/NL1.png")
    b1 = Button(
        image = img1,
        borderwidth = 0,
        highlightthickness = 0,
        command = novelread,
        relief = "flat")

    b1.place(
        x = 126, y = 498,
        width = 182,
        height = 55)

    img2 = PhotoImage(file = f"All Novel/Novel List/NL2.png")
    b2 = Button(
        image = img2,
        borderwidth = 0,
        highlightthickness = 0,
        command = btn_clicked,
        relief = "flat")

    b2.place(
        x = 341, y = 498,
        width = 182,
        height = 55)

    window.resizable(False, False)
    window.mainloop()
def novelread():
    window.title('Novel Read')
    window.geometry("1600x700")
    window.configure(bg = "#ffffff")
    canvas = Canvas(
        window,
        bg = "#ffffff",
        height = 700,
        width = 1600,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge")
    canvas.place(x = 0, y = 0)

    frame = tkinter.Frame(window, bd=2) # relief=SUNKEN)

    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    xscrollbar = tkinter.Scrollbar(frame, orient=tkinter.HORIZONTAL)
    xscrollbar.grid(row=1, column=0, sticky=tkinter.E+tkinter.W)

    yscrollbar = tkinter.Scrollbar(frame)
    yscrollbar.grid(row=0, column=1, sticky=tkinter.N+tkinter.S)

    canvas = tkinter.Canvas(frame, bd=0, width=1600, height=900, xscrollcommand=xscrollbar.set, yscrollcommand=yscrollbar.set)
    canvas.grid(row=0, column=0, sticky=tkinter.N+tkinter.S+tkinter.E+tkinter.W)
    canvas.config(scrollregion=canvas.bbox(tkinter.ALL))

    File = "All Novel/Novel Read/NR01.png"
    img = PIL.ImageTk.PhotoImage(PIL.Image.open(File))
    canvas.create_image(0,0,image=img, anchor="nw")
    canvas.config(scrollregion=canvas.bbox(tkinter.ALL))

    img0 = PhotoImage(file = f"All Novel/Novel Read/NRBack.png")
    b0 = Button(
        image = img0,
        borderwidth = 0,
        highlightthickness = 0,
        command = novellist,
        relief = "flat")

    b0.place(
        x = 20, y = 25,
        width = 120,
        height = 69) 

    xscrollbar.config(command=canvas.xview)
    yscrollbar.config(command=canvas.yview)

    frame.pack()
    window.mainloop()
#-------------------------------Manga-----------------------------------------   
def mangamenu():
    window.title('Menu Manga')
    window.geometry("1140x700")
    window.configure(bg = "#FFFFFF")
    canvas = Canvas(
        window,
        bg = "#FFFFFF",
        height = 700,
        width = 1140,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge")
    canvas.place(x = 0, y = 0)

    background_img = PhotoImage(file = f"All Manga/Manga Menu/MMBackground.png")
    background = canvas.create_image(
        570.0, 350.0,
        image=background_img)

    img0 = PhotoImage(file = f"All Manga/Manga Menu/MM1.png")
    b0 = Button(
        image = img0,
        borderwidth = 0,
        highlightthickness = 0,
        command = mangalist,
        relief = "flat")

    b0.place(
        x = 60, y = 133,
        width = 122,
        height = 173)

    img1 = PhotoImage(file = f"All Manga/Manga Menu/MM2.png")
    b1 = Button(
        image = img1,
        borderwidth = 0,
        highlightthickness = 0,
        command = btn_clicked,
        relief = "flat")

    b1.place(
        x = 209, y = 133,
        width = 122,
        height = 173)

    img2 = PhotoImage(file = f"All Manga/Manga Menu/MM3.png")
    b2 = Button(
        image = img2,
        borderwidth = 0,
        highlightthickness = 0,
        command = btn_clicked,
        relief = "flat")

    b2.place(
        x = 360, y = 133,
        width = 122,
        height = 173)

    img3 = PhotoImage(file = f"All Manga/Manga Menu/MM4.png")
    b3 = Button(
        image = img3,
        borderwidth = 0,
        highlightthickness = 0,
        command = btn_clicked,
        relief = "flat")

    b3.place(
        x = 510, y = 133,
        width = 122,
        height = 173)

    img4 = PhotoImage(file = f"All Manga/Manga Menu/MM5.png")
    b4 = Button(
        image = img4,
        borderwidth = 0,
        highlightthickness = 0,
        command = btn_clicked,
        relief = "flat")

    b4.place(
        x = 659, y = 133,
        width = 122,
        height = 173)

    img5 = PhotoImage(file = f"All Manga/Manga Menu/MM6.png")
    b5 = Button(
        image = img5,
        borderwidth = 0,
        highlightthickness = 0,
        command = btn_clicked,
        relief = "flat")

    b5.place(
        x = 808, y = 133,
        width = 122,
        height = 173)

    img6 = PhotoImage(file = f"All Manga/Manga Menu/MM7.png")
    b6 = Button(
        image = img6,
        borderwidth = 0,
        highlightthickness = 0,
        command = btn_clicked,
        relief = "flat")

    b6.place(
        x = 957, y = 134,
        width = 122,
        height = 173)

    img7 = PhotoImage(file = f"All Manga/Manga Menu/MM8.png")
    b7 = Button(
        image = img7,
        borderwidth = 0,
        highlightthickness = 0,
        command = btn_clicked,
        relief = "flat")

    b7.place(
        x = 60, y = 395,
        width = 122,
        height = 173)

    img8 = PhotoImage(file = f"All Manga/Manga Menu/MM9.png")
    b8 = Button(
        image = img8,
        borderwidth = 0,
        highlightthickness = 0,
        command = btn_clicked,
        relief = "flat")

    b8.place(
        x = 209, y = 395,
        width = 122,
        height = 173)

    img9 = PhotoImage(file = f"All Manga/Manga Menu/MM10.png")
    b9 = Button(
        image = img9,
        borderwidth = 0,
        highlightthickness = 0,
        command = btn_clicked,
        relief = "flat")

    b9.place(
        x = 358, y = 395,
        width = 122,
        height = 173)

    img10 = PhotoImage(file = f"All Manga/Manga Menu/MM11.png")
    b10 = Button(
        image = img10,
        borderwidth = 0,
        highlightthickness = 0,
        command = btn_clicked,
        relief = "flat")

    b10.place(
        x = 509, y = 395,
        width = 122,
        height = 173)

    img11 = PhotoImage(file = f"All Manga/Manga Menu/MM12.png")
    b11 = Button(
        image = img11,
        borderwidth = 0,
        highlightthickness = 0,
        command = btn_clicked,
        relief = "flat")

    b11.place(
        x = 659, y = 395,
        width = 122,
        height = 173)

    img12 = PhotoImage(file = f"All Manga/Manga Menu/MM13.png")
    b12 = Button(
        image = img12,
        borderwidth = 0,
        highlightthickness = 0,
        command = btn_clicked,
        relief = "flat")

    b12.place(
        x = 808, y = 395,
        width = 122,
        height = 173)

    img13 = PhotoImage(file = f"All Manga/Manga Menu/MM14.png")
    b13 = Button(
        image = img13,
        borderwidth = 0,
        highlightthickness = 0,
        command = btn_clicked,
        relief = "flat")

    b13.place(
        x = 957, y = 395,
        width = 122,
        height = 173)

    img14 = PhotoImage(file = f"All Manga/Manga Menu/MMBack.png")
    b14 = Button(
        image = img14,
        borderwidth = 0,
        highlightthickness = 0,
        command = truyen,
        relief = "flat")

    b14.place(
        x = 30, y = 32,
        width = 120,
        height = 69)

    window.resizable(False, False)
    window.mainloop()
def mangalist():
    window.title('Manga List')
    window.geometry("1140x700")
    window.configure(bg = "#FFFFFF")
    canvas = Canvas(
        window,
        bg = "#FFFFFF",
        height = 700,
        width = 1140,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge")
    canvas.place(x = 0, y = 0)

    background_img = PhotoImage(file = f"All Manga/Manga List/MLBackground.png")
    background = canvas.create_image(
        513.5, 365.0,
        image=background_img)

    img0 = PhotoImage(file = f"All Manga/Manga List/MLBack.png")
    b0 = Button(
        image = img0,
        borderwidth = 0,
        highlightthickness = 0,
        command = mangamenu,
        relief = "flat")

    b0.place(
        x = 30, y = 32,
        width = 120,
        height = 69)

    img1 = PhotoImage(file = f"All Manga/Manga List/ML1.png")
    b1 = Button(
        image = img1,
        borderwidth = 0,
        highlightthickness = 0,
        command = mangaread,
        relief = "flat")

    b1.place(
        x = 126, y = 498,
        width = 182,
        height = 55)

    img2 = PhotoImage(file = f"All Manga/Manga List/ML2.png")
    b2 = Button(
        image = img2,
        borderwidth = 0,
        highlightthickness = 0,
        command = btn_clicked,
        relief = "flat")

    b2.place(
        x = 126, y = 574,
        width = 182,
        height = 55)

    img3 = PhotoImage(file = f"All Manga/Manga List/ML3.png")
    b3 = Button(
        image = img3,
        borderwidth = 0,
        highlightthickness = 0,
        command = btn_clicked,
        relief = "flat")

    b3.place(
        x = 341, y = 498,
        width = 182,
        height = 55)

    img4 = PhotoImage(file = f"All Manga/Manga List/ML4.png")
    b4 = Button(
        image = img4,
        borderwidth = 0,
        highlightthickness = 0,
        command = btn_clicked,
        relief = "flat")

    b4.place(
        x = 341, y = 574,
        width = 182,
        height = 55)

    img5 = PhotoImage(file = f"All Manga/Manga List/ML5.png")
    b5 = Button(
        image = img5,
        borderwidth = 0,
        highlightthickness = 0,
        command = btn_clicked,
        relief = "flat")

    b5.place(
        x = 556, y = 498,
        width = 182,
        height = 55)

    img6 = PhotoImage(file = f"All Manga/Manga List/ML6.png")
    b6 = Button(
        image = img6,
        borderwidth = 0,
        highlightthickness = 0,
        command = btn_clicked,
        relief = "flat")

    b6.place(
        x = 556, y = 574,
        width = 182,
        height = 55)

    window.resizable(False, False)
    window.mainloop()
def mangaread():
    window.title('Manga Read')
    window.geometry("860x700")
    window.configure(bg = "#ffffff")
    canvas = Canvas(
        window,
        bg = "#ffffff",
        height = 700,
        width = 860,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge")
    canvas.place(x = 0, y = 0)

    frame = tkinter.Frame(window, bd=2) # relief=SUNKEN)

    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    xscrollbar = tkinter.Scrollbar(frame, orient=tkinter.HORIZONTAL)
    xscrollbar.grid(row=1, column=0, sticky=tkinter.E+tkinter.W)

    yscrollbar = tkinter.Scrollbar(frame)
    yscrollbar.grid(row=0, column=1, sticky=tkinter.N+tkinter.S)

    canvas = tkinter.Canvas(frame, bd=0, width=1140, height=900, xscrollcommand=xscrollbar.set, yscrollcommand=yscrollbar.set)
    canvas.grid(row=0, column=0, sticky=tkinter.N+tkinter.S+tkinter.E+tkinter.W)
    canvas.config(scrollregion=canvas.bbox(tkinter.ALL))

    File = "All Manga/Manga Read/MR1.png"
    img = PIL.ImageTk.PhotoImage(PIL.Image.open(File))
    canvas.create_image(0,0,image=img, anchor="nw")
    canvas.config(scrollregion=canvas.bbox(tkinter.ALL))

    img0 = PhotoImage(file = f"All Manga/Manga Read/MRBack.png")
    b0 = Button(
        image = img0,
        borderwidth = 0,
        highlightthickness = 0,
        command = mangalist,
        relief = "flat")

    b0.place(
        x = 720, y = 25,
        width = 120,
        height = 69) 

    xscrollbar.config(command=canvas.xview)
    yscrollbar.config(command=canvas.yview)

    frame.pack()
    window.mainloop()
#-------------------------------Music-----------------------------------------   
def music():
    # --------------Add Video--------------------------------
    def add_videos():
    # Giving path fo the music folder
        videos = filedialog.askopenfilenames(initialdir="E:/DoAn/MainProject/Music/Music List", title="Choose Videos", filetypes=(("mp4 Files", "*.mp4"),))

        #for loop to insert songs in the queue
        for video in videos:
            video = video.replace("E:/DoAn/MainProject/Music/Music List/", "")
            video = video.replace(".mp4", "")
            #Insert into playlist
            entry0.insert(END, video)
    # --------------Play Video-------------------------------
    def play_videos():
        new_video = entry0.get(ANCHOR)  #geeting the clicked song from the playlist
        new_video = f'E:/DoAn/MainProject/Music/Music List/{new_video}.mp4'  #definig the path for the song
        os.startfile(new_video)
    # --------------Delete Video-----------------------------
    def delete_videos():
        entry0.delete(ANCHOR)
    # --------------Search and Download Video----------------
    def sad():
        keyword = stringSAD.get()
        keywords = keyword.replace(" ","+")
        html = urllib.request.urlopen("https://www.youtube.com/results?search_query="+keywords)
        video_ids = re.findall(r"watch\?v=(\S{11})",html.read().decode())
        a = "https://www.youtube.com/watch?v="+video_ids[0]
        url = a
        pytube.YouTube(url).streams.get_highest_resolution().download("Music/Music List/")
    # --------------Add Song---------------------------------
    def add_songs():
        # Giving path fo the music folder
        songs = filedialog.askopenfilenames(initialdir="Music/Music List", title="Choose Songs", filetypes=(("mp3 Files", "*.mp3"),))

        #for loop to insert songs in the queue
        for song in songs:
            song = song.replace("E:/DoAn/MainProject/Music/Music List/", "")
            song = song.replace(".mp3", "")
            #Insert into playlist
            entry1.insert(END, song)
    # ----------Create Global Play Flag Variable-------------
    global playFlag, firstTimePlay
    playFlag = False
    firstTimePlay = True
    #---------------PLAY Song--------------------------------
    def play():
        global playFlag, firstTimePlay  #definig two global variabeles 'playFlag' and 'firstTimePlay'
        
        if firstTimePlay == True:
            # to play a song for first time
            new_song = entry1.get(ACTIVE)  #geeting the current/active song from the playlist
            new_song = f'Music/Music List/{new_song}.mp3'  #definig the path for the song 
            pygame.mixer.music.load(new_song)  #playing the active/current song
            pygame.mixer.music.play(loops=0)   # not keeping the song in loop
            var.set(entry1.get(tkinter.ACTIVE))  #setting the 'var' to display the title of the cureent song on top
            play_pause_btn.configure(image=pause_btn_img)  #showing the the pause icon
            firstTimePlay = False 
            playFlag = True
        
        else:
            if playFlag == True:
                # we have to Pause
                pygame.mixer.music.pause()
                play_pause_btn.configure(image=play_btn_img)
                playFlag = False
            else:
                # we have to Unpause i.e. play
                pygame.mixer.music.unpause()
                play_pause_btn.configure(image=pause_btn_img)
                playFlag = True
    #---------------STOP Song--------------------------------
    def stop():
        pygame.mixer.music.stop()
        play_pause_btn.configure(image=play_btn_img)
        entry1.selection_clear(ACTIVE)
    #---------------PLAY Song--------------------------------
    def next_song():

        next_one = entry1.curselection() # Get the current song tuple number
        next_one = next_one[0]+1 # Add one to the current song number
        song = entry1.get(next_one) # Grab song title from playlist
        song = f'Music/Music List/{song}.mp3' #add directory structure and mp3 to song title
        pygame.mixer.music.load(song)  #load and play song
        pygame.mixer.music.play(loops=0)   # not keeping the song in loop
        entry1.selection_clear(0, END)  # Clear active bar in playlist box
        entry1.activate(next_one) #Activate new song bar
        entry1.selection_set(next_one, last=None) # Set Activate bar to next song
        var.set(entry1.get(tkinter.ACTIVE))  #setting the 'var' to display the title of the cureent song on top
    #---------------PLAY Song--------------------------------
    def previous_song():
    
        previous_one = entry1.curselection()  # Get the current song tuple number  
        previous_one = previous_one[0] - 1  # Add one to the current song number
        song = entry1.get(previous_one)  # Grab song title from playlist
        song = f'Music/Music List/{song}.mp3'   # add directory structure and mp3 to song title
        pygame.mixer.music.load(song)  # load and play song
        pygame.mixer.music.play(loops=0)   # not keeping the song in loop
        entry1.selection_clear(0, END)  # Clear active bar in playlist box
        entry1.activate(previous_one) # Activate new song bar    
        entry1.selection_set(previous_one, last=None) # Set Activate bar to next song
        var.set(entry1.get(tkinter.ACTIVE))
    #---------------DELETE Song------------------------------
    def delete_song():
        entry1.delete(ANCHOR)  #delete the current/active song
        pygame.mixer.music.stop()  #stop the curent played song
    # --------------PLAY SELECTED SONG-----------------------
    def playClickedSong(event):
        global playFlag, firstTimePlay  #definig two global variabeles 'playFlag' and 'firstTimePlay'
        firstTimePlay = True
        playFlag = False

        if firstTimePlay == True:
            # to play a song for first time
            new_song = entry1.get(ANCHOR)  #geeting the clicked song from the playlist
            new_song = f'Music/Music List/{new_song}.mp3'  #definig the path for the song
            pygame.mixer.music.load(new_song)  #playing the active/current song
            pygame.mixer.music.play(loops=0)   # not keeping the song in loop
            var.set(entry1.get(tkinter.ANCHOR))  #setting the 'var' to display the title of the cureent song on top
            play_pause_btn.configure(image=pause_btn_img)  #showing the the pause icon
            firstTimePlay = False 
            playFlag = True

    global stringSAD
    stringSAD = StringVar()
    pygame.mixer.init()  # Initializing PyGame mixer

    window.title('Music')
    window.geometry("1140x700")
    window.configure(bg = "#ffffff")
    canvas = Canvas(
        window,
        bg = "#ffffff",
        height = 700,
        width = 1140,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge")
    canvas.place(x = 0, y = 0)

    background_img = PhotoImage(file = f"Music/Music Menu/MusicBackground.png")
    background = canvas.create_image(
        570.0, 350.0,
        image=background_img)

    img0 = PhotoImage(file = f"Music/Music Menu/MusicDeleteSong.png")
    b0 = Button(
        image = img0,
        borderwidth = 0,
        highlightthickness = 0,
        command = delete_song,
        relief = "flat")

    b0.place(
        x = 131, y = 611,
        width = 125,
        height = 65)

    img1 = PhotoImage(file = f"Music/Music Menu/MusicAddSong.png")
    b1 = Button(
        image = img1,
        borderwidth = 0,
        highlightthickness = 0,
        command = add_songs,
        relief = "flat")

    b1.place(
        x = 333, y = 611,
        width = 125,
        height = 65)

    img2 = PhotoImage(file = f"Music/Music Menu/MusicDown.png")
    b2 = Button(
        image = img2,
        borderwidth = 0,
        highlightthickness = 0,
        command = sad,
        relief = "flat")

    b2.place(
        x = 835, y = 142,
        width = 125,
        height = 65)

    img3 = PhotoImage(file = f"Music/Music Menu/MusicDeleteVideo.png")
    b3 = Button(
        image = img3,
        borderwidth = 0,
        highlightthickness = 0,
        command = delete_videos,
        relief = "flat")

    b3.place(
        x = 627, y = 611,
        width = 125,
        height = 65)

    img4 = PhotoImage(file = f"Music/Music Menu/MusicPlayVideo.png")
    b4 = Button(
        image = img4,
        borderwidth = 0,
        highlightthickness = 0,
        command = play_videos,
        relief = "flat")

    b4.place(
        x = 917, y = 611,
        width = 125,
        height = 65)

    img5 = PhotoImage(file = f"Music/Music Menu/MusicBack.png")
    b5 = Button(
        image = img5,
        borderwidth = 0,
        highlightthickness = 0,
        command = menu,
        relief = "flat")

    b5.place(
        x = 30, y = 32,
        width = 120,
        height = 70)

    img6 = PhotoImage(file = f"Music/Music Menu/MusicAddVideo.png")
    b6 = Button(
        image = img6,
        borderwidth = 0,
        highlightthickness = 0,
        command = add_videos,
        relief = "flat")

    b6.place(
        x = 772, y = 611,
        width = 125,
        height = 65)

    entry0_img = PhotoImage(file = f"Music/Music Menu/ListVideo.png")
    entry0_bg = canvas.create_image(
        845.5, 422.5,
        image = entry0_img)

    entry0 = Listbox(
        bd = 0,
        bg = "#c4c4c4",
        highlightthickness = 0)

    entry0.place(
        x = 590, y = 250,
        width = 511,
        height = 343)

    entry1_img = PhotoImage(file = f"Music/Music Menu/ListSong.png")
    entry1_bg = canvas.create_image(
        294.5, 396.0,
        image = entry1_img)

    entry1 = Listbox(
        bd = 0,
        bg = "#c4c4c4",
        highlightthickness = 0)
    entry1.bind('<<ListboxSelect>>', playClickedSong) #when a song is selected on the playlist then go to 'playClickedSong' function
    entry1.pack(pady=1)  #giving padding on y-axis = 1

    entry1.place(
        x = 39, y = 250,
        width = 511,
        height = 290)

    entry2_img = PhotoImage(file = f"Music/Music Menu/MusicSearch.png")
    entry2_bg = canvas.create_image(
        569.5, 174.0,
        image = entry2_img)

    entry2 = Entry(
        bd = 0,
        bg = "#c4c4c4",
        highlightthickness = 0,
        textvariable=stringSAD)

    entry2.place(
        x = 345.0, y = 143,
        width = 449.0,
        height = 60)

    back_btn_img = PhotoImage(file="Music/Music Button/back.png")
    forward_btn_img= PhotoImage(file="Music/Music Button/next.png")
    play_btn_img = PhotoImage(file="Music/Music Button/play.png")
    pause_btn_img = PhotoImage(file="Music/Music Button/pause.png")
    stop_btn_img = PhotoImage(file="Music/Music Button/stop.png")

    back_btn = Button(image = back_btn_img, borderwidth=0, command=previous_song, bg="#fffafa", activebackground="#fffafa")
    back_btn.place(x = 183.0, y = 542,width = 46.0,height = 46)

    forward_btn = Button(image=forward_btn_img, borderwidth=0, command=next_song, bg="#fffafa", activebackground="#fffafa")
    forward_btn.place(x = 360.0, y = 542,width = 46.0,height = 46)

    play_pause_btn = Button(image=play_btn_img, borderwidth=0, command=play, bg="#fffafa", activebackground="#fffafa")
    play_pause_btn.place(x = 242.0, y = 542,width = 46.0,height = 46)

    stop_btn = Button(image=stop_btn_img, borderwidth=0, command=stop, bg="#fffafa", activebackground="#fffafa")
    stop_btn.place(x = 301.0, y = 542,width = 46.0,height = 46)

    var = tkinter.StringVar() 
    song_title = tkinter.Label(window, font=("calibri 20 underline"), fg = "black", textvariable = var, bg ="white")
    song_title.pack()

    window.resizable(False, False)
    window.mainloop()
#-------------------------------Start Movie-----------------------------------   
def startmovie():
    iron_man = f'E:/DoAn/MainProject/Movie List/Iron Man.mp4'
    os.startfile(iron_man)
#-------------------------------Movie-----------------------------------------
def movie():
    window.title('Menu Movie')
    window.geometry("1140x700")
    window.configure(bg = "#ffffff")
    canvas = Canvas(
        window,
        bg = "#ffffff",
        height = 700,
        width = 1140,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge")
    canvas.place(x = 0, y = 0)

    background_img = PhotoImage(file = f"Movie/MovieBackground.png")
    background = canvas.create_image(
        570.0, 350.0,
        image=background_img)

    img0 = PhotoImage(file = f"Movie/MovieBack.png")
    b0 = Button(
        image = img0,
        borderwidth = 0,
        highlightthickness = 0,
        command = menu,
        relief = "flat")

    b0.place(
        x = 30, y = 32,
        width = 120,
        height = 70)

    img1 = PhotoImage(file = f"Movie/IronMan.png")
    b1 = Button(
        image = img1,
        borderwidth = 0,
        highlightthickness = 0,
        command = startmovie,
        relief = "flat")

    b1.place(
        x = 60, y = 132,
        width = 122,
        height = 173)

    img2 = PhotoImage(file = f"Movie/Cap.png")
    b2 = Button(
        image = img2,
        borderwidth = 0,
        highlightthickness = 0,
        command = btn_clicked,
        relief = "flat")

    b2.place(
        x = 209, y = 132,
        width = 122,
        height = 173)

    img3 = PhotoImage(file = f"Movie/Thor.png")
    b3 = Button(
        image = img3,
        borderwidth = 0,
        highlightthickness = 0,
        command = btn_clicked,
        relief = "flat")

    b3.place(
        x = 358, y = 132,
        width = 122,
        height = 173)

    img4 = PhotoImage(file = f"Movie/Hulk.png")
    b4 = Button(
        image = img4,
        borderwidth = 0,
        highlightthickness = 0,
        command = btn_clicked,
        relief = "flat")

    b4.place(
        x = 507, y = 132,
        width = 122,
        height = 173)

    img5 = PhotoImage(file = f"Movie/BlackWidow.png")
    b5 = Button(
        image = img5,
        borderwidth = 0,
        highlightthickness = 0,
        command = btn_clicked,
        relief = "flat")

    b5.place(
        x = 656, y = 132,
        width = 122,
        height = 173)

    img6 = PhotoImage(file = f"Movie/Hawkeye.png")
    b6 = Button(
        image = img6,
        borderwidth = 0,
        highlightthickness = 0,
        command = btn_clicked,
        relief = "flat")

    b6.place(
        x = 805, y = 132,
        width = 122,
        height = 173)

    window.resizable(False, False)
    window.mainloop()
#-------------------------------Truyen----------------------------------------
def truyen():
    window.title('Menu Book')
    window.geometry("1140x700")
    window.configure(bg = "#ffffff")
    canvas = Canvas(
        window,
        bg = "#ffffff",
        height = 700,
        width = 1140,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge")
    canvas.place(x = 0, y = 0)

    background_img = PhotoImage(file = f"Truyen/TruyenBackground.png")
    background = canvas.create_image(
        570.0, 350.0,
        image=background_img)

    img0 = PhotoImage(file = f"Truyen/TruyenManga.png")
    b0 = Button(
        image = img0,
        borderwidth = 0,
        highlightthickness = 0,
        command = mangamenu,
        relief = "flat")

    b0.place(
        x = 88, y = 378,
        width = 435,
        height = 180)

    img1 = PhotoImage(file = f"Truyen/TruyenNovel.png")
    b1 = Button(
        image = img1,
        borderwidth = 0,
        highlightthickness = 0,
        command = novelmenu,
        relief = "flat")

    b1.place(
        x = 616, y = 378,
        width = 435,
        height = 180)

    img2 = PhotoImage(file = f"Truyen/TruyenBack.png")
    b2 = Button(
        image = img2,
        borderwidth = 0,
        highlightthickness = 0,
        command = menu,
        relief = "flat")

    b2.place(
        x = 30, y = 32,
        width = 120,
        height = 70)

    window.resizable(False, False)
    window.mainloop()
#-------------------------------FB Hard Menu----------------------------------
def fbharmenu():
    window.geometry("1140x700")
    window.configure(bg = "#ffffff")
    canvas = Canvas(
        window,
        bg = "#ffffff",
        height = 700,
        width = 1140,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge")
    canvas.place(x = 0, y = 0)

    background_img = PhotoImage(file = f"All Game/Flappy Bird/HardMenu/HardBackground.png")
    background = canvas.create_image(
        570.0, 350.0,
        image=background_img)

    img0 = PhotoImage(file = f"All Game/Flappy Bird/HardMenu/HardExit.png")
    b0 = Button(
        image = img0,
        borderwidth = 0,
        highlightthickness = 0,
        command = fbird,
        relief = "flat")

    b0.place(
        x = 294, y = 475,
        width = 543,
        height = 107)

    img1 = PhotoImage(file = f"All Game/Flappy Bird/HardMenu/HardPlay.png")
    b1 = Button(
        image = img1,
        borderwidth = 0,
        highlightthickness = 0,
        command = fbhard,
        relief = "flat")

    b1.place(
        x = 294, y = 296,
        width = 543,
        height = 107)

    window.resizable(False, False)
    window.mainloop()
#-------------------------------FB Ez Menu------------------------------------
def fbezmenu():
    window.geometry("1140x700")
    window.configure(bg = "#ffffff")
    canvas = Canvas(
        window,
        bg = "#ffffff",
        height = 700,
        width = 1140,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge")
    canvas.place(x = 0, y = 0)

    background_img = PhotoImage(file = f"All Game/Flappy Bird/EzMenu/EzBackground.png")
    background = canvas.create_image(
        570.0, 350.0,
        image=background_img)

    img0 = PhotoImage(file = f"All Game/Flappy Bird/EzMenu/EzExit.png")
    b0 = Button(
        image = img0,
        borderwidth = 0,
        highlightthickness = 0,
        command = fbird,
        relief = "flat")

    b0.place(
        x = 294, y = 475,
        width = 543,
        height = 107)

    img1 = PhotoImage(file = f"All Game/Flappy Bird/EzMenu/EzPlay.png")
    b1 = Button(
        image = img1,
        borderwidth = 0,
        highlightthickness = 0,
        command = fbez,
        relief = "flat")

    b1.place(
        x = 294, y = 296,
        width = 543,
        height = 107)

    window.resizable(False, False)
    window.mainloop()
#-------------------------------Flappy Bird-----------------------------------
def fbird():
    window.title('Game Flappy Bird')
    window.geometry("1140x700")
    window.configure(bg = "#ffffff")
    canvas = Canvas(
        window,
        bg = "#ffffff",
        height = 700,
        width = 1140,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge")
    canvas.place(x = 0, y = 0)

    background_img = PhotoImage(file = f"All Game/Flappy Bird/FBBackground.png")
    background = canvas.create_image(
        570.0, 350.0,
        image=background_img)

    img0 = PhotoImage(file = f"All Game/Flappy Bird/FBBack.png")
    b0 = Button(
        image = img0,
        borderwidth = 0,
        highlightthickness = 0,
        command = game,
        relief = "flat")

    b0.place(
        x = 30, y = 32,
        width = 120,
        height = 70)

    img1 = PhotoImage(file = f"All Game/Flappy Bird/FBHard.png")
    b1 = Button(
        image = img1,
        borderwidth = 0,
        highlightthickness = 0,
        command = fbharmenu,
        relief = "flat")

    b1.place(
        x = 294, y = 475,
        width = 543,
        height = 107)

    img2 = PhotoImage(file = f"All Game/Flappy Bird/FBEz.png")
    b2 = Button(
        image = img2,
        borderwidth = 0,
        highlightthickness = 0,
        command = fbezmenu,
        relief = "flat")

    b2.place(
        x = 294, y = 296,
        width = 543,
        height = 107)

    window.resizable(False, False)
    window.mainloop()
#-------------------------------Caro Free Menu--------------------------------
def carofreemenu():
    window.geometry("1140x700")
    window.configure(bg = "#ffffff")
    canvas = Canvas(
        window,
        bg = "#ffffff",
        height = 700,
        width = 1140,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge")
    canvas.place(x = 0, y = 0)

    background_img = PhotoImage(file = f"All Game/Caro/FreeMenu/FreeBackground.png")
    background = canvas.create_image(
        570.0, 350.0,
        image=background_img)

    img0 = PhotoImage(file = f"All Game/Caro/FreeMenu/FreePlay.png")
    b0 = Button(
        image = img0,
        borderwidth = 0,
        highlightthickness = 0,
        command = carofree,
        relief = "flat")

    b0.place(
        x = 295, y = 296,
        width = 543,
        height = 107)

    img1 = PhotoImage(file = f"All Game/Caro/FreeMenu/FreeExit.png")
    b1 = Button(
        image = img1,
        borderwidth = 0,
        highlightthickness = 0,
        command = caro,
        relief = "flat")

    b1.place(
        x = 295, y = 475,
        width = 543,
        height = 107)

    window.resizable(False, False)
    window.mainloop()
#-------------------------------Caro 3x3 Menu---------------------------------
def caro3x3menu():
    window.geometry("1140x700")
    window.configure(bg = "#ffffff")
    canvas = Canvas(
        window,
        bg = "#ffffff",
        height = 700,
        width = 1140,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge")
    canvas.place(x = 0, y = 0)

    background_img = PhotoImage(file = f"All Game/Caro/3x3Menu/3x3Background.png")
    background = canvas.create_image(
        570.0, 350.0,
        image=background_img)

    img0 = PhotoImage(file = f"All Game/Caro/3x3Menu/3x3Play.png")
    b0 = Button(
        image = img0,
        borderwidth = 0,
        highlightthickness = 0,
        command = caro3x3,
        relief = "flat")

    b0.place(
        x = 295, y = 296,
        width = 543,
        height = 107)

    img1 = PhotoImage(file = f"All Game/Caro/3x3Menu/3x3Exit.png")
    b1 = Button(
        image = img1,
        borderwidth = 0,
        highlightthickness = 0,
        command = caro,
        relief = "flat")

    b1.place(
        x = 295, y = 475,
        width = 543,
        height = 107)

    window.resizable(False, False)
    window.mainloop()
#-------------------------------Caro------------------------------------------
def caro():
    window.title('Game Caro')
    window.geometry("1140x700")
    window.configure(bg = "#ffffff")
    canvas = Canvas(
        window,
        bg = "#ffffff",
        height = 700,
        width = 1140,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge")
    canvas.place(x = 0, y = 0)

    background_img = PhotoImage(file = f"All Game/Caro/CaroBackground.png")
    background = canvas.create_image(
        570.0, 350.0,
        image=background_img)

    img0 = PhotoImage(file = f"All Game/Caro/CaroBack.png")
    b0 = Button(
        image = img0,
        borderwidth = 0,
        highlightthickness = 0,
        command = game,
        relief = "flat")

    b0.place(
        x = 30, y = 32,
        width = 120,
        height = 70)

    img1 = PhotoImage(file = f"All Game/Caro/Caro3x3.png")
    b1 = Button(
        image = img1,
        borderwidth = 0,
        highlightthickness = 0,
        command = caro3x3menu,
        relief = "flat")

    b1.place(
        x = 295, y = 296,
        width = 543,
        height = 107)

    img2 = PhotoImage(file = f"All Game/Caro/CaroFree.png")
    b2 = Button(
        image = img2,
        borderwidth = 0,
        highlightthickness = 0,
        command = carofreemenu,
        relief = "flat")

    b2.place(
        x = 295, y = 475,
        width = 543,
        height = 107)

    window.resizable(False, False)
    window.mainloop()
#-------------------------------Snake Hard Menu-------------------------------
def snakehardmenu():
    window.geometry("1140x700")
    window.configure(bg = "#ffffff")
    canvas = Canvas(
        window,
        bg = "#ffffff",
        height = 700,
        width = 1140,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge")
    canvas.place(x = 0, y = 0)

    background_img = PhotoImage(file = f"All Game/Snake/HardMenu/HardBackground.png")
    background = canvas.create_image(
        570.0, 350.0,
        image=background_img)

    img0 = PhotoImage(file = f"All Game/Snake/HardMenu/HardPlay.png")
    b0 = Button(
        image = img0,
        borderwidth = 0,
        highlightthickness = 0,
        command = snakehard,
        relief = "flat")

    b0.place(
        x = 295, y = 296,
        width = 543,
        height = 107)

    img1 = PhotoImage(file = f"All Game/Snake/HardMenu/HardExit.png")
    b1 = Button(
        image = img1,
        borderwidth = 0,
        highlightthickness = 0,
        command = snake,
        relief = "flat")

    b1.place(
        x = 296, y = 475,
        width = 543,
        height = 107)

    window.resizable(False, False)
    window.mainloop()
#-------------------------------Snake Ez Menu---------------------------------
def snakeezmanu():
    window.geometry("1140x700")
    window.configure(bg = "#ffffff")
    canvas = Canvas(
        window,
        bg = "#ffffff",
        height = 700,
        width = 1140,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge")
    canvas.place(x = 0, y = 0)

    background_img = PhotoImage(file = f"All Game/Snake/EzMenu/EzBackground.png")
    background = canvas.create_image(
        570.0, 350.0,
        image=background_img)

    img0 = PhotoImage(file = f"All Game/Snake/EzMenu/EzPlay.png")
    b0 = Button(
        image = img0,
        borderwidth = 0,
        highlightthickness = 0,
        command = snakeez,
        relief = "flat")

    b0.place(
        x = 295, y = 296,
        width = 543,
        height = 107)

    img1 = PhotoImage(file = f"All Game/Snake/EzMenu/EzExit.png")
    b1 = Button(
        image = img1,
        borderwidth = 0,
        highlightthickness = 0,
        command = snake,
        relief = "flat")

    b1.place(
        x = 296, y = 475,
        width = 543,
        height = 107)

    window.resizable(False, False)
    window.mainloop()
#-------------------------------Snake-----------------------------------------
def snake():
    window.title('Game Snake')
    window.geometry("1140x700")
    window.configure(bg = "#ffffff")
    canvas = Canvas(
        window,
        bg = "#ffffff",
        height = 700,
        width = 1140,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge")
    canvas.place(x = 0, y = 0)

    background_img = PhotoImage(file = f"All Game/Snake/SnakeBackground.png")
    background = canvas.create_image(
        570.0, 350.0,
        image=background_img)

    img0 = PhotoImage(file = f"All Game/Snake/SnakeEz.png")
    b0 = Button(
        image = img0,
        borderwidth = 0,
        highlightthickness = 0,
        command = snakeezmanu,
        relief = "flat")

    b0.place(
        x = 295, y = 296,
        width = 543,
        height = 107)

    img1 = PhotoImage(file = f"All Game/Snake/SnakeHard.png")
    b1 = Button(
        image = img1,
        borderwidth = 0,
        highlightthickness = 0,
        command = snakehardmenu,
        relief = "flat")

    b1.place(
        x = 296, y = 475,
        width = 543,
        height = 107)

    img2 = PhotoImage(file = f"All Game/Snake/SnakeBack.png")
    b2 = Button(
        image = img2,
        borderwidth = 0,
        highlightthickness = 0,
        command = game,
        relief = "flat")

    b2.place(
        x = 30, y = 32,
        width = 120,
        height = 70)

    window.resizable(False, False)
    window.mainloop()
#-------------------------------Game------------------------------------------
def game():
    window.title('Menu Game')
    window.geometry("1140x700")
    window.configure(bg = "#ffffff")
    canvas = Canvas(
        window,
        bg = "#ffffff",
        height = 700,
        width = 1140,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge")
    canvas.place(x = 0, y = 0)

    background_img = PhotoImage(file = f"Game/GameBackground.png")
    background = canvas.create_image(
        570.0, 350.0,
        image=background_img)

    img0 = PhotoImage(file = f"Game/GameSnake.png")
    b0 = Button(
        image = img0,
        borderwidth = 0,
        highlightthickness = 0,
        command = snake,
        relief = "flat")

    b0.place(
        x = 297, y = 322,
        width = 543,
        height = 107)

    img1 = PhotoImage(file = f"Game/GameFBird.png")
    b1 = Button(
        image = img1,
        borderwidth = 0,
        highlightthickness = 0,
        command = fbird,
        relief = "flat")

    b1.place(
        x = 299, y = 496,
        width = 543,
        height = 107)

    img2 = PhotoImage(file = f"Game/GameCaro.png")
    b2 = Button(
        image = img2,
        borderwidth = 0,
        highlightthickness = 0,
        command = caro,
        relief = "flat")

    b2.place(
        x = 299, y = 148,
        width = 543,
        height = 107)

    img3 = PhotoImage(file = f"Game/GameBack.png")
    b3 = Button(
        image = img3,
        borderwidth = 0,
        highlightthickness = 0,
        command = menu,
        relief = "flat")

    b3.place(
        x = 30, y = 32,
        width = 120,
        height = 70)

    window.resizable(False, False)
    window.mainloop()
#-------------------------------Menu------------------------------------------
def menu():
    window.title('Menu')
    window.geometry("1140x700")
    window.configure(bg = "#ffffff")
    canvas = Canvas(
        window,
        bg = "#ffffff",
        height = 700,
        width = 1140,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge")
    canvas.place(x = 0, y = 0)

    background_img = PhotoImage(file = f"Menu/MenuBackground.png")
    background = canvas.create_image(
        570.0, 347.5,
        image=background_img)

    img0 = PhotoImage(file = f"Menu/MenuGame.png")
    b0 = Button(
        image = img0,
        borderwidth = 0,
        highlightthickness = 0,
        command = game,
        relief = "flat")

    b0.place(
        x = 118, y = 244,
        width = 435,
        height = 180)

    img1 = PhotoImage(file = f"Menu/MenuTruyen.png")
    b1 = Button(
        image = img1,
        borderwidth = 0,
        highlightthickness = 0,
        command = truyen,
        relief = "flat")

    b1.place(
        x = 588, y = 244,
        width = 435,
        height = 180)

    img2 = PhotoImage(file = f"Menu/MenuMovie.png")
    b2 = Button(
        image = img2,
        borderwidth = 0,
        highlightthickness = 0,
        command = movie,
        relief = "flat")

    b2.place(
        x = 118, y = 467,
        width = 435,
        height = 180)

    img3 = PhotoImage(file = f"Menu/MenuMusic.png")
    b3 = Button(
        image = img3,
        borderwidth = 0,
        highlightthickness = 0,
        command = music,
        relief = "flat")

    b3.place(
        x = 588, y = 467,
        width = 435,
        height = 180)

    window.resizable(False, False)
    window.mainloop()
#-------------------------------Error-----------------------------------------
def enough():
    window.title('Error')
    window.geometry("1140x700")
    window.configure(bg = "#ffffff")
    canvas = Canvas(
        window,
        bg = "#ffffff",
        height = 700,
        width = 1140,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge")
    canvas.place(x = 0, y = 0)

    background_img = PhotoImage(file = f"Error/EnoughBackground.png")
    background = canvas.create_image(
        570.0, 350.0,
        image=background_img)

    img0 = PhotoImage(file = f"Error/EnoughYes.png")
    b0 = Button(
        image = img0,
        borderwidth = 0,
        highlightthickness = 0,
        command = register,
        relief = "flat")

    b0.place(
        x = 508, y = 384,
        width = 125,
        height = 65)

    window.resizable(False, False)
    window.mainloop()
def missing():
    window.title('Error')
    window.geometry("1140x700")
    window.configure(bg = "#ffffff")
    canvas = Canvas(
        window,
        bg = "#ffffff",
        height = 700,
        width = 1140,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge")
    canvas.place(x = 0, y = 0)

    background_img = PhotoImage(file = f"Error/MissingBackground.png")
    background = canvas.create_image(
        570.0, 350.0,
        image=background_img)

    img0 = PhotoImage(file = f"Error/MissingYes.png")
    b0 = Button(
        image = img0,
        borderwidth = 0,
        highlightthickness = 0,
        command = register,
        relief = "flat")

    b0.place(
        x = 508, y = 384,
        width = 125,
        height = 65)

    window.resizable(False, False)
    window.mainloop()
def wrong():
    window.title('Error')
    window.geometry("1140x700")
    window.configure(bg = "#ffffff")
    canvas = Canvas(
        window,
        bg = "#ffffff",
        height = 700,
        width = 1140,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge")
    canvas.place(x = 0, y = 0)

    background_img = PhotoImage(file = f"Error/WrongBackground.png")
    background = canvas.create_image(
        570.0, 350.0,
        image=background_img)

    img0 = PhotoImage(file = f"Error/WrongYes.png")
    b0 = Button(
        image = img0,
        borderwidth = 0,
        highlightthickness = 0,
        command = login,
        relief = "flat")

    b0.place(
        x = 508, y = 384,
        width = 125,
        height = 65)

    window.resizable(False, False)
    window.mainloop()
#-------------------------------Create Acc------------------------------------
def tryregister():
    if stringHO.get() == "":
        missing()
    elif stringTEN.get() == "":
        missing()
    elif stringTK.get() == "":
        missing()
    elif len(stringTK.get()) < 6:
        enough()
    elif stringMK.get() == "":
        missing()
    elif len(stringMK.get()) < 6:
        enough()
    else:
        cursor.execute("INSERT INTO users VALUES (?,?,?,?)", stringHO.get(), stringTEN.get(), stringTK.get(), stringMK.get())
        conx.commit()
        login()
#-------------------------------Register--------------------------------------
def register():
    global stringHO, stringTEN, stringTK, stringMK, cursor, conx
    conx = pyodbc.connect("Driver={SQL Server};"
                    "Server=LAPTOP-G463R823\SQLEXPRESS;"
                    "Database=FUN_Account;"
                    "Trusted_Connection=yes;")
    cursor = conx.cursor()

    stringHO = StringVar()
    stringTEN = StringVar()
    stringTK = StringVar()
    stringMK = StringVar()

    window.title('Register')
    window.geometry("1140x700")
    window.configure(bg = "#ffffff")
    canvas = Canvas(
        window,
        bg = "#ffffff",
        height = 700,
        width = 1140,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge")
    canvas.place(x = 0, y = 0)
    
    background_img = PhotoImage(file = f"Register/RegisterBackground.png")
    background = canvas.create_image(
        574.0, 350.0,
        image=background_img)
    
    img0 = PhotoImage(file = f"Register/RegisterRg.png")
    b0 = Button(
        image = img0,
        borderwidth = 0,
        highlightthickness = 0,
        command = tryregister,
        relief = "flat")
    
    b0.place(
        x = 400, y = 432,
        width = 125,
        height = 65)
    
    img1 = PhotoImage(file = f"Register/RegisterCancel.png")
    b1 = Button(
        image = img1,
        borderwidth = 0,
        highlightthickness = 0,
        command = login,
        relief = "flat")
    
    b1.place(
        x = 614, y = 432,
        width = 125,
        height = 65)
    
    entry0_img = PhotoImage(file = f"Register/RegisterTK.png")
    entry0_bg = canvas.create_image(
        578.0, 330.5,
        image = entry0_img)
    
    entry0 = Entry(
        bd = 0,
        bg = "#9d9d9d",
        highlightthickness = 0,
        textvariable=stringTK)
    
    entry0.place(
        x = 378, y = 313,
        width = 400,
        height = 33)
    
    entry1_img = PhotoImage(file = f"Register/RegisterMK.png")
    entry1_bg = canvas.create_image(
        578.0, 399.5,
        image = entry1_img)
    
    entry1 = Entry(
        bd = 0,
        bg = "#9d9d9d",
        highlightthickness = 0,
        textvariable=stringMK)
    
    entry1.place(
        x = 378, y = 382,
        width = 400,
        height = 33)
    
    entry2_img = PhotoImage(file = f"Register/RegisterHO.png")
    entry2_bg = canvas.create_image(
        463.0, 260.5,
        image = entry2_img)
    
    entry2 = Entry(
        bd = 0,
        bg = "#9d9d9d",
        highlightthickness = 0,
        textvariable=stringHO)
    
    entry2.place(
        x = 378, y = 243,
        width = 170,
        height = 33)
    
    entry3_img = PhotoImage(file = f"Register/RegisterTEN.png")
    entry3_bg = canvas.create_image(
        693.0, 260.5,
        image = entry3_img)
    
    entry3 = Entry(
        bd = 0,
        bg = "#9d9d9d",
        highlightthickness = 0,
        textvariable=stringTEN)
    
    entry3.place(
        x = 608, y = 243,
        width = 170,
        height = 33)
    
    window.resizable(False, False)
    window.mainloop()
#-------------------------------Logout----------------------------------------
def logout():
    window.title('Logout')
    window.geometry("1140x700")
    window.configure(bg = "#ffffff")
    canvas = Canvas(
        window,
        bg = "#ffffff",
        height = 700,
        width = 1140,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge")
    canvas.place(x = 0, y = 0)
    
    background_img = PhotoImage(file = f"Logout/LogoutBackground.png")
    background = canvas.create_image(
        570.0, 350.0,
        image=background_img)
    
    img0 = PhotoImage(file = f"Logout/LogoutYes.png")
    b0 = Button(
        image = img0,
        borderwidth = 0,
        highlightthickness = 0,
        command = window.destroy,
        relief = "flat")
    
    b0.place(
        x = 405, y = 371,
        width = 125,
        height = 65)
    
    img1 = PhotoImage(file = f"Logout/LogoutNo.png")
    b1 = Button(
        image = img1,
        borderwidth = 0,
        highlightthickness = 0,
        command = standing,
        relief = "flat")
    
    b1.place(
        x = 616, y = 371,
        width = 125,
        height = 65)
    
    window.resizable(False, False)
    window.mainloop()
#-------------------------------Check User------------------------------------
def trylogin(event=None):
    if stringTK.get() == "" or stringMK.get() == "":
        print("Please complete the required field!")
    else:
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (stringTK.get(), stringMK.get()))
        if cursor.fetchone() is not None:
            stringTK.set("")
            stringMK.set("")
            menu()
        else:
            stringTK.set("")
            stringMK.set("")
            wrong()
#-------------------------------Login-----------------------------------------
def login():
    global stringTK, stringMK , cursor
    stringTK = StringVar()
    stringMK = StringVar()

    conx = pyodbc.connect("Driver={SQL Server};"
                "Server=LAPTOP-G463R823\SQLEXPRESS;"
                "Database=FUN_Account;"
                "Trusted_Connection=yes;")
    cursor = conx.cursor()
    statement = f"SELECT username, password from users WHERE username='{stringTK}';"
    cursor.execute(statement)

    window.title('Login')
    window.geometry("1140x700")
    window.configure(bg = "#ffffff")
    canvas = Canvas(
        window,
        bg = "#ffffff",
        height = 700,
        width = 1140,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge")
    canvas.place(x = 0, y = 0)
    
    background_img = PhotoImage(file = f"Login/LoginBackground.png")
    background = canvas.create_image(
        574.0, 350.0,
        image=background_img)
    
    img0 = PhotoImage(file = f"Login/Loginlg.png")
    b0 = Button(
        image = img0,
        borderwidth = 0,
        highlightthickness = 0,
        command = trylogin,
        relief = "flat")
    
    b0.place(
        x = 378, y = 432,
        width = 125,
        height = 65)
    
    img1 = PhotoImage(file = f"Login/LoginCancel.png")
    b1 = Button(
        image = img1,
        borderwidth = 0,
        highlightthickness = 0,
        command = standing,
        relief = "flat")
    
    b1.place(
        x = 653, y = 432,
        width = 125,
        height = 65)
    
    entry0_img = PhotoImage(file = f"Login/LoginTk.png")
    entry0_bg = canvas.create_image(
        578.0, 292.5,
        image = entry0_img)
    
    entry0 = Entry(
        bd = 0,
        bg = "#9d9d9d",
        highlightthickness = 0,
        textvariable=stringTK)
    
    entry0.place(
        x = 378, y = 265,
        width = 400,
        height = 53)
    
    entry1_img = PhotoImage(file = f"Login/LoginMK.png")
    entry1_bg = canvas.create_image(
        578.0, 388.5,
        image = entry1_img)
    
    entry1 = Entry(
        bd = 0,
        bg = "#9d9d9d",
        highlightthickness = 0,
        textvariable=stringMK,
        show='*')
    
    entry1.place(
        x = 378, y = 361,
        width = 400,
        height = 53)
    
    img2 = PhotoImage(file = f"Login/LoginRegister.png")
    b4 = Button(
        image = img2,
        borderwidth = 0,
        highlightthickness = 0,
        command = register,
        relief = "flat")
    
    b4.place(
        x = 515, y = 432,
        width = 125,
        height = 65)
    window.resizable(False, False)
    window.mainloop()    
#-------------------------------Standing--------------------------------------
def standing():
    window.title('Standing')
    window.geometry("1140x700")
    window.configure(bg = "#ffffff")
    canvas = Canvas(
        window,
        bg = "#ffffff",
        height = 700,
        width = 1140,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge")
    canvas.place(x = 0, y = 0)

    background_img = PhotoImage(file = f"Standing/StandingBackground.png")
    background = canvas.create_image(
        570.0, 350.0,
        image=background_img)

    img0 = PhotoImage(file = f"Standing/StandingLogin.png")
    b0 = Button(
        image = img0,
        borderwidth = 0,
        highlightthickness = 0,
        command = login,
        relief = "flat")

    b0.place(
        x = 389, y = 538,
        width = 140,
        height = 75)

    img1 = PhotoImage(file = f"Standing/StandingLogout.png")
    b1 = Button(
        image = img1,
        borderwidth = 0,
        highlightthickness = 0,
        command = logout,
        relief = "flat")

    b1.place(
        x = 610, y = 538,
        width = 140,
        height = 75)

    window.resizable(False, False)
    window.mainloop()

window = Tk()

window.title('Standing')

window.geometry("1140x700")
window.configure(bg = "#ffffff")
canvas = Canvas(
    window,
    bg = "#ffffff",
    height = 700,
    width = 1140,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas.place(x = 0, y = 0)

background_img = PhotoImage(file = f"Standing/StandingBackground.png")
background = canvas.create_image(
    570.0, 350.0,
    image=background_img)

img0 = PhotoImage(file = f"Standing/StandingLogin.png")
b0 = Button(
    image = img0,
    borderwidth = 0,
    highlightthickness = 0,
    command = login,
    relief = "flat")

b0.place(
    x = 389, y = 538,
    width = 140,
    height = 75)

img1 = PhotoImage(file = f"Standing/StandingLogout.png")
b1 = Button(
    image = img1,
    borderwidth = 0,
    highlightthickness = 0,
    command = logout,
    relief = "flat")

b1.place(
    x = 610, y = 538,
    width = 140,
    height = 75)

window.resizable(False, False)
window.mainloop()