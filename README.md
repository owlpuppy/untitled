# untitled
> becoming a master artist, a text-based adventure

Becoming an artist is hard, becoming a master artist is even harder. I tried to make it difficult. Please have patience.
There is no save game currently planned.
Warning: this is incomplete and not fully tested!

To be clear, untitled is the *name* I chose. It's intentional. And maybe dumb, but oh well.

## Purpose  
text-based adventure game, entertainment

## Requirements:  
Python 3.13 or later, UV, and a terminal able to output ANSI escape characters (this can be altered if necessary).
(also refer to pyproject.toml)

## Use

### Play the game
Navigate to the base directory (the one with this Readme in it).
Make shell script executable.
Enter the following into the terminal (note this will clear the terminal window):
```./play.sh```

### Run automated tests
Navigate to the base directory (the one with this Readme in it).
Make shell script executable.
Enter the following into the terminal:
```./test.sh```
Note there aren't any tests yet, but it will run.

## Planned  
- expand classes
- add more information to title section (it's bare)
- add rooms and actions (create art, etc.), separate actions
- add failure modes
- automated tests
- modify functions to return stuff as necessary, ensure all print commands are located in the same function
- filter player input more

## Possible
- editable artwork inventory
- logging (haven't thought of anything to log yet)
- print handler (type to screen)
- randomized descriptions and statements

## Completed changes
- basic classes
- actions separated
- screen output separated
- separate status displays, can accept messages as well
- settings menu
- added ability to go to previous location by using << prev >> in story
- added commands function to control the common commands display
- added more instance methods 

Last updated: 4 November 2026
