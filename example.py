from ursina import *

app = Ursina()

player = Entity(model='circle', color=color.orange, scale_y=2)

def update():   # update gets automatically called.
    player.x += held_keys['d'] * .1
    player.x -= held_keys['a'] * .1

app.run() 