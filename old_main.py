from ursina import *
from ursina.prefabs.platformer_controller_2d import PlatformerController2d

import random
from obj.cat_menu import HealthBar, MenuMenu
from obj.enemy import DogEnemy, BirdEnemy, MouseEnemy
from obj.cat_powers import CatBall, CatCoins

x = random.randint(-10, 10)
death_enemies = []  # list with death dog enemis(created in order to restore them after pressing restart)
score_counter = 0
immortal_muffin = 1  # for dev purpose muffin is immortal value 1 = immortal
start_range_x_ball_attack = 0
cat_power_flag = 0
mouse_hit_points = 5


# def show_menu():
#     play = Button('Play', on_click=first_level, scale=(0.4, 0.4), x=0, y=0)


def reset():
    global switch, enemies, immortal_muffin, score_counter, cat_power_flag
    score_counter = 0
    player.rotation_z = 0
    cat_power_flag = 0
    cat_food.visible = True
    player.x = 0
    green_bar.scale_x = 5
    switch = 1
    restart_button.visible = False
    for enemy in death_enemies:
        enemy.visible = True  # set the visible to true for death enemies(when they die visible becomes false..
    enemies += death_enemies  # add death enemies to the new list when they are revived(after restart button is presset)
    immortal_muffin = 1
    invoke(reset_to_immortal, delay=5)


def reset_to_immortal():
    global immortal_muffin
    immortal_muffin = 0


def load_audio(filepath: str, loop=False) -> audio.Audio:
    a = audio.Audio(sound_file_name=None, loop=False)
    loaded_sound = app.loader.loadSfx(filepath)
    a.clip = loaded_sound
    return a


def update():
    global speed, dx, switch, start_range_x_ball_attack, score_counter, bird_speed, cat_ball_attack, cat_power_flag, mouse_hit_points, start

    for coint in list_of_coints:
        if abs(player.x - coint.x) <= 1 and abs(player.y - coint.y) <= 1:
            score_counter += 10
            coint.visible = False
            list_of_coints.remove(coint)
            load_audio(os.path.join('', 'assets', 'coint.mp3')).play()

    if abs(player.x - cat_food.x) <= 1 and abs(player.y - cat_food.y) <= 1:
        cat_power_flag = 1
        cat_food.visible = False
    print_on_screen(f'Cube Score: {score_counter}', scale=1, position=(-.85, .45), )

    full_bar.x = camera.x - size // 1.5  # size is the width of the background image
    full_bar.y = camera.y + 4
    green_bar.x = full_bar.x
    green_bar.y = full_bar.y
    if (player.right[0] == 1.0):
        cat_ball_attack.x += 0.10
    else:
        cat_ball_attack.x -= 0.10  # if the player is in left position it should  attack in left with a ball

    # final boss movement

    if switch == 1:
        dx += speed * time.dt
        if abs(dx) > 2:
            speed *= -1
            bird_speed *= -1
            dx = 0

        mouse_enemy.x += speed * time.dt
        # check for collision with enemy
        for enemy in enemies:
            enemy.x += speed * time.dt
            if type(enemy) is BirdEnemy:
                enemy.x += 0.01
                enemy.x += bird_speed * time.dt
            if abs(player.x - enemy.x) < 1 and abs(player.y - enemy.y) < 1 and immortal_muffin == 0:
                player.rotation_z = 90
                switch = 0
                green_bar.scale_x = 0

            if isinstance(enemy, MouseEnemy) is False:
                if abs(cat_ball_attack.x - enemy.x) < 1 and abs(cat_ball_attack.y - enemy.y) < 1:
                    death_enemies.append(enemy)
                    enemy.visible = False
                    enemies.remove(enemy)
                    score_counter += 1

            else:
                if abs(cat_ball_attack.x - enemy.x) < 5 and abs(cat_ball_attack.y - enemy.y) < 5:
                    mouse_hit_points -= 1
                    # destroy(cat_ball_attack)  # todo fix this also try  to make the mouse invisible for 0.5 sec when hit
                    print('Mouse hit points ', mouse_hit_points)
                    if mouse_hit_points < 1:
                        enemy.visible = False
                        # enemies.remove(enemy)
                        score_counter += 50

    # check for collision in traps
    for trap in trap_list:
        dis = abs(player.x - trap.x)
        if dis <= 0.1:  # todo: works currently only for X axes
            player.color = color.red
            # loose health
            green_bar.scale_x -= shrink_health_bar * time.dt
            if green_bar.scale_x < 0.1 and immortal_muffin == 0:
                player.rotation_z = 90
                switch = 0
        else:
            player.color = color.white
        print("player x is ", player.x)
        print("trap  is ", trap.x)
    if switch == 0:
        restart_button.visible = True
    if held_keys['q'] or held_keys['escape']:
        quit()
    # if player.y <= -8:
    #     quit()q

    if held_keys['space']:
        player.jump()
        load_audio(os.path.join('', 'assets', 'jump.mp3')).play()

    if cat_power_flag == 1:
        if held_keys['r']:
            cat_ball_attack.attack(player.x, player.y + 0.5)
            cat_ball_attack.visible = True
            start_range_x_ball_attack = cat_ball_attack.x

    if abs(cat_ball_attack.x) > start_range_x_ball_attack + 5:
        cat_ball_attack.visible = False  # can not destroy the bullet due to library error
        cat_ball_attack.y = -3
        cat_ball_attack.x = -3

    # in case you are stuck
    if held_keys['y']:  # in case player stuck
        player.y += 1
        player.x += 1


