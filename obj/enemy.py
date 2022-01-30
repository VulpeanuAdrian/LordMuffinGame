from ursina import Entity
from ursina import color
import time

class DogEnemy(Entity):
    def __init__(self,x,y):
        super().__init__()
        self.model='quad'
        self.color=color.white
        self.texture='images/dog.png'
        self.x=x
        self.y=y
        #self.collider='box'
        self.scale=(2,2)

class BirdEnemy(Entity):
    def __init__(self,x,y):
        super().__init__()
        self.model='quad'
        self.color=color.white
        self.texture='images/eagle.png'
        self.x=x
        self.y=y
        #self.collider='box'
        self.scale=(2,2)


class MouseEnemy(Entity):
    def __init__(self,x,y):
        super().__init__()
        self.model='quad'
        self.color=color.white
        self.texture='images/evil_mouse.png'
        self.x=x
        self.y=y
        self.collider='box'
        self.scale=(5,5)
        self.cheese_attack=Entity(model='quad',x=self.x-1.5,y=self.y-1.5,scale=1,texture='images/cheese_attack.png')
        #self.cheese_attack.x-=10









