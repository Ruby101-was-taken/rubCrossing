from components import *
from resources import *
from tiles import Tiles
import random
import copy

from sign import sign

class GameObject:
    def __init__(self, x, y, z=0) -> None:
        self.x = x
        self.y = y
        self.z = z
        
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
    def start(self): #start is called after init but before first update, only if game object is created at start of game, unless otherwise made to do so
        for component in self.components:
            component.start()
    def draw(self, win, useCam=True):
        if self.getComponent(Renderer).isVisible:
            self.getComponent(Renderer).draw(win, useCam=useCam)
        
class Test(GameObject):
    def __init__(self, x, y) -> None:
        super().__init__(x, y)
        self.addComponent(Renderer(None))
        self.addComponent(SquareCollider(32, 32))
        
        
class World(GameObject):
    def __init__(self, w=50, h=50, spawnLocation=(64,64)) -> None:
        super().__init__(0,0)
        self.worldSurf = pygame.Surface((w*32, h*32), pygame.SRCALPHA)
        self.spawnLocation = spawnLocation
        allTiles = []
        for y in range(h):
            for x in range(w):
                if y==0 or y==h-1 or x==0 or x==w-1:
                    newTile = Tile(x*32,y*32)
                    newTile.simpleSetTile(Tiles.Wall)
                    allTiles.append(newTile)
                elif y==1 and (x!=0 or x!=w-1):
                    newTile = Tile(x*32,y*32)
                    newTile.simpleSetTile(Tiles.SideWall)
                    allTiles.append(newTile)
        self.allTiles = allTiles
        self.floor = pygame.image.load("resources/tiles/floors/basicWood.png")
        self.w, self.h = w, h
        self.addComponent(Renderer(self.worldSurf))
    def start(self):
        for tile in self.allTiles:
            tile.game = self.game
            tile.isActive = True
        for tile in self.allTiles:
            tile.start()
        self.updateWholeWorld()
        super().start()
    def updateWholeWorld(self):
        for y in range(self.h):
            for x in range(self.w):
                if not x in [0, self.w] and not y in [0,self.h]:
                    self.worldSurf.blit(self.floor, (x*32, y*32))
        for tile in self.allTiles:
            self.updateWorld(tile.x, tile.y)
    def updateWorld(self, x, y):
        for iY in [-1,0,1]:
            for iX in [-1,0,1]:
                if not x+(32*iX) in [0,(32*self.w)] and not y+(32*iY) in [0,(32*self.h)]:
                    self.worldSurf.blit(self.floor, (x+(32*iX), y+(32*iY)))
        for tile in self.allTiles:
            if x+64 > tile.x > x-64 and y+64 > tile.y > y-64:
                tile.draw(self.worldSurf, False)
    
    def getTile(self, x, y):
        for tile in self.allTiles:
            if tile.x == x and tile.y == y:
                return tile
        return Tile(0,0)

    def isTile(self, x, y):
        for tile in self.allTiles:
            if tile.x == x and tile.y == y:
                return True
        return False
    
    def removeTile(self, x, y):
        for tile in self.allTiles:
            if tile.x == x and tile.y == y:
                self.allTiles.remove(tile)
                self.updateWorld(tile.x, tile.y)
                del tile
                
    def update(self, deltaTime):
        for tile in self.allTiles:
            tile.update(deltaTime)
        return super().update(deltaTime)
                
    
    
        
class Tile(GameObject):
    def __init__(self, x, y) -> None:
        super().__init__(x, y)
        self.addComponent(SquareCollider(32, 32))
        self.addComponent(Renderer(colour=(0,0,0,0), alwaysDraw=True))
        self.isSolid = False
        self.canPickUp = False
        self.tileType = None
    def start(self):
        if self.isSolid:
            self.game.world.updateWorld(self.x, self.y)
        super().start()
    def draw(self, win, useCam=True):
        if self.hasComponent(Renderer):
            self.getComponent(Renderer).draw(win, (0, -(self.getComponent(Renderer).surface.get_height()-32)), useCam)
    def setTile(self, tile):
        self.simpleSetTile(tile)
        
        self.game.world.updateWorld(self.x, self.y)
    def simpleSetTile(self, tile):
        if not tile.value.fileName in tileImages:
            tileImages[tile.value.fileName] = pygame.image.load(f"resources/tiles/{tile.value.fileName}.png")
        self.getComponent(Renderer).setImage(tileImages[tile.value.fileName])
        
        self.tileType = tile
        
        self.isSolid =  tile.value.isSolid
        self.canPickUp =  tile.value.canPickUp
        
    def __str__(self) -> str:
        return f"X; {self.x}, Y; {self.y}"
    
