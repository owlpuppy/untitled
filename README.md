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
- add rooms and actions
- add failure modes
- automated tests
- modify functions to return stuff as necessary, ensure all print commands are located in the same function
- decide on what I want for win mechanics and how to implement them
- update quit and intro screens
- update studio text
- add warning and lose mechanic for no sleep (called in engine) (may need to place creation of reply variable at start of loop and append to it)
- need to add testing (should have done this already)
- create a way to update inventory (may just be able to use a second input)

## Possible
- editable artwork inventory
- logging (haven't thought of anything to log yet)
- print handler (type to screen)
- more input filtering

## Changelog (forgot this is how you do that)
## 0.1.0 - 0.1.2
- basic classes
- actions separated
- screen output separated
- separate status displays, can accept messages as well
- settings menu
- added ability to go to previous location by using << prev >> in story
- added commands function to control the common commands display
- added more instance methods 

### 0.1.3
- moved action responses to TOML file
- added ability to randomly choose one of multiple action responses
- added ability to define lose message and status in TOML file and collect responses
- changed end of game detection to use get (simpler, am told it's faster)
- added content to TOML

### 0.1.4
- updated drink coffee action logic
- added PlayerMood enum
- added player instance method to update mood based on artworks (based on combined mood of artworks)
- added liked (mood) to artwork and a class method to create artwork with weighted randomized mood (based on player mood)
- added basic input filtering

### 0.1.5
- started on studio time mechanic
- started on nap action
- started on add artwork action
- updated drink coffee action to use time
- modified update mood mechanic to vary based on time in studio
- modified status bar for clarity, added studio time to status bar
(I wanted to commit this even though it is not done)

### 0.1.6
- create artwork action finished
- create artwork status and reply messages added 
- fixed mood mechanic to only adjust when a work has been added
- created artwork title generator
- temporarily displayed all artworks (this will be removed)

Last updated: 9 November 2026
