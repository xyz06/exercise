import random
import pygame
import sys, time
from pygame.locals import *
import argparse



def runing_text(title,color):
    pygame.init()
    screen = pygame.display.set_mode((600, 300))
    pygame.display.set_caption("hello world")

    white = (255, 255, 255)
    blue = (0, 0, 255)
    red = (255, 0, 0)
    orange = (255, 156, 0)
    yellow = (255, 255, 0)
    green = (0, 255, 0)
    colors = {'white': white, 'blue': blue, 'red': red, 'orange': orange,'yellow':yellow, 'green': green}
    x = 0
    y = 0
    vel_x = 2
    vel_y = 1
    myfont = pygame.font.Font(None, 60)
    mytitle = myfont.render(title, True, colors[color])
    ztx, zty, ztw, zth = mytitle.get_rect()

    flag = True
    while 1:
        for event in pygame.event.get():
            if event.type in (QUIT, KEYDOWN):
                sys.exit()

        screen.fill((0, 0, 0))

        x += vel_x
        if x >= 610 and flag:

            y = y + 20
            x = 0

        if y > 260 and x == 0 and flag:
            print("Start the collision")
            flag = False
            y = 260
            vel_x = -vel_x
            vel_y = -vel_y

        #after collision change color
        if not flag:  # x += vel_x
            y += vel_y
            if x > 600 - ztw or x < 0:
                vel_x = -vel_x
                mytitle = myfont.render(title, True, random.choice(list(colors.values())))
            if y > 260 or y < 0:
                mytitle = myfont.render(title, True, random.choice(list(colors.values())))
                vel_y = -vel_y

            if y == 260 and x == 102:
                flag = True
                vel_y = -vel_y
                x = 0
                y = 0

        screen.blit(mytitle, (x, y))
        pygame.display.update()
        time.sleep(0.006)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--title", type=str, required=True)
    parser.add_argument("--color", type=str, default='red', help="chocie one color [white, blue, red, orange, yellow, green] ")
    args = parser.parse_args()
    runing_text(args.title,args.color)
