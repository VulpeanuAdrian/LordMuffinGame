from ursina import Entity,Animation,camera,Sprite
import time
from ursina import color

class HealthBar(Entity):
    def __init__(self,y,z,r,g,b):
        super().__init__()
        self.model='quad'
        self.scale=(5,0.5)
        self.color=color.rgb(r,g,b)
        self.y=y
        self.z=z
        self.origin=(-.5,-.5)

class MenuMenu(Entity):
    def __init__(self, **kwargs):
        super().__init__(parent=camera.ui, ignore_paused=True)
        #x = Animation('/lisa.gif', fps=30, loop=False, autoplay=True, duration=13)
        #x.start()
        #time.sleep(13)
        self.main_menu = Entity(parent=self, enabled=True,color=color.blue)
        self.options_menu = Entity(parent=self, enabled=False)
        self.help_menu = Entity(parent=self, enabled=False)
        self.background1 = Animation('/images/lisa.gif', fps=60, loop=True, autoplay=True)
        self.background = Sprite(self.background1, z=1)