class TransportTile(Tile):
    def __init__(self, x, y, worldName="storage") -> None:
        super().__init__(x, y)
        self.worldName = worldName
    def update(self, deltaTime):
        if self.squareCollider.checkCollision(self.game.player):
            self.game.setWorld(self.worldName)
        return super().update(deltaTime)
            
         
class Player(GameObject):
    def __init__(self, x, y) -> None:
        super().__init__(x, y, 2)
        self.speed = 2
        self.addComponent(Renderer(pygame.image.load("resources/player/idle.png")))
        self.addComponent(SquareCollider(20, 28, (5,2)))
        self.heldItem = 0
        self.inventory = Inventory(10)
        self.addComponent(AnimationHandler(self.getComponent(Renderer)))
        
        self.range = pygame.Rect(336,161, 128, 128)
        
        self.prevX, self.prevY = x, y
    def start(self):
        self.game.player = self
        self.game.addGameObject(self.inventory)
        super().start()
        self.animator.addAnimation(Animation([pygame.image.load("resources/player/walk1.png"), pygame.image.load("resources/player/walk2.png"), pygame.image.load("resources/player/walk3.png")], 0.1), "walk")
    def update(self, deltaTime):
        walls = [tile for tile in self.game.world.allTiles if tile.isSolid]
        if not self.game.gameManager.inMenu and not self.game.gameManager.swipe:
            isWalkingSide = False
            if self.game.input.inputEvent("left"):
                self.x -= self.speed*deltaTime
                isWalkingSide = True
                if not self.renderer.flipX:
                    self.renderer.setFlip(True)
            if self.game.input.inputEvent("right"):
                self.x += self.speed*deltaTime
                isWalkingSide = True
                if self.renderer.flipX:
                    self.renderer.setFlip(False)
            
            for wall in walls:
                if wall.getComponent(SquareCollider).checkCollision(self.getComponent(SquareCollider)) and wall:
                    colliding = True
                    if self.game.input.inputEvent("left"):
                        self.x=wall.x+27
                        isWalkingSide = False
                    if self.game.input.inputEvent("right"):
                        self.x=wall.x-25
                        isWalkingSide = False
            
            isWalkingUp = False
            if self.game.input.inputEvent("up"):
                self.y -= self.speed*deltaTime
                isWalkingUp = True
            if self.game.input.inputEvent("down"):
                self.y += self.speed*deltaTime
                isWalkingUp = True
                
            for wall in walls:
                if wall.getComponent(SquareCollider).checkCollision(self.getComponent(SquareCollider)):
                    colliding = True
                    if self.game.input.inputEvent("up"):
                        self.y=wall.y+30
                        isWalkingUp = False
                    if self.game.input.inputEvent("down"):
                        self.y=wall.y-30
                        isWalkingUp = False
            
            if (self.prevX!=self.x or self.prevY!=self.y) and (isWalkingSide or isWalkingUp):
                self.animator.playAnimation("walk", 5)
            else:
                self.animator.playAnimation("default")
                    
            if self.game.input.scrolly != 0:
                self.heldItem += sign(self.game.input.scrolly)
                if self.heldItem >= len(self.inventory.inventory):
                    self.heldItem = 0
                elif self.heldItem < 0:
                    self.heldItem = len(self.inventory.inventory)-1
                        
            if self.game.input.clicked[0] and self.inventory.inventory[self.heldItem] != None and not self.game.input.clickDown[0]:
                self.place()
            elif self.game.input.clicked[0] and self.inventory.inventory[self.heldItem] == None and not self.game.input.clickDown[0]:
                self.pickUp()
        else:
            self.animator.playAnimation("default")

        
        self.prevX, self.prevY = self.x, self.y
        super().update(deltaTime)
    def place(self):
        placeX = int((self.game.input.worldX)/32)   
        placeY = int((self.game.input.worldY)/32)
        # if self.game.world.isTile(placeX*32, placeY*32):
        #     if not self.game.world.getTile(placeX*32, placeY*32).getComponent(SquareCollider).checkCollision(self.getComponent(SquareCollider)):
        #         self.game.world.getTile(placeX*32, placeY*32).setTile(self.inventory[self.heldItem])
        #         #  remove item after place
        #         self.inventory.pop(self.heldItem)
        #         self.heldItem = 0
        # el
        if 0 < placeX < self.game.world.w and 0 < placeY < self.game.world.h and not self.game.world.isTile(placeX*32, placeY*32) and self.range.collidepoint((self.game.input.posx, self.game.input.posy)):
            testCollider = SquareCollider(32, 32)
            testCollider.gameObject = GameObject(placeX*32, placeY*32)
            if not testCollider.checkCollision(self.getComponent(SquareCollider)):
                newTile = Tile(placeX*32, placeY*32)
                newTile.game = self.game
                self.game.world.allTiles.append(newTile)
                newTile.setTile(self.inventory.inventory[self.heldItem])
                #  remove item after place
                self.inventory.inventory.pop(self.heldItem)
                self.heldItem = 0
                self.game.input.clickDown[0] = True
                
    def pickUp(self):
        placeX = int((self.game.input.worldX)/32)   
        placeY = int((self.game.input.worldY)/32)
        if self.game.world.isTile(placeX*32, placeY*32):
            if self.game.world.getTile(placeX*32, placeY*32).canPickUp:
                self.inventory.inventory.append(copy.copy(self.game.world.getTile(placeX*32, placeY*32).tileType))
                self.game.world.removeTile(placeX*32, placeY*32)
                self.game.input.clickDown[0] = True
        # el
        # if 0 < placeX < 50 and 0 < placeY < 50:
        #     if not self.game.world.getTile(placeX*32, placeY*32).getComponent(SquareCollider).checkCollision(self.getComponent(SquareCollider)):
        #         newTile = Tile(placeX*32, placeY*32)
        #         newTile.game = self.game
        #         self.game.world.allTiles.append(newTile)
        #         newTile.setTile(self.inventory[self.heldItem])
        #         #  remove item after place
        #         self.inventory.pop(self.heldItem)
        #         self.heldItem = 0
            
                
