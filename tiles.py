from enum import Enum

class Door:
    def __init__(self, tpTo) -> None:
        self.tpTo = tpTo
        
class Item:
    def __init__(self, name, fileName, isSolid, canPickUp = True, tp=None) -> None:
        self.name = name
        self.fileName = fileName
        self.isSolid = isSolid
        self.canPickUp = canPickUp

        self.tp = tp
        
class Tiles(Enum):
    Grass = Item("Grass", "grass", False)
    RatStatue = Item("Rat Statue", "ratStatue", True)
    WomanStatue = Item("Woman Statue", "womanStatue", True)
    RockStatue = Item("Rock Statue", "rockStatue", True)
    GooberStatue = Item("Goober Statue", "gooberStatue", True)
    
    Wall = Item("Wall", "wall", True, False)
    SideWall = Item("Side Wall", "sideWall", False, False)
    
    EnterStorageDoor = Item("Storage Door", "door", False, False, Door("storage"))
    EnterShopDoor = Item("Shop Door", "door", False, False, Door("shop"))
    
    # TopWall = Item("Top Wall", "topWall", True, False)
    # RightWall = Item("Right Wall", "rightWall", True, False)
    # LeftWall = Item("Left Wall", "leftWall", True, False)
    # BottomWall = Item("Bottom Wall", "bottomWall", True, False)
    
    # LeftTopWall = Item("Left Top Wall", "leftTopWall", True, False)
    # RightTopWall = Item("Right Top Wall", "rightTopWall", True, False)
    # LeftBottomWall = Item("Bottom Bottom Wall", "leftBottomWall", True, False)
    # RightBottomWall = Item("Left Bottom Wall", "rightBottomWall", True, False)
    