from adventurelib import *

from colorama import Back, Fore

import word_search.adventure.contexts as contexts
from scriptum.context import Context

from word_search.adventure import CURRENT_ROOM
from word_search.adventure import GAME_MAP
from word_search.adventure import INVENTORY

from scriptum.screen import Screen
# ------------------------------------------------------------------------------
# Game
# ------------------------------------------------------------------------------
@when("save")
def save_state():
    say("Saving has not yet been implemented!")
# ------------------------------------------------------------------------------
# Inventory Related Commands
# ------------------------------------------------------------------------------
@when("i")
@when("inventory")
def view():
    if INVENTORY:
        print(F"You're carrying {len(INVENTORY)} items:")
        for item in INVENTORY:
            print(F"{item}")
    else:
        print("You have nothing!")

@when("take THING from OBJECT")
@when("take THING off OBJECT")
@when("remove THING from OBJECT")
def take_item1(thing, object):
    obj = CURRENT_ROOM.objects.find(object)

    if obj:
        item = obj.items.take(thing)
        if item:
            INVENTORY.add(item)
            say(F"You remove the {item} from the {obj}.")
        else:
            item = obj.parts.find(thing)
            if item:
                say(F"The {thing} is tightly fastend to the {object} and will not come off.")
            else:
                say(F"You don't see a {thing} on the {object}")
    else:
        say(F"You don't see any {object} in here.")

@when("pick up THING")
@when("take THING")
def take_item2(thing):
    item = CURRENT_ROOM.items.take(thing)
    if item:
        INVENTORY.add(item)
        print(F"You take the {thing}.")
    else:
        obj = CURRENT_ROOM.objects.find(thing)
        if obj:
            say(F"You can't pick that up.")
        else:
            say(F"You don't see any '{thing}' here.")

@when("drop THING")
def remove_item(thing):
    item = INVENTORY.find(thing)

    if item:
        if not item.undroppable:
            item = INVENTORY.take(thing)
            CURRENT_ROOM.items.add(item)
            say(F"Dropped {thing}.")
        else:
            say(F"You should probably hold onto your {thing}.")
    else:
        say(F"You're not even carrying a {thing}.")

@when("push PART on THING")
def interact(part, thing):
    item = INVENTORY.find(thing) or CURRENT_ROOM.objects.find(thing)

    if item:
        sub_item = item.items.find(part) or item.parts.find(part)
        if sub_item:
            sub_item.activate()
        else:
            say(F"{thing} does not have a {part}.")
    else:
        say(F"There's no {thing} in the current vicinity.")

@when("examine PART on THING")
@when("x PART on THING")
@when("look at PART on THING")
def examine_part(part, thing):
    item = INVENTORY.find(thing) or CURRENT_ROOM.objects.find(thing)
    sub_item = None

    if item:
        sub_item = item.items.find(part) or item.parts.find(part)
        if sub_item:
            say(sub_item.describe())
        else:
            say(F"{thing} does not have a {part}.")
    else:
        say(F"You don't have any {thing}.")

@when("examine THING")
@when("x THING")
@when("look at THING")
def examine(thing):
    item = INVENTORY.find(thing) or CURRENT_ROOM.objects.find(thing)

    if item:
        say(item.describe())
    else:
        say(F"You don't have any {thing}.")

# ------------------------------------------------------------------------------
# Room Related Commands
# ------------------------------------------------------------------------------
@when("l")
@when("look")
def look():
    print(CURRENT_ROOM)

    # TODO: better incorporate items in to the narrative
    if CURRENT_ROOM.items:
        print("\nLooking around you reveals: ")
        for thing in CURRENT_ROOM.items:
            print(thing)

    # TODO: better incorporate exits in to the narrative
    exits = CURRENT_ROOM.exits()
    if exits:
        print(F"\nExits: {exits}")

@when("map")
def map():
    loc = getattr(CURRENT_ROOM, 'location', None)
    if loc:
        old_cell = GAME_MAP.get(loc[0], loc[1])
        GAME_MAP.set(loc[0], loc[1], Screen.colorize_text(old_cell, fg=Fore.BLACK, bg=Back.WHITE))
        print(GAME_MAP)
        GAME_MAP.set(loc[0], loc[1], old_cell)
    else:
        say("Map? What map?")

# ------------------------------------------------------------------------------
# Movement
# ------------------------------------------------------------------------------
@when("exit")
def leave():
    global CURRENT_ROOM

    exits = CURRENT_ROOM.exits()
    if len(exits) > 1:
        say(F"""
            There's more than one way to leave this room. Which one would you like to try?
            {exits}
        """)
    elif len(exits) == 0:
        print("There doesn't appear to be any way out of here! You're trapped! Forever!")
    else:
        if CURRENT_ROOM.exit_scene:
            CURRENT_ROOM.exit_scene.play()

        CURRENT_ROOM = CURRENT_ROOM.exit(exits[0])

        if CURRENT_ROOM.enter_scene:
            CURRENT_ROOM.enter_scene.play()

        print(CURRENT_ROOM)

@when("open THING")
def open(thing):
    openable = CURRENT_ROOM.objects.find(thing)
    if not openable:
        for object in CURRENT_ROOM.objects:
            if object.is_a(thing):
                openable = thing

    if openable:
        if openable.is_a("door"):
            # TODO: how to open the door, exit which direction?
            say(F"You opened {thing}")
        else:
            say(F"You can't open the {thing}")
    else:
        say(F"You don't see any {thing} there.")


@when('n', direction='north')
@when('ne', direction='northeast')
@when('e', direction='east')
@when('se', direction='southeast')
@when('s', direction='south')
@when('sw', direction='southwest')
@when('w', direction='west')
@when('nw', direction='northwest')
def move(direction):
    global CURRENT_ROOM

    if CURRENT_ROOM.exit_scene:
        CURRENT_ROOM.exit_scene.play()

    room = CURRENT_ROOM.exit(direction)

    if room:
        if room.enter_scene:
            room.enter_scene.play()

        CURRENT_ROOM = room
        print(CURRENT_ROOM)

        # Update map
        loc = getattr(CURRENT_ROOM, 'location', None)
        if loc:
            puzzle = INVENTORY.find("puzzle")
            GAME_MAP.set(loc[0], loc[1], puzzle.real_obj.letter_at(loc[0], loc[1]))

    else:
        say(F"You can't move {direction}.")
# ------------------------------------------------------------------------------
# Cheating
# ------------------------------------------------------------------------------
@when("context ACTION", context="cheating")
def context(action):
    if action == "clear":
        Context.clear()
        Context.add(contexts.CHEATING)
    elif action == "show":
        print(get_context())
    elif action.startswith("add"):
        status = action.replace("add", "")
        ctx = Context(status.strip())
        Context.add(ctx)

@when("cheat ACTION", context="cheating")
def cheat(action):
    print(F"Unknown cheat command '{action}'.")









#