app = Ursina()
cat_ball_attack = CatBall()

load_audio(os.path.join('', 'assets', 'first_level_sounds.mp3')).play()

speed = 1
bird_speed = 1
dx = 0  # distance enemy moves to 1 direction
size = 13
shrink_health_bar = 2
enemies = []
enemy = DogEnemy(2, -1)
enemies.append(enemy)
enemy = DogEnemy(-6, -1)
enemies.append(enemy)
# enemy=BirdEnemy(-10,5)
# enemies.append(enemy)

terrain_lengh_size = 5
window.fullscreen = True
bg = Entity(model='cube', scale=(size, 24), texture='images/image01', z=1)
print(bg.y)

ground = Entity(model='quad', y=-2, collider='box', color=color.white, scale=(10, 0.7),
                texture=f'images/brick.jpg')

player = PlatformerController2d(y=ground.y + 22, z=-0.01, scale=(1, 1), color=color.white,
                                texture=f'images/muffin_02.png')
player.walk_speed = 10
list_of_coints = []
for i in range(50):
    list_of_coints.append(CatCoins(player.x + 2 + i, ground.y + 1))
cube = Entity(model='quad', x=2, y=3, scale_x=2, collider='box', color=color.white, texture='images/cat_slider')

cat_food = Entity(model='quad', x=2, y=4, scale_x=0.5, color=color.white, texture='images/cat_food1')

wall = Entity(model='quad', scale=(2, 3), x=-3,
              collider='box', color=color.white, texture='images/cat_tower.png')
level = Entity(model='quad', color=color.white, y=1.3, scale=(3, 1), x=4, collider='box',
               texture='images/cat_slider')
trap_list = []
for i in range(1, 5):
    trap = Entity(model='quad', scale=(1, 1), x=4 * i // 2 * 5, y=4, collider='box', texture=f'images/trap.png',
                  color=color.green)
    trap_list.append(trap)

restart_button = Button(color=color.blue, scale=(.15, .1), text='Restart')

restart_button.visible = False
restart_button.on_click = reset
# Health Bar
full_bar = HealthBar(4, 0, 255, 0, 0)
green_bar = HealthBar(4, -.01, 0, 255, 0)
for m in range(terrain_lengh_size + 5):
    duplicate(entity=bg, x=size * (m + 1))
for m in range(terrain_lengh_size):
    enemy = DogEnemy(2 - 1 + size * (m - 1), -1)
    enemies.append(enemy)
    enemy = DogEnemy(2 - 1 - size * (m - 1), -1)
    enemies.append(enemy)
    if m % 2 == 2:
        enemy = DogEnemy(-2.5 - 1 + size * (m - 1), -1)
        enemies.append(enemy)
        enemy = DogEnemy(-2.5 - 1 - size * (m - 1), -1)
        enemies.append(enemy)

    enemy = BirdEnemy(-10 - 1 + size * (m - 1), 5)
    enemies.append(enemy)
    enemy = BirdEnemy(-10 - 1 - size * (m - 1), 5)
    enemies.append(enemy)
    duplicate(entity=bg, x=size * (m + 1))
    duplicate(entity=bg, x=-size * (m + 1))

    duplicate(entity=ground, x=size * (m + 1))
    duplicate(entity=ground, x=-size * (m + 1))
    if m % 2 == 1:
        duplicate(entity=wall, x=-3 + size * (m + 1))
        duplicate(entity=wall, x=-3 + size * (m + 1))

    duplicate(entity=level, x=4 + size * (m + 1))
    duplicate(entity=level, x=4 - size * (m + 1))
    if m % 2 == 0:
        duplicate(entity=cube, x=size * (m + 1))
        duplicate(entity=cube, x=-size * (m + 1))
for i in range(3):
    stairs = Entity(model='quad', y=i + i, x=i + ground.x + terrain_lengh_size * 14, collider='box',
                    color=color.white,
                    scale=(1, 1),
                    texture=f'images/brick.jpg')
    if i % 5 == 0:
        duplicate(entity=bg, x=stairs.x, y=stairs.y)

up_stairs_ground = Entity(model='quad', y=stairs.y, x=stairs.x + 17, collider='box', color=color.red,
                          scale=(30, 0.7),
                          texture=f'images/brick.jpg')

mouse_enemy = MouseEnemy(y=stairs.y + 2, x=stairs.x + 8)
enemies.append(mouse_enemy)
switch = 1
camera.add_script(SmoothFollow(target=player, offset=[0, 1, -30], speed=4))

app.run()

# if __name__ == '__main__':
#     app = Ursina()
#     show_menu()
#     app = app.run()
