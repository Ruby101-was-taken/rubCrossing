from typing import Any
import pygame, os, random, copy

from pygame.sprite import Group, Sprite


os.system("cls")

#python -m pygbag ENDINGSIM
#run in cmd in the folder above (in this case !JAMS)
#go into to !JAMS folder and type 'cmd' into address bar

# Define colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PINK = (255, 192, 203)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
BROWN = (165, 42, 42)
GREY = (128, 128, 128)
WHITE = (255,255,255)
LOGORED = (170, 32, 32)

# Set win dimensions
w = 800
h = 450

minW, minH = 252, 180

# Initialize Pygame
pygame.init()
pygame.mixer.init()
pygame.joystick.init()

class noJoystick:
    def get_init(self):
        return False
    def get_button(self, num):
        return False
    def get_axis(self, num):
        return False
    def get_hat(self, num):
        return (0,0)

num_joysticks = pygame.joystick.get_count()

if num_joysticks > 0:
    if num_joysticks == 1:
        joystick = pygame.joystick.Joystick(0)
        joystick.rumble(1, 1, 1000)
    else:
        from extraControllers import getController
        joystick = pygame.joystick.Joystick(getController(num_joysticks, pygame.joystick))
        joystick.rumble(1, 1, 1000)
    joystick.init()
else:
    print("No controllers found.")
    joystick = noJoystick()

isXboxController = False
if joystick.get_init():
    if "xbox" in joystick.get_name().lower():
        isXboxController = True

# Set up the display
win = pygame.display.set_mode((w, h), pygame.RESIZABLE) #sets up window
pygame.display.set_caption("TITLE") #Set title
pygame.display.set_icon(pygame.image.load('icon.png')) #Set icon

logo=[pygame.image.load('logo/logosubless.png'), pygame.image.load('logo/logoSUB.png'), pygame.image.load('logo/logoBGless.png')]

for i in range(500):
    win.fill(LOGORED)
    if i<=100:
        win.blit(logo[0], (int(w/2)-168, int(h/2)-48))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
                quit()
    elif i<200:
        subLength = int(w/2)-168+40
        subHeight = int(h/2)-40
        win.blit(logo[0], (int(w/2)-168, int(h/2)-48))
        win.blit(logo[1], (subLength, (subHeight*i / 100)-subHeight))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
                quit()
    elif i<500:
        win.blit(logo[0], (int(w/2)-168, int(h/2)-48))
        win.blit(logo[1], (subLength, (subHeight*200 / 100)-subHeight))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
                quit()
    
    pygame.display.flip()

loadingTexts = ["LOADING IMAGES", "LOADING UI", "LOADING SOUNDS"]


# Set up fonts
smallFont = pygame.font.SysFont("arial", 20)
smallerFont = pygame.font.SysFont("arial", 15)
bigFont = pygame.font.SysFont("arial", 45)

# Set up timer
clock = pygame.time.Clock()

#load image text
win.blit(smallFont.render(loadingTexts[0], True, (255, 255, 255)), (0,200+(0*20)))
pygame.display.flip()

#LOAD IMAGES 




win.blit(smallFont.render(loadingTexts[0] + " - COMPLETED", True, (255, 255, 255)), (0,200+(0*20)))
pygame.display.flip()

#load ui text
win.blit(smallFont.render(loadingTexts[1], True, (255, 255, 255)), (0,200+(1*20)))
pygame.display.flip()
ui = {
}

win.blit(smallFont.render(loadingTexts[1] + " - COMPLETED", True, (255, 255, 255)), (0,200+(1*20)))
pygame.display.flip()


#load sounds text
win.blit(smallFont.render(loadingTexts[2], True, (255, 255, 255)), (0,200+(2*20)))
pygame.display.flip()
sound = {
}

win.blit(smallFont.render(loadingTexts[1] + " - COMPLETED", True, (255, 255, 255)), (0,200+(2*20)))
pygame.display.flip()

