import sys

import word_search.adventure.items.entrance as items
from scriptum.scene import Scene

from scriptum.room import Room
# ------------------------------------------------------------------------------
room = Room(
    "Exit",
    F"""
Ahhhh ... Sunshine!
""",
    # items=[items.lantern],
    # objects=[
    #     items.door
    # ],
    # north=puzzle_room
)

room.enter_scene = Scene("Got No Time For This")
room.enter_scene.add_dialogue(F"""You ain't got time for this! You head off out of the
cavern in search of a pencil.
""")
room.enter_scene.add_action(sys.exit)
