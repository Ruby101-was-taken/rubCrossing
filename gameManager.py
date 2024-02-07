class GameManger:
    def __init__(self) -> None:
        self.inInventory = False
        self.swipe = False
        
        self.inMenu = False
        self.inShop = False
    
    def toggleMenuStatus(self):
        self.inMenu = not self.inMenu
        
    def toggleShopStatus(self):
        self.toggleMenuStatus()
        self.inShop = not self.inShop