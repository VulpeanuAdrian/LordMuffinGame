from ursina import *
from ursina.prefabs.platformer_controller_2d import PlatformerController2d
from obj.cat_menu import HealthBar, MenuMenu
from obj.enemy import DogEnemy, BirdEnemy, MouseEnemy, RattonEnemy, CatFireTower, OrangeSlime
from obj.cat_powers import CatBall, CatCoins
from levels.second_level import SecondLevel

from ursina import print_on_screen

# def load_audio(filepath: str, loop=False) -> audio.Audio:
#     a = audio.Audio(sound_file_name=None, loop=False)
#     loaded_sound = app.loader.loadSfx(filepath)
#     a.clip = loaded_sound
#     return a
# speed = 1
# coints_sound=Audio('coint.mp3',loop=False,autoplay=False)
terrain_lengh_size = 5


class FirstLevel(Entity):
    def __init__(self, **kwargs):
        super().__init__()
        self.finish_level = False
        self.first_level_sound = Audio('platformer_level04_loop.ogg', loop=True, autoplay=True)
        self.jump = Audio('../assets/jump.mp3', loop=False, autoplay=False)
        self.coints_sound = Audio('coint.mp3', loop=False, autoplay=False)
        self.pause_handler = Entity(ignore_paused=True)
        self.pause_text = Text('PAUSE', origin=(0, 0), scale=2,
                               enabled=False,color=color.yellow)
        # Assign the input function to the pause handler.
        self.death_enemies = []
        self.mouse_hit_points = 6  # final boss life = equal with 5 hits
        self.immortal_muffin = 0
        self.switch = 1
        self.cat_power_flag = 0
        self.bird_speed = 1
        self.dx = 0  # distance enemy moves to 1 direction
        self.size = 13
        self.shrink_health_bar = 2
        self.enemies = []
        self.enemy = DogEnemy(2, -2)
        self.enemies.append(self.enemy)
        self.enemy = DogEnemy(-6, -2)
        self.enemies.append(self.enemy)
        self.enemy = BirdEnemy(-10, 4.5)
        self.enemies.append(self.enemy)
        self.speed = 1
        self.size = 13
        self.cat_ball_attack = CatBall()
        self.score_counter = 0
        self.full_bar = 10
        ground_coordonates = []
        self.checkpoint_list = []
        self.bg = Entity(model='cube', y=15.8, scale=(self.size, 45), texture='images/forest_bg', z=1)

        self.cloud_background = Entity(model='cube', x=170, scale=(200, 50), texture='images/background_0', z=1)

        self.ground = Entity(model='quad', y=-5, collider='box', color=color.white, scale=(10, 5),
                             texture=f'images/grass.png')

        self.player = PlatformerController2d(y=22, x=0, scale=(1, 1, 0.01 / 2), color=color.white,  # for dev use x=99
                                             texture=f'images/muffin_02.png', )
        # print("player model",self.player.model)
        self.restart_coord = (5, 22)
        self.player.walk_speed = 10
        self.list_of_coins = []

        self.cube = Entity(model='quad', x=2, y=3, scale_x=2, collider='box', color=color.white,
                           texture='images/low_slider')
        ground_coordonates.append([self.cube.x + 1, self.cube.y + 1])
        self.cat_food = Entity(model='quad', x=2, y=4, scale_x=0.5, color=color.white, texture='images/cat_food1')
        self.cat_food_2 = Entity(model='quad', x=72, y=8, scale_x=0.5, color=color.white, texture='images/cat_food1')

        self.wall = Entity(model='quad', y=-0.5, x=-3, scale=(2.5, 2.5),
                           collider='box', color=color.white, texture='images/slider.png')
        ground_coordonates.append([self.wall.x, self.wall.y + 5])

        self.level = Entity(model='quad', color=color.white, y=1.3, scale=(3, 1), x=4, collider='box',
                            texture='images/platform_1')
        ground_coordonates.append([self.level.x + 3, self.level.y + 3])

        self.trap_list = []
        for i in range(1, 5):
            self.trap = Entity(model='quad', scale=(1, 1), x=4 * i // 2 * 5, y=4, collider='box',
                               texture=f'images/poison_plant.png',
                               color=color.green)
            self.trap_list.append(self.trap)

        self.restart_button = Button(color=color.blue, scale=(.15, .1), text='Restart', visible=False,
                                     on_click=self.reset)

        # Health Bar
        self.full_bar = HealthBar(4, 0, 255, 0, 0)
        self.green_bar = HealthBar(4, -.01, 0, 255, 0)
        text = Text(text='Health', scale=2, position=(-.75, .34), origin=(0, 0), color=color.yellow,
                    background=False)
        for m in range(terrain_lengh_size + 2):
            duplicate(entity=self.bg, x=self.size * (m + 1))
            if i % 2 == 1:
                duplicate(entity=self.bg, x=self.size * (m + 1), texture='images/second_forest_bg')

        for m in range(terrain_lengh_size):
            self.enemy = DogEnemy(2 - 1 + self.size * (m - 1), -2)
            self.enemies.append(self.enemy)
            self.enemy = DogEnemy(2 - 1 - self.size * (m - 1), -2)
            self.enemies.append(self.enemy)
            if m % 2 == 2:
                self.enemy = DogEnemy(-2.5 - 1 + self.size * (m - 1), -2)
                self.enemies.append(self.enemy)
                self.enemy = DogEnemy(-2.5 - 1 - self.size * (m - 1), -2)
                self.enemies.append(self.enemy)

            self.enemy = BirdEnemy(-10 - 1 + self.size * (m - 1), 4.5)
            self.enemies.append(self.enemy)
            self.enemy = BirdEnemy(-10 - 1 - self.size * (m - 1), 4.5)
            self.enemies.append(self.enemy)
            # duplicate(entity=self.bg, x=self.size * (m + 1))

            duplicate(entity=self.ground, x=self.size * (m + 1))
            duplicate(entity=self.ground, x=-self.size * (m + 1))
            if m % 2 == 1:
                duplicate(entity=self.wall, x=-3 + self.size * (m + 1))
                duplicate(entity=self.wall, x=-3 + self.size * (m + 1))
                ground_coordonates.append([self.wall.x + self.size * (m + 1), self.wall.y + 5])

            duplicate(entity=self.level, x=4 + self.size * (m + 1))
            duplicate(entity=self.level, x=4 - self.size * (m + 1))
            ground_coordonates.append([self.level.x + self.size * (m + 1), self.level.y + 1])

            if m % 2 == 0:
                duplicate(entity=self.cube, x=self.size * (m + 1))
                duplicate(entity=self.cube, x=-self.size * (m + 1))
        for i in range(2):
            self.stairs = Entity(model='quad', y=i + i, x=i + self.ground.x + terrain_lengh_size * 14, collider='box',
                                 color=color.white,
                                 scale=(1, 1),
                                 texture=f'images/grass.png')

            self.cat_food_stair = Entity(model='quad', y=4, x=72, collider='box',
                                         color=color.white,
                                         scale=(1, 1),
                                         texture=f'images/grass.png')

            # if i % 5 == 0:
            #     duplicate(entity=self.bg, x=self.stairs.x, y=self.stairs.y)

        self.up_stairs_ground = Entity(model='quad', y=self.stairs.y, x=self.stairs.x + 10, collider='box',
                                       color=color.white,
                                       scale=(15, 1),
                                       texture=f'images/grass.png')

        self.mouse_enemy = MouseEnemy(y=self.stairs.y + 2.5, x=self.stairs.x + 10)

        for i in range(6):
            self.stairs = Entity(model='quad', y=self.up_stairs_ground.y + i, x=i + self.up_stairs_ground.x + 5 + i,
                                 collider='box',
                                 color=color.white,
                                 scale=(0.8, 1),
                                 texture=f'images/cloud.png')

        self.cloud_stair = Entity(model='quad', y=self.stairs.y - 3, x=i + self.up_stairs_ground.x + 17, collider='box',
                                  color=color.white,
                                  scale=(10, 5),
                                  texture=f'images/cloud.png')

        self.cat_fire_tower = CatFireTower(x=self.cloud_stair.x, y=self.cloud_stair.y + 4)
        for i in range(1, 4):
            duplicate(entity=self.cloud_stair, x=self.cloud_stair.x + 13 * i)
            self.enemies.append(RattonEnemy(x=self.cloud_stair.x + 13 * i, y=self.cloud_stair.y + 3))
        # duplicate(entity=self.cat_fire_towerx=self.cloud_stair.x+10*i)

        self.cloud_ground = Entity(model='quad', y=self.stairs.y - 3, x=self.up_stairs_ground.x + 75, collider='box',
                                   color=color.white,
                                   scale=(10, 2),
                                   texture=f'images/second_ground.png', collision=True)
        for i in range(1, 90):
            duplicate(entity=self.cloud_ground, x=self.cloud_ground.x + 13 * i)
            if i%10 == 0:
                duplicate(entity=self.cloud_ground,x=self.cloud_ground.x+10,y=self.stairs.y-3)
            self.enemies.append(OrangeSlime(x=self.cloud_ground.x + 13 * i, y=self.cloud_ground.y + 1.5))

        for i in range(10):
            ground_coordonates.append([self.mouse_enemy.x + i, self.mouse_enemy.y - 1.3])

        self.enemies.append(self.mouse_enemy)
        # for key, value in kwargs.items():
        #     setattr(self, key, value)
        camera.add_script(SmoothFollow(target=self.player, offset=[0, 1, -30], speed=4))
        print(ground_coordonates)
        for i in range(len(ground_coordonates)):
            self.list_of_coins.append(CatCoins(ground_coordonates[i][0], ground_coordonates[i][1]))

        checkpoint_coordonates_list = [(-1.5, 40), (3.5, 84)]
        for checkpoint_cord in range(len(checkpoint_coordonates_list)):  # checkpoints
            self.checkpoint_list.append(Entity(model='quad', y=checkpoint_coordonates_list[checkpoint_cord][0],
                                               x=checkpoint_coordonates_list[checkpoint_cord][1], scale=(2, 2),
                                               texture='images/checkpoint'))

    def restart_logic(self):
        if self.player.y < -5:
            self.restart_button.visible = True
            self.restart_button.on_click()
            self.player.y = 5

    def score_coint_tracker(self):
        global text
        for coin in self.list_of_coins:
            coin.rotation_y += time.dt * 300
        text.y = 1
        text = Text(text=f' Score: {self.score_counter}', scale=2, position=(-.75, .45), origin=(0, 0),
                    color=color.yellow,
                    background=True)

        for coint in self.list_of_coins:
            if abs(self.player.x - coint.x) <= 1 and abs(self.player.y - coint.y) <= 1:
                self.score_counter += 10
                coint.visible = False
                self.list_of_coins.remove(coint)
                self.coints_sound.play()

    def cat_food_power_up(self):
        global right_flag
        if abs(self.player.x - self.cat_food.x) <= 1 and abs(self.player.y - self.cat_food.y) <= 1:
            self.cat_power_flag = 1
            self.cat_food.visible = False
        if abs(self.player.x - self.cat_food_2.x) <= 1 and abs(self.player.y - self.cat_food_2.y) <= 1:
            self.cat_power_flag = 1
            self.cat_food_2.visible = False
        if self.cat_power_flag == 1:
            if held_keys['r']:
                self.cat_ball_attack.visible = True
                if self.player.right[0] == 1.0:
                    right_flag = True
                else:
                    right_flag = False

                self.cat_ball_attack.attack(self.player)
        try:
            if right_flag:
                self.cat_ball_attack.x += 0.10
            elif right_flag == False:
                self.cat_ball_attack.x -= 0.10
        except:
            pass
        if abs(self.cat_ball_attack.x) > abs(self.player.x) + 9:  # range of the cat ball attack
            self.cat_ball_attack.visible = False
            self.cat_ball_attack.y = -3
            self.cat_ball_attack.x = -3

    def health_bar(self):
        self.full_bar.x = camera.x - self.size // 1.5  # size is the width of the background image
        self.full_bar.y = camera.y + 4
        self.green_bar.x = self.full_bar.x
        self.green_bar.y = self.full_bar.y

    def check_point_save(self):
        if len(self.checkpoint_list) > 0:
            for checkpoint in self.checkpoint_list:
                if abs(self.player.x - checkpoint.x) < 1 and abs(
                        self.player.y - checkpoint.y) < 2:
                    if checkpoint.visible:
                        m = Text(text="Checkpoint reached!", origin=(0, 0), scale=2,
                                 color=color.yellow,
                                 background=True)
                        invoke(destroy, m, delay=1)
                        checkpoint.visible = False
                        self.restart_coord = (checkpoint.x, checkpoint.y)

    def plant_trap_logic(self):
        for trap in self.trap_list:
            dis = abs(self.player.x - trap.x)
            dis_2 = abs(self.player.y - trap.y)
            if dis <= 1.5 and dis_2 <= 1.5:
                self.player.color = color.red
                # loose health
                self.green_bar.scale_x -= self.shrink_health_bar * time.dt
                if self.green_bar.scale_x < 0.1 and self.immortal_muffin == 0:
                    self.player.rotation_z = 90
                    self.switch = 0
                    self.player.x, self.player.y = self.restart_coord[0], self.restart_coord[1]

            else:
                self.player.color = color.white

    def enemy_movement_and_control(self):
        self.dx += self.speed * time.dt
        if abs(self.dx) > 2:
            self.speed *= -1
            self.bird_speed *= -1
            self.dx = 0

        self.mouse_enemy.x += self.speed * time.dt
        # check for collision with enemy
        for enemy in self.enemies:
            enemy.x += self.speed * time.dt
            if type(enemy) is BirdEnemy:
                enemy.x += self.bird_speed * time.dt
            if abs(self.player.x - enemy.x) < 1.5 and abs(self.player.y - enemy.y) < 1.5 and self.immortal_muffin == 0:
                self.player.rotation_z = 90
                self.switch = 0
                self.green_bar.scale_x = 0

            if isinstance(enemy, MouseEnemy) is False:
                if abs(self.cat_ball_attack.x - enemy.x) < 1 and abs(self.cat_ball_attack.y - enemy.y) < 1:
                    self.death_enemies.append(enemy)
                    enemy.visible = False
                    self.enemies.remove(enemy)
                    self.score_counter += 1

            if isinstance(enemy, RattonEnemy):
                try:
                    if abs(self.player.x - enemy.raccon_attack.x) < 1 and abs(
                            self.player.y - enemy.raccon_attack.y) < 1 and self.immortal_muffin == 0:
                        self.player.rotation_z = 90
                        self.switch = 0
                        self.green_bar.scale_x = 0
                except AssertionError:
                    pass
            if abs(self.player.x - self.cat_fire_tower.fire_tower_attack.x) < 1 and abs(
                    self.player.y - self.cat_fire_tower.fire_tower_attack.y) < 1 and self.immortal_muffin == 0:
                # self.switch = 0
                self.green_bar.scale_x -= self.shrink_health_bar * time.dt
            elif isinstance(enemy, MouseEnemy):
                if abs(self.player.x - self.mouse_enemy.cheese_attack.x) < 1 and abs(
                        self.player.y - self.mouse_enemy.cheese_attack.y) < 1 and self.immortal_muffin == 0:
                    self.switch = 0
                    self.green_bar.scale_x = 0
                if abs(self.cat_ball_attack.x - enemy.x) < 1:
                    self.cat_ball_attack.x = -1222
                    self.mouse_hit_points -= 1
                    invoke(setattr, enemy, 'visible', False, delay=0.25)
                    invoke(setattr, enemy, 'visible', True, delay=0.25)
                    self.mouse_enemy.cheese_attack.visible == False
                    enemy.visible = True
                    if self.mouse_hit_points < 6:
                        enemy.visible = False
                        enemy.x = -1222
                        self.score_counter += 50
                        m = Text(text="Puwerfect , you just finish the first level!", origin=(0, 0), scale=2,
                                 color=color.yellow,
                                 background=True)
                        invoke(destroy, m, delay=2)

                        self.finish_level = True

    def reset_and_restart_all(self):
        """
        All enemy movement and game logic are inside self.switch( if the player is alive switch is equal with 1 -> thus enemy
        are moving ,player can move etc-> if its 0 -> wait for reset -> stop all movement of the enemies until
        the player clicks on restart
        :rtype: object
        """
        if self.switch == 1:
            self.enemy_movement_and_control()

        if self.switch == 0:
            self.restart_button.visible = True
            self.player.walk_speed = 0

    def update(self):
        self.restart_logic()
        self.score_coint_tracker()
        self.cat_food_power_up()
        self.health_bar()
        self.check_point_save()
        self.plant_trap_logic()
        self.reset_and_restart_all()
        # final boss movement

    def immortal_muffin_active(self):
        self.immortal_muffin = 1

    def pause_handler_input(self, key):
        if key == 'p':
            application.paused = not application.paused  # Pause/unpause the game.
            self.pause_text.enabled = application.paused  # Also toggle "PAUSED" graphic.

    def input(self, key):
        actions = {'space': self.jump.play, 'i': self.immortal_muffin_active, }
        self.pause_handler.input = self.pause_handler_input  # Assign the input function to the pause handler.
        if key in actions:
            actions[key]()

        if held_keys['q'] or held_keys['escape']:
            quit()
        # in case you are stuck
        if held_keys['y']:  # in case player stuck
            self.player.y += 1
            self.player.x += 1

    def unloadlevel(self):
        # todo : try so solve this!
        destroy(self.player)

    def reset(self):
        # global switch, enemies, immortal_muffin, score_counter, cat_power_flag
        self.player.x, self.player.y = self.restart_coord[0], self.restart_coord[1]
        self.score_counter = 0
        self.player.rotation_z = 0
        self.cat_power_flag = 0
        self.cat_food.visible = True
        self.cat_food_2.visible = True
        self.green_bar.scale_x = 5
        self.switch = 1
        self.restart_button.visible = False
        self.immortal_muffin = 1
        self.player.walk_speed = 10
        invoke(self.reset_immortal_muffin, delay=5)
        # for enemy in self.death_enemies:
        #     enemy.visible = True  # set the visible to true for death enemies(when they die visible becomes false..
        # self.enemies += self.death_enemies  # add death enemies to the new list when they are revived(after restart button is presset)

    def reset_immortal_muffin(self):
        self.immortal_muffin = 0
