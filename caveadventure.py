# writing this program within a single document hurt my brain. idk how the notepad++ guy does it.
# i'm decently familiar with scripting languages through my experience doing game dev and i'm familiar with OOP because i took a java class in high school. anything that could possibly be misconstrued as written by AI i've given an explanation for; the Python docs have been very helpful.

import os # to clear the terminal
import sys
import time
from tkinter import *
from tkinter import ttk
import keyboard # googled "python keyboard pressed input library"; this way we can detect key presses without the user having to send a whole line in the console and without having to pause the program for their input.
import location # i wrote this; # handles the Location class and builder

# information dictionaries
value_dict = None # maps items to their value

# player data variables
current_location = None
inventory = []

# location variables (objects)
# after calling initialize_locations() at program start, they will each contain a unique location object
# i'm not sure if you have to declare global variables before you set them in Python, but i am just to be safe
locations = None # maps location names to Location objects (see initialize_locations())
loc_entrance = None
loc_main_tunnel = None
loc_forked_path = None
loc_crystal_cavern = None
loc_hidden_passage = None
loc_ancient_shrine = None
loc_underground_stream = None
loc_cavern_pool = None
loc_submerged_tunnel = None
loc_sunken_chamber = None



# the ingame menu where you can input actions
def game_menu(loc_name):
    global locations
    global current_location
    look(locations[loc_name])
    while True:
        command = input("> ")
        moved, new_loc_name = interpret_command(command, loc_name) # returning True means the location has changed
        if moved:
            current_location = new_loc_name
            game_menu(new_loc_name) # if the location has changed, we'll call game_menu and pass in the new location
            return # putting this return here probably makes everything safer, idk; we're just getting deeper into this chain with each game_menu() call


# interpret player's command for game actions
def interpret_command(command, loc_name):
    global locations
    loc = locations[loc_name]
    flush_input()
    command_array = process_command(command)
    time.sleep(0.5)
    if len(command_array) > 0:
        match command_array[0].lower():
            case "checkvalue":
                check_value()
                return False, loc_name
            case "goto":
                if len(command_array) == 2:
                    return goto(loc, command_array[1])
                else:
                    print("Invalid usage. Please use 'GOTO <location>' where <location> uses underscores instead of spaces.")
                    return False, loc_name
            case "help":
                display_help()
                return False, loc_name
            case "inventory":
                if len(command_array) == 1:
                    display_inventory()
                    return False, loc_name
                match command_array[1]:
                    case "min":
                        min_max_inventory(True)
                        return False, loc_name
                    case "max":
                        min_max_inventory()
                        return False, loc_name
                    case "sum":
                        sum_inventory()
                        return False, loc_name
                    case _:
                        display_inventory()
                        return False, loc_name
                display_inventory()
                return False, loc_name
            case "look":
                flush_input()
                look(loc)
                return False, loc_name
            case "pickup":
                pickup(loc, command_array)
                return False, loc_name
    else:
        return False, loc_name
    print("Unknown command. Type \"help\" for a list of available commands.")
    return False, loc_name


# process a command into an array with each piece of syntax (in order) at a subsequent index
def process_command(command):
    command_array = command.split() # splits the string using " " as the separator, adding each word to a subsequent index in the array
    return command_array


# display the inventory and select an item to check the value of
def check_value():
    try:
        global inventory
        global value_dict
        print("Select an item by integer:")
        index = 0
        for item in inventory:
            print(f"{index + 1}. {item}")
            index += 1
        choice = int(input("Which item would you like to check the value of? ")) - 1
        if choice < len(inventory):
            selected_item = inventory[choice]
            print(f"The value of a {selected_item} is {value_dict[selected_item]}")
            display_popup(f"The value of a {selected_item} is {value_dict[selected_item]}", "cool")
        else:
            print("Selection must be an integer listed above.")
    except ValueError:
        print("Selection must be a valid integer.")
        


def goto(loc, new_loc_name):
    for location in loc.can_go:
        if location == new_loc_name:
            return True, new_loc_name
    print("Destination is invalid or you can't go there. Please use \"_\" instead of \" \" in destination name.")
    return False, loc.name


