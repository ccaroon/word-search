import word_search.adventure.items.entrance as items

from .exit import room as exit_room
from scriptum.room import Room
# ------------------------------------------------------------------------------
room = Room(
    "Entrance",
    F"""
You are standing just inside the entrace to a cavern. Directly in front of you is a {items.door.state_desc()}.

The mouth of the cave, the only way out of here, is to the south.
""",
    items=[items.lantern],
    objects=[
        items.door
    ],
    south=exit_room
)