class AllSprites:
    def __init__(self) -> None:
        self.allSprites = []
    def resizeSprites(self):
        for spriteGroup in self.allSprites:
            for sprite in spriteGroup:
                sprite.resize()
    def add(self, spriteGroup):
        self.allSprites.append(spriteGroup)
    def draw(self, win):
        for spriteGroup in self.allSprites:
           spriteGroup.draw(win)
    def update(self, deltaTime):
        for spriteGroup in self.allSprites:
            spriteGroup.update(deltaTime)
            
class World:
    def __init__(self) -> None:
        self.x = w // 2
        self.y = h // 2
    
    def update(self, deltaTime):
        if self.x < -375:
            self.x = -375
        elif self.x > 4575:
            self.x = 4575
        if self.y < -200:
            self.y = -200
        elif self.y > 4750:
            self.y = 4750
        
world = World()

        
class Thing(pygame.sprite.Sprite):
    def __init__(self, x, y) -> None:
        super().__init__()
        self.image = pygame.Surface((50, 50))  # Replace this with your player image
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (x-(self.image.get_width()/2), y-(self.image.get_height()/2))
        
        self.x, self.y = x, y
    def update(self, deltaTime) -> None:
        self.rect.x = self.x-world.x
        self.rect.y = self.y-world.y
        
    def resize(self):
        self.x = self.x+int((w-oldW)/2)
        self.y = self.y+int((h-oldH)/2)
    

class Player(Thing):
    def __init__(self, x, y):
        super().__init__(0,0)
        self.image.fill(BLUE)
        self.rect.center = (x, y)

    def update(self, deltaTime):
        self.move(deltaTime)
    def move(self, deltaTime):
        if keys[pygame.K_w]:
            world.y -= 5*deltaTime
        if keys[pygame.K_s]:
            world.y += 5*deltaTime
        if keys[pygame.K_a]:
            world.x -= 5*deltaTime
        if keys[pygame.K_d]:
            world.x += 5*deltaTime
            
    def resize(self):
        self.rect.x = self.rect.x+int((w-oldW)/2)
        self.rect.y = self.rect.y+int((h-oldH)/2)

class Tile(Thing):
    def __init__(self, x, y) -> None:
        super().__init__(x, y)
        self.image.fill((random.randint(0,255), random.randint(0,255), random.randint(0,255)))
            

class UICanvas:
    def __init__(self) -> None:
        self.UIComponents = []
    def addElement(self, element):
        self.UIComponents.append(element)
    def getElementByTag(self, tag:str):
        for element in self.UIComponents:
            if element.tag == tag:
                return element
    def draw(self):
        for element in self.UIComponents:
            element.draw()
    def update(self):
        for element in self.UIComponents:
            element.update()

class UIElement:
    def __init__(self, screenPos, tag:str) -> None:
        self.screenPos = screenPos
        self.tag = tag
        self.surface = pygame.Surface((0,0), pygame.SRCALPHA)
        self.show = True
    def toggleShow(self):
        self.show = not self.show
    def setShow(self, setTo:bool):
        self.show = setTo
    def moveTo(self, newPos):
        self.screenPos = newPos
    def draw(self):
        if self.show:
            win.blit(self.surface, self.screenPos)
    def update(self):
        pass

