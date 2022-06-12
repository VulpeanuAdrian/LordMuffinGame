from ursina import Entity
from ursina import color
from ursina import destroy
import time


class DogEnemy(Entity):
    def __init__(self, x, y):
        super().__init__()
        self.model = 'quad'
        self.color = color.white
        self.texture = 'images/dog.png'
        self.x = x
        self.y = y
        # self.collider='box'
        self.scale = (2, 2)


class BirdEnemy(Entity):
    def __init__(self, x, y):
        super().__init__()
        self.model = 'quad'
        self.color = color.white
        self.texture = 'images/eagle.png'
        self.x = x
        self.y = y
        # self.collider='box'
        self.scale = (2, 2)


class MouseEnemy(Entity):
    def __init__(self, x, y):
        super().__init__()
        self.model = 'quad'
        self.color = color.white
        self.texture = 'images/evil_mouse.png'
        self.x = x
        self.y = y
        self.collider = 'box'
        self.scale = (5, 5)
        self.cheese_attack = Entity(model='quad', x=self.x - 1.5, y=self.y - 1.5, scale=1,
                                    texture='images/cheese_attack.png')
        # self.cheese_attack.x-=10

    def update(self):
        if self.visible == True:
            self.cheese_attack
            self.cheese_attack.x -= 0.10
            if self.cheese_attack.x + 10 < self.x:
                self.cheese_attack.x = self.x
        # else:
        #     destroy(self.cheese_attack)


class RattonEnemy(Entity):
    def __init__(self, x, y):
        super().__init__()
        self.model = 'quad'
        self.color = color.white
        self.texture = 'images/raccon.png'
        self.x = x
        self.y = y
        # self.collider='box'
        self.scale = (1.5, 1.5)
        self.raccon_attack = Entity(model='quad', x=self.x - 1.5, y=self.y, scale=0.8, texture='images/smell.png',
                                    color=color.green)

    def update(self):
        if self.visible:
            left_attack = self.raccon_attack
            up_attack = self.raccon_attack
            up_attack.y += 0.10
            left_attack.x -= 0.10
            if left_attack.x + 5 < self.x or up_attack.y > self.y + 5:
                left_attack.x = self.x
                up_attack.y = self.y
        else:
            self.raccon_attack.visible = False


class OrangeSlime(Entity):
    def __init__(self, x, y):
        super().__init__()
        self.model = 'quad'
        self.color = color.white
        self.texture = 'images/orange_slime.png'
        self.x = x
        self.y = y
        # self.collider='box'
        self.scale = (1.5, 1.5)
        self.slime_attack = Entity(model='circle', x=self.x - 1.5, y=self.y, scale=0.8,
                                   color=color.orange)

    def update(self):
        if self.visible == True:
            left_attack = self.slime_attack
            up_attack = self.slime_attack
            left_attack.x -= 0.10
            if left_attack.x + 5 < self.x or up_attack.y > self.y + 5:
                left_attack.x = self.x
                up_attack.y = self.y
        else:
            # destroy(self.slime_attack)
            self.raccon_attack.visible = False
        # TODO refactor with destroy


class CatFireTower(Entity):
    def __init__(self, x, y):
        super().__init__()
        self.model = 'quad'
        self.color = color.white
        self.texture = 'images/cat_fire_tower.png'
        self.x = x
        self.y = y
        self.collider = 'box'
        self.scale = (2, 4)
        self.fire_tower_attack = Entity(model='quad', x=self.x - 1.5, y=y, scale=(2, 1.5), texture='arrow_right',
                                        color=color.red)

    def update(self):
        self.fire_tower_attack.x -= 0.05
        if self.fire_tower_attack.x + 10 < self.x:
            self.fire_tower_attack.x = self.x
