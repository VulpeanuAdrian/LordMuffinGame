from ursina import *
from levels.first_level import FirstLevel
from levels.second_level import SecondLevel

help_text_string='In a catlaxy far away the fat persian Muffin must save the universe ->\n' \
                 'In order to do that you can control it by using:\n' \
                 'Movement: Left: A Right: D key jump: space,\n' \
                 'Attack:R  ->\n'\
                 'Exit:Q in order to quit the game'
def start_level():
    global m
    destroy(play)
    destroy(help)
    destroy(help_text)
    destroy(exit_button)
    destroy(cat_screen)
    m=FirstLevel()


def help_menu():
    help_text.visible=True

if __name__ =='__main__':
    app = Ursina()
    window.fullscreen=True
    cat_screen = Animation('cat_gif', fps=30, loop=True, autoplay=True,scale=(13,13))
    cat_screen.start()
    play = Button(' Play ', on_click=start_level,scale=(0.095,0.095),x=0,y=0,color=color.blue)
    help=Button('Help', on_click=help_menu,scale=(0.095,0.095),x=0,y=-0.1)
    help_text=Text(text=help_text_string,x=-0.3,y=0.3,visible=False,color=color.random_color())

    exit_button = Button(' Quit ',on_click=application.quit,x=0,y=-0.2,scale=(0.095,0.095),color=color.red)



    app = app.run()