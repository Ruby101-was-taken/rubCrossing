class GameManger:
    def __init__(self) -> None:
        self.inInventory = False
        self.swipe = False
        
        self.inMenu = False
    
    def toggleMenuStatus(self):
        self.inMenu = not self.inMenu