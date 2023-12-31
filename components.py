import pygame

class Component:
    def __init__(self) -> None:
        pass
    def update(self, deltaTime):
        pass

class Renderer(Component):
    def __init__(self, image=None, w=32, h=32, colour=(0,0,255)) -> None:
        super().__init__()
        self.surface = pygame.Surface((w, h))
        if image == None:
            self.surface.fill(colour)
            self.w = w
            self.h = h
        else:
            self.surface = image
            self.w = image.get_width()
            self.h = image.get_height()
            
        self.isVisible = True
    def draw(self, win):
        if self.gameObject.game.camera.lockOn != self.gameObject:
            win.blit(self.surface, (self.gameObject.x-self.gameObject.game.camera.x, self.gameObject.y-self.gameObject.game.camera.y))
        else:
            win.blit(self.surface, (400-self.w/2, 225-self.h/2))
    
    def update(self, deltaTime):
        x = self.gameObject.x-self.gameObject.game.camera.x
        y = self.gameObject.y-self.gameObject.game.camera.y
        
        self.isVisible = -self.w < x < 800 and -self.h < y < 450  
        

class SquareCollider(Component):
    def __init__(self, w:int, h:int) -> None:
        super().__init__()
        self.w = w
        self.h = h
    def checkCollision(self, otherCollider):
        pos = (self.gameObject.x, self.gameObject.y)
        otherPos = (otherCollider.gameObject.x, otherCollider.gameObject.y)
        
        [left, right, top, bottom] = [pos[0], pos[0]+self.w, pos[1], pos[1]+self.h]
        [otherLeft, otherRight, otherTop, otherBottom] = [otherPos[0], otherPos[0]+otherCollider.w, otherPos[1], otherPos[1]+otherCollider.h]
        
        
        return (left < otherRight and right > otherLeft and top < otherBottom and bottom > otherTop)