class HighLight(GameObject):
    def __init__(self, x, y) -> None:
        super().__init__(x, y)
        highLightSurf = pygame.Surface((32, 32), pygame.SRCALPHA)
        pygame.draw.rect(highLightSurf, (255, 200, 200), pygame.Rect(0,0,32,32), 5, 10)
        self.addComponent(Renderer(highLightSurf))
        self.addComponent(SquareCollider(32, 32))
    def update(self, deltaTime):
        self.x = int((self.game.input.worldX)/32) *32
        self.y = int((self.game.input.worldY)/32) *32
        
        if  0 < self.x/32 < self.game.world.w and 0 < self.y/32 < self.game.world.h:
            if self.getComponent(SquareCollider).checkCollision(self.game.player.getComponent(SquareCollider)) or not self.game.player.range.collidepoint((self.game.input.posx, self.game.input.posy)):
                highLightSurf = pygame.Surface((32, 32), pygame.SRCALPHA)
                pygame.draw.rect(highLightSurf, (255, 0, 0), pygame.Rect(0,0,32,32), 5, 10)
                self.getComponent(Renderer).setImage(highLightSurf)
            else:
                highLightSurf = pygame.Surface((32, 32), pygame.SRCALPHA)
                pygame.draw.rect(highLightSurf, (255, 200, 200), pygame.Rect(0,0,32,32), 5, 10)
                self.getComponent(Renderer).setImage(highLightSurf)
                
        self.getComponent(Renderer).isVisible = (not self.game.gameManager.inMenu) and ((32*self.game.world.w) > self.game.input.worldX > 0 and (32*self.game.world.h) > self.game.input.worldY > 0)
        super().update(deltaTime)
        
        
class Inventory(GameObject):
    def __init__(self, maxCapacity) -> None:
        super().__init__(0, 0)
        self.inventory = [None, Tiles.RatStatue]
        self.maxCapacity = maxCapacity
        self.baseSurf = pygame.image.load("resources/ui/inventory.png")
        self.addComponent(Renderer(self.updateInventory()))
        self.getComponent(Renderer).isVisible = False
    def update(self, deltaTime):
        
        self.x = self.game.camera.x+172
        self.y = self.game.camera.y
        
        if self.game.input.inputEvent("inventory", False) and not self.game.gameManager.swipe:
            self.getComponent(Renderer).setImage(self.updateInventory())
            self.game.gameManager.inInventory = not self.game.gameManager.inInventory
            self.getComponent(Renderer).isVisible = self.game.gameManager.inInventory
            self.game.gameManager.toggleMenuStatus()
            
        super().update(deltaTime)
    
    def updateInventory(self):
        invSurf = copy.copy(self.baseSurf)
        item = 1 if len(self.inventory)>1 else 0
        for y in range(6):
            for x in range(12):
                if self.inventory[item] != None:
                    if not self.inventory[item].value.fileName in tileImages:
                        tileImages[self.inventory[item].value.fileName] = pygame.image.load(f"resources/tiles/{self.inventory[item].value.fileName}.png")
                    invSurf.blit(tileImages[self.inventory[item].value.fileName], (32*x, 32*y))
                item+=1
            
                if item==len(self.inventory):
                    return invSurf 
          


