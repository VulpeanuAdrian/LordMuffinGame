from ursina import *
from ursina.prefabs.platformer_controller_2d import PlatformerController2d
from obj.cat_menu import HealthBar, MenuMenu
from obj.enemy import DogEnemy, BirdEnemy, MouseEnemy
from obj.cat_powers import CatBall, CatCoins
# def load_audio(filepath: str, loop=False) -> audio.Audio:
#     a = audio.Audio(sound_file_name=None, loop=False)
#     loaded_sound = app.loader.loadSfx(filepath)
#     a.clip = loaded_sound
#     return a
# speed = 1
#coints_sound=Audio('coint.mp3',loop=False,autoplay=False)
terrain_lengh_size = 5
class FirstLevel(Entity):
    def __init__(self, **kwargs):
        super().__init__()
        self.first_level_sound=Audio('first_level_sounds.mp3',loop=True,autoplay=True)
        self.jump = Audio('assets/jump.mp3',loop=False,autoplay=False)
        #self.coints_sound=Audio('coint.mp3',loop=False,autoplay=False)
        self.death_enemies=[]
        self.mouse_hit_points=5 # final boss life
        self.immortal_muffin=1
        self.switch=1
        self.cat_power_flag=0
        self.bird_speed = 1
        self.dx = 0  # distance enemy moves to 1 direction
        self.size = 13
        self.shrink_health_bar = 2
        self.enemies = []
        self.enemy = DogEnemy(2, -1)
        self.enemies.append(self.enemy)
        self.enemy = DogEnemy(-6, -1)
        self.enemies.append(self.enemy)
        self.enemy=BirdEnemy(-10,5)
        self.enemies.append(self.enemy)
        self.speed=1
        self.size=13
        self.cat_ball_attack=CatBall()
        self.score_counter=0
        self.bg = Entity(model='cube', scale=(self.size, 24), texture='images/image01', z=1)

        self.ground = Entity(model='quad', y=-2, collider='box', color=color.white, scale=(10, 0.7),
                        texture=f'images/brick.jpg')

        self.player = PlatformerController2d(y=4, z=-0.01, scale=(1, 1), color=color.white,
                                        texture=f'images/muffin_02.png')
        self.player.walk_speed = 10
        self.list_of_coints = []
        for i in range(50):
            self.list_of_coints.append(CatCoins(self.player.x + 2 + i, self.ground.y + 1))
        self.cube = Entity(model='quad', x=2, y=3, scale_x=2, collider='box', color=color.white, texture='images/cat_slider')

        self.cat_food = Entity(model='quad', x=2, y=4, scale_x=0.5, color=color.white, texture='images/cat_food1')

        self.wall = Entity(model='quad', scale=(2, 3), x=-3,
                      collider='box', color=color.white, texture='images/cat_tower.png')
        self.level = Entity(model='quad', color=color.white, y=1.3, scale=(3, 1), x=4, collider='box',
                       texture='images/cat_slider')
        self.trap_list = []
        for i in range(1, 5):
            self.trap = Entity(model='quad', scale=(1, 1), x=4 * i // 2 * 5, y=4, collider='box', texture=f'images/trap.png',
                          color=color.green)
            self.trap_list.append(self.trap)

        self.restart_button = Button(color=color.blue, scale=(.15, .1), text='Restart')

        self.restart_button.visible = False
        #self.restart_button.on_click = self.reset
        # Health Bar
        self.full_bar = HealthBar(4, 0, 255, 0, 0)
        self.green_bar = HealthBar(4, -.01, 0, 255, 0)
        for m in range(terrain_lengh_size + 5):
            duplicate(entity=self.bg, x=self.size * (m + 1))
            duplicate(entity=self.bg, x=-self.size * (m + 1))

        for m in range(terrain_lengh_size):
            self.enemy = DogEnemy(2 - 1 + self.size * (m - 1), -1)
            self.enemies.append(self.enemy)
            self.enemy = DogEnemy(2 - 1 - self.size * (m - 1), -1)
            self.enemies.append(self.enemy)
            if m % 2 == 2:
                self.enemy = DogEnemy(-2.5 - 1 + self.size * (m - 1), -1)
                self.enemies.append(self.enemy)
                self.enemy = DogEnemy(-2.5 - 1 - self.size * (m - 1), -1)
                self.enemies.append(self.enemy)

            self.enemy = BirdEnemy(-10 - 1 + self.size * (m - 1), 5)
            self.enemies.append(self.enemy)
            self.enemy = BirdEnemy(-10 - 1 - self.size * (m - 1), 5)
            self.enemies.append(self.enemy)
            duplicate(entity=self.bg, x=self.size * (m + 1))

            duplicate(entity=self.ground, x=self.size * (m + 1))
            duplicate(entity=self.ground, x=-self.size * (m + 1))
            if m % 2 == 1:
                duplicate(entity=self.wall, x=-3 + self.size * (m + 1))
                duplicate(entity=self.wall, x=-3 + self.size * (m + 1))

            duplicate(entity=self.level, x=4 + self.size * (m + 1))
            duplicate(entity=self.level, x=4 - self.size * (m + 1))
            if m % 2 == 0:
                duplicate(entity=self.cube, x=self.size * (m + 1))
                duplicate(entity=self.cube, x=-self.size * (m + 1))
        for i in range(3):
            self.stairs = Entity(model='quad', y=i + i, x=i + self.ground.x + terrain_lengh_size * 14, collider='box',
                            color=color.white,
                            scale=(1, 1),
                            texture=f'images/brick.jpg')
            if i % 5 == 0:
                duplicate(entity=self.bg, x=self.stairs.x, y=self.stairs.y)

        self.up_stairs_ground = Entity(model='quad', y=self.stairs.y, x=self.stairs.x + 17, collider='box', color=color.red,
                                  scale=(30, 0.7),
                                  texture=f'images/brick.jpg')

        self.mouse_enemy = MouseEnemy(y=self.stairs.y + 2, x=self.stairs.x + 8)
        self.enemies.append(self.mouse_enemy)
        switch = 1
        #camera.add_script(SmoothFollow(target=self.player, offset=[0, 1, -30], self.speed=4))
        for key, value in kwargs.items():
            setattr(self, key ,value)
        camera.add_script(SmoothFollow(target=self.player, offset=[0, 1, -30], speed=4))
    def update(self):
        print_on_screen(f'Cube Score: {self.score_counter}', scale=1, position=(-.85, .45), )
        #global  dx, switch, start_range_x_ball_attack, bird_speed, cat_power_flag, mouse_hit_points, start
        for coint in self.list_of_coints:
            if abs(self.player.x - coint.x) <= 1 and abs(self.player.y - coint.y) <= 1:
                self.score_counter += 10
                coint.visible = False
                self.list_of_coints.remove(coint)
                #coints_sound.play()

        if abs(self.player.x - self.cat_food.x) <= 1 and abs(self.player.y - self.cat_food.y) <= 1:
            self.cat_power_flag = 1
            self.cat_food.visible = False


        self.full_bar.x = camera.x - self.size // 1.5  # size is the width of the background image
        self.full_bar.y = camera.y + 4
        self.green_bar.x = self.full_bar.x
        self.green_bar.y = self.full_bar.y
        if (self.player.right[0] == 1.0):
            self.cat_ball_attack.x += 0.10
        else:
            self.cat_ball_attack.x -= 0.10  # if the player is in left position it should  attack in left with a ball

        # final boss movement

        if self.switch == 1:
            self.dx += self.speed * time.dt
            if abs(self.dx) > 2:
                self.speed *= -1
                self.bird_speed *= -1
                dx = 0

            self.mouse_enemy.x += self.speed * time.dt
            # check for collision with enemy
            for enemy in self.enemies:
                enemy.x += self.speed * time.dt
                if type(enemy) is BirdEnemy:
                    enemy.x += 0.01
                    enemy.x += self.bird_speed * time.dt
                if abs(self.player.x - enemy.x) < 1 and abs(self.player.y - enemy.y) < 1 and self.immortal_muffin == 0:
                    self.player.rotation_z = 90
                    switch = 0
                    self.green_bar.scale_x = 0

                if isinstance(enemy, MouseEnemy) is False:
                    if abs(self.cat_ball_attack.x - enemy.x) < 1 and abs(self.cat_ball_attack.y - enemy.y) < 1:
                        self.death_enemies.append(enemy)
                        enemy.visible = False
                        self.enemies.remove(enemy)
                        self.score_counter += 1

                else:
                    if abs(self.cat_ball_attack.x - enemy.x) < 5 and abs(self.cat_ball_attack.y - enemy.y) < 5:
                        self.mouse_hit_points -= 1
                        # destroy(cat_ball_attack)  # todo fix this also try  to make the mouse invisible for 0.5 sec when hit
                        if self.mouse_hit_points < 1:
                            enemy.visible = False
                            # enemies.remove(enemy)
                            self.score_counter += 50

        # check for collision in traps
        for trap in self.trap_list:
            dis = abs(self.player.x - trap.x)
            if dis <= 0.1:  # todo: works currently only for X axes
                self.player.color = color.red
                # loose health
                self.green_bar.scale_x -= self.shrink_health_bar * time.dt
                if self.green_bar.scale_x < 0.1 and self.immortal_muffin == 0:
                    self.player.rotation_z = 90
                    switch = 0
            else:
                self.player.color = color.white

        if self.switch == 0:
            self.restart_button.visible = True
        if held_keys['q'] or held_keys['escape']:
            quit()
        # if player.y <= -8:
        #     quit()q

        if self.cat_power_flag == 1:
            if held_keys['r']:
                self.cat_ball_attack.attack(self.player.x, self.player.y + 0.5)
                self.cat_ball_attack.visible = True

        if abs(self.cat_ball_attack.x) > abs(self.cat_ball_attack.x) + 5:  #todo: fix this
            self.cat_ball_attack.visible = False  # can not destroy the bullet due to library error
            self.cat_ball_attack.y = -3
            self.cat_ball_attack.x = -3

        # in case you are stuck
        if held_keys['y']:  # in case player stuck
            self.player.y += 1
            self.player.x += 1

    def input(self,key):
        if key == 'space':
            if not self.jump.playing:
                self.jump.play()
            self.player.texture='muffin_jump.png'
            self.player.jump()
        if self.player.jumping is False:
            self.player.texture='muffin_02.png'