class UIText(UIElement):
    def __init__(self, screenPos, tag:str, text="", fontSize=10, colour=(0,0,0), padding=20) -> None:
        super().__init__(screenPos, tag)
        self.text = text
        self.fontSize = fontSize
        self.colour = colour
        self.font = pygame.font.SysFont("arial", self.fontSize)
        self.surface = self.font.render(text, True, self.colour)
        self.padding = padding

        self.surface = pygame.Surface((self.surface.get_width() + self.padding*2, self.surface.get_height() + self.padding*2), pygame.SRCALPHA)
        self.bg = UIRect((0,0), "textBGEmpty", self.surface.get_width(),self.surface.get_height(), colour)

        self.updateText(self.text)
    def updateText(self, newText:str, fontSize=None, colour=None):
        if fontSize!=None:
            self.fontSize = fontSize
        if colour!=None:
            self.colour = colour
        self.font = pygame.font.SysFont("arial", self.fontSize)
        textSurf = self.font.render(newText, True, self.colour)
        self.surface = textSurf.copy()
        self.surface = pygame.Surface((textSurf.get_width() + self.padding*2, textSurf.get_height() + self.padding*2), pygame.SRCALPHA)

        if self.bg.tag!="textBGEmpty":
            self.bg.updateSize(self.surface.get_width(),self.surface.get_height())
            self.bg.updateSurface()

            self.surface.blit(self.bg.surface, (0,0))
        self.surface.blit(textSurf, (self.padding,self.padding))
    def setBG(self, colour):
        self.bg = UIRect((0,0), "textBG", self.surface.get_width(),self.surface.get_height(), colour)
        self.updateText(self.text)
    def removeBG(self):
        self.bg.tag = "textBGEmpty"
        self.updateText(self.text)
    def updatePadding(self, newPadding):
        self.padding = newPadding
        self.updateText(self.text)

class UIRect(UIElement):
    def __init__(self, screenPos, tag:str, w:int, h:int, colour=(0,0,0)) -> None:
        super().__init__(screenPos, tag)
        self.updateRect(w, h, colour)
    def updateRect(self, w:int, h:int, colour=None):
        self.w, self.h = w, h
        self.rect = pygame.Rect(self.screenPos[0], self.screenPos[1], self.w, self.h)
        self.surface = pygame.Surface((w, h))
        if colour != None:
            self.colour = colour
        pygame.draw.rect(self.surface, self.colour, self.rect)
    def updateSurface(self):
        pygame.draw.rect(self.surface, self.colour, self.rect)
    def updateSize(self, w, h):
        self.w, self.h = w, h
        self.rect = pygame.Rect(self.screenPos[0], self.screenPos[1], self.w, self.h)
        self.surface = pygame.Surface((w, h))
        
class UIButton(UIText):
    def __init__(self, screenPos, tag:str, onClick, text="", fontSize=10, padding=20, textColour=(0, 0, 0), buttonColours=((255,255,255), (127,127,127), (0,0,0)), canHold=False) -> None:
        super().__init__(screenPos, tag, text, fontSize, textColour, padding)
        self.setBG(buttonColours[0])
        self.onClick = onClick
        self.held = False
        self.canHold = canHold
        self.buttonColours = buttonColours
    def update(self):
        tempRect = self.surface.get_rect()
        tempRect.x, tempRect.y = self.screenPos[0], self.screenPos[1]
        if tempRect.collidepoint(posx, posy):
            self.setBG(self.buttonColours[1])
            if clicked[0]:
                self.setBG(self.buttonColours[2])
                if not self.held:
                    self.held = not self.canHold
                    self.onClick()
        if not tempRect.collidepoint(posx, posy):
            self.setBG(self.buttonColours[0])

        self.held = clicked[0] or self.canHold

class UIImage(UIElement):
    def __init__(self, screenPos, tag: str, image:pygame.Surface) -> None:
        super().__init__(screenPos, tag)
        self.surface = image
   
class AudioPlayer:
    def __init__(self) -> None:
        pass
    def playSound(self, soundSrc, volume=100, channel=0):
        sound = soundSrc.sound
        sound.set_volume(volume)
        if channel != 0 or channel > 6:
            pygame.mixer.Channel(channel).play(sound)
        else:
            sound.play()
    def playMusic(self, musicSrc, volume=100):
        sound = musicSrc.sound
        sound.set_volume(volume)
        pygame.mixer.Channel(7).play(sound, -1)
    
