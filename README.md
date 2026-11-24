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
- decide on what I want for win mechanics and how to implement them
- update quit screen
- need to add testing (should have done this already)
- implement inventory modifications using second input line within the function (in progress)
- inplement random problem mechanics
- add eq method to player?

## Possible
- editable artwork inventory
- logging (haven't thought of anything to log yet)
- print handler (type to screen)

## Current Version

### 0.4.0
- changed 1 and 2 to success and caution in story and logic (makes code clearer)
- changed get response to continue if responses are missing/wrong in story, generates error if the type is invalid
- added travel time option, only does anything if there's a target
- added logging

## Changelog

### 0.1.0 - 0.1.2
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

### 0.1.7
- reworked mood mechanic to work differently
- added loss by excessive studio time mechanic, warns in status line only
- (artwork display is still temporarily on)

### 0.1.8
- added ability for variable story text and helper function to select text based on type
- fixed error that bypasssed failure to create
- added home with nap (bed) action, finished nap (bed) action
- added more story text
- changed actions to use error for in game failure (idk if this is best but it makes it readable)

### 0.1.9
- story edits
- mechanic adjustments
- replace min and max vars with low and high (forgot this would shadow)
- remove exisitng tired weight, add mechanic that reduces or adds time until tired depending on mood when going to sleep
- various small code improvements
- removed drink coffee and nap actions from player and added the underlying functionality to actions

### 0.2.0
- story edits, added catalog
- added show data to render, has artwork catalog so far but it's expandable
- added str method to artwork objects
- added game action placeholders for catalog editing (displays not implemented)
- removed art list from regular pages, since you can now look at it in catalog

### 0.2.1
- added remove work action (has instant loss mechanic, conditional error mechanic)
- fixed update mood bug (didn't reset mood when only one work was present and that was deleted)
- created function to get a response based on response type
- cleaned up some render logic
- added common input functions to take string and int (false is error for string, not an int for int)
- changed artwork, player classes to do variable initial values in a classmethod
- added str and repr to player
- story updates

### 0.2.2
- changed studio time to time awake
- added error to actions
- delete work: added random fail to delete and time awake, code cleanup
- added rework work
- added random fail to drink coffee
- fixed caution/extra delete bug in actions to make sure it only deletes a second one if there is one
- added time awake to repr and str for player
- changed time awake and add time to go 2 above min
- modified PlayerMood to have named values, makes more sense internally
- modified common input functions to return None if the request is cancelled, added logic to act on that
- code improvements

### 0.3.0
- added win by value check, win location, win story
- added weight to artwork creation
- changed rework to handle the weighted variables and always get a little better or worse (code is messy)
- removed repr methods (they weren't correct, I need to figure that out)
- added win stats to render
- updated intro

Last updated: 23 November 2026
