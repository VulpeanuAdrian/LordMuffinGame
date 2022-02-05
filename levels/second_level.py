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
# coints_sound=Audio('coint.mp3',loop=False,autoplay=False)
terrain_lengh_size = 5


class SecondLevel(Entity):
    def __init__(self, **kwargs):
        super().__init__()
        self.finish_level=False
        self.first_level_sound = Audio('first_level_sounds.mp3', loop=True, autoplay=True)
        self.jump = Audio('../assets/jump.mp3', loop=False, autoplay=False)
        self.coints_sound=Audio('coint.mp3',loop=False,autoplay=False)
        self.death_enemies = []
        self.mouse_hit_points = 6  # final boss life = equal with 5 hits
        self.immortal_muffin = 1
        self.switch = 1
        self.cat_power_flag = 0
        self.bird_speed = 1
        self.dx = 0  # distance enemy moves to 1 direction
        self.size = 13
        self.shrink_health_bar = 2
        self.enemies = []
        self.enemy = DogEnemy(2, -1)
        self.enemies.append(self.enemy)
        self.enemy = DogEnemy(-6, -1)
        self.enemies.append(self.enemy)
        self.enemy = BirdEnemy(-10, 5)
        self.enemies.append(self.enemy)
        self.speed = 1
        self.size = 13
        self.cat_ball_attack = CatBall()
        self.score_counter = 0
        ground_coordonates=[]
        self.bg = Entity(model='cube', scale=(self.size, 24), texture='images/image01', z=1)

        self.ground = Entity(model='quad', y=-2, collider='box', color=color.white, scale=(10, 0.7),
                             )


    def update(self):
        print(1111*1000)