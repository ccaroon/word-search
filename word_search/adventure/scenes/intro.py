from colorama import Fore

from scriptum.screen import Screen
from scriptum.scene import Scene

scene = Scene("Intro")
scene.add_action(Screen.clear, pause=False)
scene.add_dialogue("Word Crawler", enlarge=True, color="red")
scene.add_dialogue("A word search puzzle, dungeon crawler style!")
