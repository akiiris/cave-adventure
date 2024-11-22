import time
import keyboard # googled "python keyboard pressed input library"; this way we can detect key presses without the user having to send a whole line in the console and without having to pause the program for their input.


def scene_intro():
    printg("You step outside your house, greeted by the crisp chill of the evening air.")
    printg(" The sun dips below the horizon, painting the sky in hues of orange and purple.", 0.2)
    printg(" The world feels still, save for the occasional rustle of leaves in the distance.", 0.2, True)
    printg(".", 1.0)
    printg(".", 1.0)
    printg(".", 1.0)


# prints a line gradually, can press ENTER to print instantly
# Python strings are like arrays or lists (not sure which) of chars, so this lets us do some fun things using indices
def printg(string, prewait = 0.0, newline = False, delta = 0.020): # interpret "delta" as time in seconds between chars
    time.sleep(prewait)
    pos = 0
    while pos < len(string): # used (pos)ition instead of a for loop over the string so we know the index it stops at if the player presses ENTER
        print(string[pos], end = "", flush = True) # originally this wasn't showing up in the terminal. apparently, by default, the output only displays at certain points. this is when it flushes the buffer. one of these points is when there's a \n, so normally you would see everything from a print() statement immediately. however, when replacing the end character with empty string, it never flushes the buffer. we can fix this by setting flush to True so that it forcefully flushes it every print() call.
        pos += 1
        if keyboard.is_pressed('enter'): # checks if the player presses enter
            flush_input() # flush the input buffer so the ENTER key press isn't processed multiple times
            print(string[pos:], end = "") # "string slicing" (from geeksforgeeks.org); colon indicates to removes all chars before the specified index; print the remainder of the string
            if newline:
                print() # add a \n
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
        import sys, termios
        termios.tcflush(sys.stdin, termios.TCIOFLUSH) # idk how this works and didn't bother looking into it because i don't use linux or macos, but i added it for compatibility


def main():
    scene_intro()


if __name__ == "__main__":
    main()