def display_help():
    print("Available commands:")
    print("CHECKVALUE")
    print("Checks the value of an item in your inventory.")
    print()
    print("GOTO <location>")
    print("- Goes to a location in range. (Use \"_\" instead of \" \" in location names)")
    print()
    print("HELP")
    print("- Shows a list available commands.")
    print()
    print("INVENTORY")
    print("- Displays your inventory.")
    print()
    print("INVENTORY MIN/MAX")
    print("- Tells you the highest/lowest valued item in your inventory.")
    print()
    print("INVENTORY SUM")
    print("- Sums the values of every item in your inventory.")
    print()
    print("LOOK")
    print("- Looks at your surroundings.")
    print()
    print("PICKUP <item>")
    print("Picks up an item in range.")


# display the inventory
def display_inventory():
    global inventory
    print("Inventory:")
    if len(inventory) == 0:
        print("Empty")
    else:
        for item in inventory:
            itemc = item.capitalize() # capitalize each item
            print(f"{itemc}")


# sort the inventory; called any time the inventory is changed
def sort_inventory():
    global inventory
    inventory.sort() # sort the inventory in alphabetical order


# find the minimum or maximum value item in the inventory
def min_max_inventory(minimum = False):
    global inventory
    global value_dict
    if len(inventory) == 0:
        printg("Your inventory is empty.")
    elif minimum:
        first_go_through = True
        min_value_item = None
        for item in inventory:
            if first_go_through:
                min_value_item = item
                first_go_through = False
            else:
                min_value = min(value_dict[item], value_dict[min_value_item])
                if value_dict[item] == min_value:
                    min_value_item = item
        print(f"Your lowest-valued item is a {min_value_item} at a value of {value_dict[min_value_item]}")
        
    else:
        first_go_through = True
        max_value_item = None
        for item in inventory:
            if first_go_through:
                max_value_item = item
                first_go__through = False
            else:
                max_value = max(value_dict[item], value_dict[max_value_item])
                if value_dict[item] == max_value:
                    max_value_item = item
        print(f"Your highest-valued item is a {max_value_item} at a value of {value_dict[max_value_item]}")


# sum the values of all items in the inventory and display the sum
def sum_inventory():
    global inventory
    global value_dict
    vsum = 0
    for item in inventory:
        for ref, value in value_dict.items():
            if item == ref:
                vsum += value
    print(f"The total value of your inventory is {vsum}.")


def look(loc):
    printg(loc.desc)
    for item in loc.items:
        printg(f"There is a {item} here.")
    for location in loc.can_go:
        printg(f"There is a path leading to the {location}.")


# pick up an item and add it to the inventory
def pickup(loc, command_array): # TODO
    global inventory
    item_name = ""
    first_go_through = True
    for word in command_array:
        if first_go_through:
            first_go_through = False
        else:
            item_name += word + " "
    item_name = item_name.strip()
    print(item_name)
    found = False
    for item in loc.items:
        if item == item_name:
            found = True
            loc.items.remove(item)
            inventory.append(item)
            sort_inventory()
            print(f"You picked up a {item}!")
    if not found:
        print("There is no item within range with that name.")


# play the intro scene when a new game is started
def intro():
    printg("You step outside your house, greeted by the crisp chill of the evening air. The sun dips below the horizon, painting the sky in hues of orange and purple. The world feels still, save for the occasional rustle of leaves in the distance.", True)
    printg(".", 1.0)
    printg(".", 1.0)
    printg(".", 1.0)
    # TODO: finish intro
    # ----- not the most important, so for now we'll skip to the part where we're in the entrance of the cave


# starts a new game
def new_game():
    global current_location
    current_location = "entrance"
    game_menu("entrance")


# load and interpret a save
def load_game(): # TODO
    pass


