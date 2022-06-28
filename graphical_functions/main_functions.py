from ursina import *
from levels.first_level import FirstLevel
from levels.second_level import SecondLevel

help_text_string = 'In a catlaxy far away the fat persian Muffin must save the catniverse \n \n' \
                   'In order to do that you can control it by using:\n \n' \
                   'Movement: Left:A Right:D  jump:space,\n\n' \
                   'Attack:R \n \n' \
                   'Exit:Q in order to quit the game'
from direct.stdpy import \
    thread  # we need threading to load entities in the background (this is specific to ursina, standard threading wouldn't work)


def main():
    def start_level() -> FirstLevel:
        destroy(play)
        destroy(help)
        destroy(help_text)
        destroy(exit_button)
        destroy(cat_screen)
        return FirstLevel()

    def help_text_func() -> None:
        play.visible = True
        exit_button.visible = True
        destroy(help_text_bt)

    def help_menu() -> None:
        global help_text_bt

        help_text_bt = Button(text=help_text_string, on_click=help_text_func, scale=(0.8, 0.6), x=0.05, y=0.35,
                              color=color.orange, text_color=color.violet)


    app = Ursina()
    window.fullscreen = False
    cat_screen = Animation('cat_gif', fps=30, loop=True, autoplay=True, scale=(13, 13))  # Cat Animation
    cat_screen.start()
    play = Button('Play', on_click=start_level, scale=(0.095, 0.095), x=0, y=0, color=color.blue)  # Start level button
    help = Button('Help', on_click=help_menu, scale=(0.095, 0.095), x=0, y=-0.1)  # Help Button
    help_text = Text(text=help_text_string, x=-0.3, y=0.3, visible=False,
                     color=color.random_color())  # Help text pop up
    exit_button = Button(' Quit ', on_click=application.quit, x=0, y=-0.2, scale=(0.095, 0.095),
                         color=color.red)  # Exit button
    app.run()