class AudioSource:
    def __init__(self, soundPath:str) -> None:
        self.sound = pygame.mixer.Sound("sound/" + soundPath)

class InputSystem:
    def __init__(self) -> None:
        self.inputDict = {}
        self.controllerDict = {}
        self.axisDict = {}
    def setKey(self, keyEnum, inputName:str):
        if inputName in self.inputDict:
            self.inputDict[inputName].append(keyEnum)
        else:
            self.inputDict[inputName] = [keyEnum]
    def setButton(self, buttonNum, inputName:str):
        if inputName in self.controllerDict:
            self.controllerDict[inputName].append(buttonNum)
        else:
            self.controllerDict[inputName] = [buttonNum]
    def setAxis(self, axis, axisRange, inputName):
        if inputName in self.axisDict:
            self.axisDict[inputName].append([axis, axisRange])
        else:
            self.axisDict[inputName] = [[axis, axisRange]]
    def inputEvent(self, inputName:str) -> bool:
        inputted = False
        if inputName in self.inputDict:
            for keyEnum in self.inputDict[inputName]:
                if keys[keyEnum]:
                    inputted = True
        if joystick.get_init():
            if not inputted and inputName in self.controllerDict:
                for button in self.controllerDict[inputName]:
                    if joystick.get_button(button):
                        inputted = True
            if not inputted and inputName in self.axisDict:
                for axis in self.axisDict[inputName]:
                    if joystick.get_axis(axis[0]) > axis[1][0] and joystick.get_axis(axis[0]) < axis[1][1]:
                        inputted = True
        return inputted
    def rumble(self, lf, hf, dur):
        if joystick.get_init():
            joystick.rumble(lf, hf, dur)

inputs = InputSystem()
inputs.setKey(pygame.K_SPACE, "Jump")
inputs.setButton(0, "Jump")
pygame.time.delay(100)

allSprites = AllSprites()


wallSprites = pygame.sprite.Group()
wallSprites.add(Thing(100, 100))

allSprites.add(wallSprites)

worldTiles = pygame.sprite.Group()
for y in range(100):
    for x in range(100):
        worldTiles.add(Tile(x*50, y*50))

allSprites.add(worldTiles)

ui = UICanvas()
# ui.addElement(UIText((20, 504), "Sample", "Hello World", 40, BLACK))

# Create player SHOULD ALWAYS BE ADDED LAST OF ALL GAMEOBJECT (AKA SPRITES
player = Player(w // 2, h // 2)
playerSprites = pygame.sprite.Group()
playerSprites.add(player)

allSprites.add(playerSprites)

def redrawScreen():
    win.fill(WHITE)
    
    allSprites.draw(win)
    
    # Draw sprites
    ui.draw()
    #updates screen
    pygame.display.flip()

deltaTime = 0
run = True
sizeMultiplierW, sizeMultiplierH = 1, 1
# Main game loop
while run:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False
            quit()
        elif event.type == pygame.MOUSEWHEEL:
            scrolly = event.y
        elif event.type == pygame.WINDOWRESIZED:
            oldW, oldH = w, h
            w = event.x if event.x>minW else minW
            h = event.y if event.y>minH else minH
            win = pygame.display.set_mode((w, h), pygame.RESIZABLE)
            
            sizeMultiplierW, sizeMultiplierH = w/oldW, h/oldH
            
            allSprites.resizeSprites()
            

    
    #mouse getters
    clicked = pygame.mouse.get_pressed(num_buttons=3)
    posx, posy = pygame.mouse.get_pos()
    #get pressed keys
    keys = pygame.key.get_pressed()

    allSprites.update(deltaTime)
    
    world.update(deltaTime)
    
    
 # Update player and UI
    ui.update()


    #redraw win
    redrawScreen()
    
    #for web version
    #await asyncio.sleep(0)
    
    # Set the framerate
    deltaTime = clock.tick(60)/10

