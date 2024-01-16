import pygame
import copy

class Component:
    def __init__(self) -> None:
        pass
    def update(self, deltaTime):
        pass
    def start(self):
        pass

class Renderer(Component):
    def __init__(self, image=None, w=32, h=32, colour=(0,0,255), alwaysDraw=False) -> None:
        super().__init__()
        self.setImage(image, w, h, colour)
            
        self.isVisible = True
        
        self.flipX, self.flipY = False, False
        
        self.alwaysDraw = alwaysDraw
    def start(self):
        self.gameObject.renderer = self
    def draw(self, win, offset=(0,0), useCam=True):
        if self.gameObject.game.camera.lockOn != self.gameObject and self.isVisible:
            win.blit(self.surface, (self.gameObject.x-(self.gameObject.game.camera.x if useCam else 0)+offset[0], self.gameObject.y-(self.gameObject.game.camera.y if useCam else 0)+offset[0]))
        else:
            win.blit(self.surface, ((400-self.w/2)+offset[0], (225-self.h/2)+offset[1]))
    
    def setFlip(self, x=True, y=False):
        self.flipX, self.flipY = x, y
        
        
        
    def update(self, deltaTime):
        x = self.gameObject.x-self.gameObject.game.camera.x
        y = self.gameObject.y-self.gameObject.game.camera.y
        
        self.isVisible = ((-self.w < x < 800 and -self.h < y < 450) and self.isVisible) or self.alwaysDraw 

    def setImage(self, image, w=32, h=32, colour=(0,0,255)):
        self.surface = pygame.Surface((w, h), pygame.SRCALPHA)
        if image == None:
            self.surface.fill(colour)
            self.baseSurface = copy.copy(self.surface)
            self.w = w
            self.h = h
        else:
            self.surface = image
            self.baseSurface = copy.copy(self.surface)
            self.w = image.get_width()
            self.h = image.get_height()
        
        

class SquareCollider(Component):
    def __init__(self, w:int, h:int, offset = (0,0)) -> None:
        super().__init__()
        self.w = w
        self.h = h
        self.offset = offset
    def start(self):
        self.gameObject.squareCollider = self
    def checkCollision(self, otherCollider):
        
        if type(otherCollider)!=SquareCollider:
            otherCollider = otherCollider.getComponent(SquareCollider)
            
        
        pos = (self.gameObject.x+self.offset[0], self.gameObject.y+self.offset[1])
        otherPos = (otherCollider.gameObject.x+otherCollider.offset[0], otherCollider.gameObject.y+otherCollider.offset[1])
        
        [left, right, top, bottom] = [pos[0], pos[0]+self.w, pos[1], pos[1]+self.h]
        [otherLeft, otherRight, otherTop, otherBottom] = [otherPos[0], otherPos[0]+otherCollider.w, otherPos[1], otherPos[1]+otherCollider.h]
        
        
        return (left < otherRight and right > otherLeft and top < otherBottom and bottom > otherTop)

class AnimationHandler(Component):
    def __init__(self, renderer) -> None:
        super().__init__()
        self.frameTimer = 0
        self.loops = 0
        self.currentLoop = 0
        self.renderer = renderer
        self.currentAnimation = Animation([renderer.surface], 1)
        self.defaultAnimation = self.currentAnimation
        
        self.currentAnimationName = "default"
        
        self.animations = {"default": self.defaultAnimation}
    def start(self):
        self.gameObject.animator = self
    def playAnimation(self, animationName, loops=0):
        if animationName in self.animations and animationName!=self.currentAnimationName:
            self.loops = loops
            self.currentLoop = 0
            self.frameTimer = 0
            self.currentAnimation = self.animations[animationName]
            self.currentAnimationName = animationName
    def addAnimation(self, animation, animationName):
        self.animations[animationName] = animation
    def update(self, deltaTime, bonusNum=0):
        frameTimerBefore = self.frameTimer
        self.frameTimer+=(deltaTime*self.currentAnimation.speed)+bonusNum
        if int(self.frameTimer) >= len(self.currentAnimation.frames):
            self.frameTimer = 0
        if int(self.frameTimer)!=frameTimerBefore:
            if self.renderer.flipX or self.renderer.flipY:
                self.renderer.setImage(pygame.transform.flip(self.currentAnimation.frames[int(self.frameTimer)], self.renderer.flipX, self.renderer.flipY))
            else:
                self.renderer.setImage(self.currentAnimation.frames[int(self.frameTimer)])
        
    def getAnimation(self)->str:
        return self.currentAnimationName
        
class Animation(Component):
    def __init__(self, frames, speed=1) -> None:
        super().__init__()
        self.frames = frames
        self.speed=speed