# print a line gradually, can press ENTER to print instantly
# Python strings are like arrays or lists (not sure which) of chars, so this lets us do some fun things using indices
def printg(string, newline = True, delta = 0.020): # interpret "delta" as time in seconds between chars
    pos = 0
    while pos < len(string): # used (pos)ition instead of a for loop over the string so we know the index it stops at if the player presses ENTER
        print(string[pos], end = "", flush = True) # originally this wasn't showing up in the terminal. apparently, by default, the output only displays at certain points. this is when it flushes the buffer. one of these points is when there's a \n, so normally you would see everything from a print() statement immediately. however, when replacing the end character with empty string, it never flushes the buffer. we can fix this by setting flush to True so that it forcefully flushes it every print() call.
        pos += 1
        if keyboard.is_pressed('enter'): # checks if the player presses enter
            flush_input() # flush the input buffer so the ENTER key press isn't processed multiple times
            print(string[pos:], end = "") # "string slicing" (from geeksforgeeks.org); colon indicates to removes all chars before the specified index; print the remainder of the string
            if newline:
                print()
            return
        time.sleep(delta) # sleeps for delta seconds
    if newline:
        print()


# pauses the program to give the player time to read
def pause():
    input("Press the <ENTER> key to continue... ")


# i was getting this dumb bug where if i had printg() followed by pause() and i hit enter during the print to fast forward, the input would still be processed during the pause call
# this method flushes the input buffer so input won't be processed multiple times (code from stackoverflow, googled "python flush input buffer")
def flush_input():
    try: # for Windows
        import msvcrt # "Microsoft Visual C/C++ Runtime Library"
        while msvcrt.kbhit(): # returns True if a key press is buffered
            msvcrt.getch() # removes the key press from the input buffer after reading it
    except ImportError: # for Unix
        import termios
        termios.tcflush(sys.stdin, termios.TCIOFLUSH) # idk how this works and didn't bother looking into it because i don't use linux or macos, but i added it for compatibility


def quit():
    print("Goodbye!")
    time.sleep(1.0)
    sys.exit()


# clears the terminal (duh)
def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear') # first case is for windows, else is for unix
    flush_input() # flush the input buffer so dumb shit doesn't happen (this is becoming a really useful method)


# display a popup with a specific message
def display_popup(message, button_text): # from Python's "tkinter life preserver"
    root = Tk()
    frm = ttk.Frame(root, padding = 10)
    frm.grid()
    ttk.Label(frm, text = message).grid(column = 0, row = 0)
    ttk.Button(frm, text = button_text, command = root.destroy).grid(column = 1, row = 0)
    root.mainloop()


def main_menu():
    while True:
        print("Welcome to Cave Adventure!")
        print("1. New Game")
        print("2. Load Game")
        print("3. Quit")
        choice = input("> ")
        match choice.lower():
            case "1" | "new game":
                new_game()
            case "2" | "load game":
                load_game() # TODO: implement save loading
                display_popup("Saving and loading feature not yet implemented.", "aw darn")
            case "3" | "quit":
                quit()
            case _:
                print("Input is invalid. Please enter an integer (1-3).")
                time.sleep(1.5)
                clear_terminal()


# set up and parse all starting game data
def set_up_data():
    global value_dict
    
    initialize_locations()
    value_dict = parse_items()


