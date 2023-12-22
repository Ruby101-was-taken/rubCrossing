

import pygame, os
from pygame.locals import *


smallFont = pygame.font.SysFont("arial", 20)



def getController(numOfJoy, joy):
    class Button():
        def __init__(self, x, y, width, height, buttonText='Button', ID = 0):
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.ID = ID
            self.alreadyPressed = False

            self.fillColors = {
                'normal': '#ffffff',
                'hover': '#666666',
                'pressed': '#333333',
            }
            
            self.buttonSurface = pygame.Surface((self.width, self.height))
            self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

            self.buttonSurf = smallFont.render(buttonText, True, (20, 20, 20))

            self.buttonText = buttonText
        
        def process(self):
            mousePos = pygame.mouse.get_pos()
            if self.buttonRect.collidepoint(mousePos):
                
                if pygame.mouse.get_pressed(num_buttons=3)[0]:
                    return self.ID
                else:
                    return -1
            else:
                return -1
        def draw(self):
            mousePos = pygame.mouse.get_pos()
            self.buttonSurface.fill(self.fillColors['normal'])
            if self.buttonRect.collidepoint(mousePos):
                self.buttonSurface.fill(self.fillColors['hover'])
                if pygame.mouse.get_pressed(num_buttons=3)[0]:
                    self.buttonSurface.fill(self.fillColors['pressed'])
            self.buttonSurface.blit(self.buttonSurf, [
                self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2,
                self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2
            ])
            win.blit(self.buttonSurface, self.buttonRect)
    pygame.init()

    controllerSelected = False
    smallFont = pygame.font.SysFont("arial", 20)

    buttons = []
    for button in range(numOfJoy):
        buttons.append(Button(0, 25+(30*button), 800, 30, joy.Joystick(button).get_name(), button))


    win = pygame.display.set_mode((800, 50*numOfJoy))
    pygame.display.set_caption("Multiple Controllers Conected!")
    while not controllerSelected:  
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                controllerSelected = True
                quit()
        win.fill((0,0,0))
        win.blit(smallFont.render(f"There are {numOfJoy} controllers connected. Selected one to continue (You can still use keyboard and mouse!)", True, (255, 255, 255)), (0,0))

        for button in buttons:
            button.draw()
            if button.process() != -1:
                controllerSelected = True
                return button.ID


        pygame.display.flip()
    
