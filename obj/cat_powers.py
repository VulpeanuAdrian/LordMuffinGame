from ursina import Entity
from ursina import color
from ursina import destroy
import time

class CatBall(Entity):
    def __init__(self,x=0,y=0):
        super().__init__()
        self.model='quad'
        self.color=color.white
        self.texture='images/cat_ball.png'
        self.x=x
        self.y=y
        self.visible=False
        self.scale=(0.5,0.5)

    def attack(self,player):
        self.x=player.x
        self.y=player.y+0.5




list_of_coints=[]
class CatCoins(Entity):
    def __init__(self,x,y=-1):
        super().__init__()

        self.model='quad'
        self.color=color.white
        self.texture='images/cat_coin.png'
        self.x=x
        self.y=y
        self.scale=(0.5,0.5)
        global list_of_coints



    def create_coints(self,number_of_coins):
        for i in range(number_of_coins):
            CatCoins(i)
            list_of_coints.append(CatCoins(i))
        return list_of_coints

    def enable(self,player):
        if abs(player.x-self.x) <=5:
                self.enabled=False


