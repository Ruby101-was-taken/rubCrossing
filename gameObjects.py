from components import *
import random

class GameObject:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        
        self.isActive = True
        
        self.components = []
    def addComponent(self, component):
        component.gameObject = self
        self.components.append(component)
    def getComponent(self, componentType):
        for component in self.components:
            if type(component) == componentType:
                return component
        return None
    def hasComponent(self, componentType):
        for component in self.components:
            if type(component) == componentType:
                return True
        return False
    def update(self, deltaTime):
        for component in self.components:
            component.update(deltaTime)
    def start(self): #start is called after init but before first update
        pass
    def draw(self, win):
        if self.hasComponent(Renderer):
            self.getComponent(Renderer).draw(win)
        
class Test(GameObject):
    def __init__(self, x, y) -> None:
        super().__init__(x, y)
        self.addComponent(Renderer(None))
        self.addComponent(SquareCollider(32, 32))
        
        
class World(GameObject):
    def __init__(self, allTiles) -> None:
        super().__init__(0,0)
        self.worldSurf = pygame.Surface((1600, 1600), pygame.SRCALPHA)
        self.allTiles = allTiles
        for tile in self.allTiles:
            tile.draw(self.worldSurf)
        self.addComponent(Renderer(self.worldSurf))
    def start(self):
        self.game.world = self
        
class Tile(GameObject):
    def __init__(self, x, y) -> None:
        super().__init__(x, y)
        self.addComponent(SquareCollider(32, 32))
        self.isSolid = random.choice([True, False, False, False, False, False, False])
        self.addComponent(Renderer(colour=(random.randint(155, 255),0 if not self.isSolid else 255,0 if not self.isSolid else 255)))

class Player(GameObject):
    def __init__(self, x, y) -> None:
        super().__init__(x, y)
        self.speed = 2
        self.addComponent(Renderer(pygame.image.load("player.png")))
        self.addComponent(SquareCollider(32, 32))
    def update(self, deltaTime):
        walls = [tile for tile in self.game.world.allTiles if tile.isSolid]
        if self.game.input.inputEvent("left"):
            self.x -= self.speed*deltaTime
        if self.game.input.inputEvent("right"):
            self.x += self.speed*deltaTime
        
        for wall in walls:
            if wall.getComponent(SquareCollider).checkCollision(self.getComponent(SquareCollider)) and wall:
                colliding = True
                if self.game.input.inputEvent("left"):
                    self.x=wall.x+32
                if self.game.input.inputEvent("right"):
                    self.x=wall.x-32
            
        if self.game.input.inputEvent("up"):
            self.y -= self.speed*deltaTime
        if self.game.input.inputEvent("down"):
            self.y += self.speed*deltaTime
            
        for wall in walls:
            if wall.getComponent(SquareCollider).checkCollision(self.getComponent(SquareCollider)):
                colliding = True
                if self.game.input.inputEvent("up"):
                    self.y=wall.y+32
                if self.game.input.inputEvent("down"):
                    self.y=wall.y-32
        
        
        super().update(deltaTime)