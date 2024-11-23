# writing this program within a single document hurt my brain. idk how the notepad++ guy does it.
# i'm pretty familiar with scripting languages through my experience doing game dev. anything that could possibly be misconstrued as written by AI i've given an explanation for; the Python docs have been very helpful.

import os # to clear the terminal
import sys
import time
import keyboard # googled "python keyboard pressed input library"; this way we can detect key presses without the user having to send a whole line in the console and without having to pause the program for their input.
from enum import Enum, auto

# An enum for all location names
class Location(Enum): # learned about how enums work in Python through the docs
    ENTRANCE = auto()






# interpret player's command for game actions
def interpret_command(command, loc):
    flush_input()
    command_array = process_command(command)
    if len(command_array) > 0:
        match command_array[0].lower():
            case "help":
                display_help()
                return False, loc
            case "look":
                time.sleep(0.5)
                flush_input()
                look(loc)
                return False, loc
    else:
        return False, loc
    print("Unknown command. Type \"help\" for a list of valid commands.")
    return False, loc


# process a command into an array with each piece of syntax (in order) at a subsequent index
def process_command(command):
    command_array = command.split() # splits the string using " " as the separator, adding each word to a subsequent index in the array
    return command_array


# the ingame menu where you can input actions
def game_menu(loc):
    look(loc)
    while True:
        command = input("> ")
        print()
        moved, new_loc = interpret_command(command, loc) # returning True means the location has changed
        if moved:
            game_menu(new_loc) # if the location has changed, we'll call game_menu and pass in the new location
            return # putting this return here probably makes everything safer, idk


def display_help():
    print("Available commands:")
    print("HELP")
    print("- Shows a list available commands.")
    print()
    print("LOOK")
    print("- Looks at your surroundings.")


def look(loc):
    match loc:
        case Location.ENTRANCE:
            printg("You stand before the mouth of the cave, a jagged opening carved into the side of a weathered hillside.")
            printg(" The air is noticeably cooler here, carrying a faint, musty scent of earth and stone.", 0.2)
            printg(" A soft breeze escapes the darkness within, brushing against your skin and sending a faint shiver down your spine.", 0.2, True)


# play the intro scene when a new game is started
def intro():
    printg("You step outside your house, greeted by the crisp chill of the evening air.")
    printg(" The sun dips below the horizon, painting the sky in hues of orange and purple.")
    printg(" The world feels still, save for the occasional rustle of leaves in the distance.", True)
    printg(".", 1.0)
    printg(".", 1.0)
    printg(".", 1.0)
    # TODO: finish intro
    # ----- not the most important, so for now we'll skip to the part where we're in the entrance of the cave


# starts a new game
def new_game():
    game_menu(Location.ENTRANCE)


# load and interpret a save
def load_game():
    pass


# print a line gradually, can press ENTER to print instantly
# Python strings are like arrays or lists (not sure which) of chars, so this lets us do some fun things using indices
def printg(string, newline = False, delta = 0.020): # interpret "delta" as time in seconds between chars
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
    input("Press the <ENTER> key to continue...")


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
def terminal_screen():
    os.system('cls' if os.name == 'nt' else 'clear') # first case is for windows, else is for unix
    flush_input() # flush the input buffer so dumb shit doesn't happen (this is becoming a really useful method)


def main_menu():
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
        case "3" | "quit":
            quit()
        case _:
            print("Input is invalid. Please enter an integer (1-3).")
            time.sleep(1.5)
            clear_terminal()
            main_menu()


def main():
    #intro()
    main_menu()


if __name__ == "__main__":
    main()