# set up and build all locations in their initial states
def initialize_locations():
    global locations
    global loc_entrance
    global loc_main_tunnel
    global loc_forked_path
    global loc_crystal_cavern
    global loc_hidden_passage
    global loc_ancient_shrine
    global loc_underground_stream
    global loc_cavern_pool
    global loc_submerged_tunnel
    global loc_sunken_chamber
    
    builder_entrance = location.LocationBuilder()
    builder_entrance.set_name("entrance")
    builder_entrance.set_desc("You stand before the mouth of the cave, a jagged opening carved into the side of a weathered hillside. The air is noticeably cooler here, carrying a faint, musty scent of earth and stone. A soft breeze escapes the darkness within, brushing against your skin and sending a faint shiver down your spine.")
    builder_entrance.set_items([])
    builder_entrance.set_can_go(["main_tunnel"])
    loc_entrance = builder_entrance.build()
    
    builder_main_tunnel = location.LocationBuilder()
    builder_main_tunnel.set_name("main_tunnel")
    builder_main_tunnel.set_desc("You're in the main tunnel.") # TODO
    builder_main_tunnel.set_items(["rock", "stick"])
    builder_main_tunnel.set_can_go(["forked_path"])
    loc_main_tunnel = builder_main_tunnel.build()

    builder_forked_path = location.LocationBuilder()
    builder_forked_path.set_name("forked_path")
    builder_forked_path.set_desc("You're at the forked path.") # TODO
    builder_forked_path.set_items(["rock"])
    builder_forked_path.set_can_go(["main_tunnel", "crystal_cavern", "underground_stream"])
    loc_forked_path = builder_forked_path.build()
    
    builder_crystal_cavern = location.LocationBuilder()
    builder_crystal_cavern.set_name("crystal_cavern")
    builder_crystal_cavern.set_desc("You're in the crystal cavern.") # TODO
    builder_crystal_cavern.set_items(["shiny gem"])
    builder_crystal_cavern.set_can_go(["forked_path", "hidden_passage"])
    loc_crystal_cavern = builder_crystal_cavern.build()
    
    builder_hidden_passage = location.LocationBuilder()
    builder_hidden_passage.set_name("hidden_passage")
    builder_hidden_passage.set_desc("You're in the hidden passage.") # TODO
    builder_hidden_passage.set_items([])
    builder_hidden_passage.set_can_go(["crystal_cavern", "ancient_shrine"])
    loc_hidden_passage = builder_hidden_passage.build()
    
    builder_ancient_shrine = location.LocationBuilder()
    builder_ancient_shrine.set_name("ancient_shrine")
    builder_ancient_shrine.set_desc("You're at the ancient shrine.") # TODO
    builder_ancient_shrine.set_items([])
    builder_ancient_shrine.set_can_go(["hidden_passage"])
    loc_ancient_shrine = builder_ancient_shrine.build()
    
    builder_underground_stream = location.LocationBuilder()
    builder_underground_stream.set_name("underground_stream")
    builder_underground_stream.set_desc("You're at the underground stream.") # TODO
    builder_underground_stream.set_items(["fish"])
    builder_underground_stream.set_can_go(["forked_path", "cavern_pool", "submerged_tunnel"])
    loc_underground_stream = builder_underground_stream.build()
    
    builder_cavern_pool = location.LocationBuilder()
    builder_cavern_pool.set_name("cavern_pool")
    builder_cavern_pool.set_desc("You're at the cavern pool.") # TODO
    builder_cavern_pool.set_items(["stick"])
    builder_cavern_pool.set_can_go(["underground_stream"])
    loc_cavern_pool = builder_cavern_pool.build()
    
    builder_submerged_tunnel = location.LocationBuilder()
    builder_submerged_tunnel.set_name("submerged_tunnel")
    builder_submerged_tunnel.set_desc("You're in the submerged tunnel.") # TODO
    builder_submerged_tunnel.set_items(["rusted dagger"])
    builder_submerged_tunnel.set_can_go(["underground_stream", "sunken_chamber"])
    loc_submerged_tunnel = builder_submerged_tunnel.build()
    
    builder_sunken_chamber = location.LocationBuilder()
    builder_sunken_chamber.set_name("sunken_chamber")
    builder_sunken_chamber.set_desc("You're in the sunken chamber.") # TODO
    builder_sunken_chamber.set_items(["gold coin", "cut ruby"])
    builder_sunken_chamber.set_can_go(["submerged_tunnel"])
    loc_sunken_chamber = builder_sunken_chamber.build()

    # map location names to Location objects for easy referencing
    locations = {"entrance": loc_entrance,
             "main_tunnel": loc_main_tunnel,
             "forked_path": loc_forked_path,
             "crystal_cavern": loc_crystal_cavern,
             "hidden_passage": loc_hidden_passage,
             "ancient_shrine": loc_ancient_shrine,
             "underground_stream": loc_underground_stream,
             "cavern_pool": loc_cavern_pool,
             "submerged_tunnel": loc_submerged_tunnel,
             "sunken_chamber": loc_sunken_chamber}


# parse items.txt into a dictionary mapping item names to value
def parse_items():
    items_lines = []
    with open("items.txt") as file: # open file in read mode
        items_lines = file.readlines() # list where each line in the file is an item
    value_dict = {}
    for line in items_lines:
        item, value = line.strip().split(",")
        value_dict[item] = int(value)
    return value_dict


def main():
    #intro()
    set_up_data()
    main_menu()


if __name__ == "__main__":
    main()
