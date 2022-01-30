from ursina import *
from ursina.prefabs.platformer_controller_2d import PlatformerController2d
from obj.cat_menu import HealthBar, MenuMenu
from obj.enemy import DogEnemy, BirdEnemy, MouseEnemy
from obj.cat_powers import CatBall, CatCoins
from levels.first_level import FirstLevel
# def load_audio(filepath: str, loop=False) -> audio.Audio:
#     a = audio.Audio(sound_file_name=None, loop=False)
#     loaded_sound = app.loader.loadSfx(filepath)
#     a.clip = loaded_sound
#     return a
# speed = 1
# coints_sound=Audio('coint.mp3',loop=False,autoplay=False)
terrain_lengh_size = 5


class SecondLevel(FirstLevel):
    def __init__(self, **kwargs):
        super().__init__(
            self.player
        )