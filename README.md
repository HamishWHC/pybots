# PyBots Overview
PyBots is a programming game inspired by CROBOTS and was originally created by [Alessandro Pira](https://alessandropira.org).
Basically you have to write a python class that will control a pybot
which will fight with other pybots in an arena, aiming to be the last one standing
(or a tie by no bots remaining or 1000 steps have passed), without enemy shots still present in the arena.

Each bot has different options that you can set in order to change what is suited towards (e.g. a tank with low damage
and a small body, or a bot with higher damage but is weaker and larger). Each attribute has a cost associated with it,
so no high damage, high armour, high health bots!

Pybots are written as a single Python class that utilises no outside imports (aside from the math, random and util modules).
A method on this bot will be called periodically by the game to determine your bots next step.

The game itself consists of an arena of a given width and height and bots are spawned randomly around the map.
Each step (or turn) is taken simultaneously, and bots can shoot, move and change their scanner in each turn.
The scanner is used to determine the location of other bots and target shots.
Movement and shooting is done by setting an angle and speed (movement speed is variable,
however shot speed is set once along with damage and other attributes as mentioned above).
Shots move in a constant direction and at a constant speed. Bots cannot be hit by their own shots.
Exiting the map will cause a certain amount of damage per step.

# Installing PyBots
To install PyBots (the engine/game, not one bot!), you will need Python >=3.6 installed (only tested with Python 3.7, please add an issue if anything in 3.6 or 3.8 comes up, it may work in <3.6, but I'm not going to try supporting it).

Next, clone or download this repo to a location on your computer. And now PyBots is installed!

# Creating PyBots
To create a pybot you have to create a .py file.
The name of the file (excluding the ".py" extension) will be the name of your bot.

In this file you can import only random and math from python modules.
You can also import util which is a pybots module containing some utility functions.
If you try to import anything else your pybot will fail to load.

Inside this file you have to declare a class named "bot". This class must define the following (integer) class variabiles which will define the "hardware" of the pybot:
* `size` (5 - 15): each pybot is circular (or as circular as possible on a 2D, square grid), this determines the radius of the circle; bigger pybots are easier to hit.
* `armour` (0 - 3): each time the pybot is hit this value is subtracted from the damage
* `maxdamage` (10 - 15): the total damage that can be absorbed by the pybot before being eliminated (i.e. starting health)
* `maxspeed` (1 - 5): the maximum speed at which the pybot can move
* `shotpower` (1 - 5): the total power of shots that can be fired each round (damage inflicted on other bots)
* `shotspeed` (3 - 10): the speed of the shots
* `scanradius` (1 - 9): the width of the scanner (multiply by 20 to get the total scanner angle, centred on the direction of the scan given the `act` method)
Besides, you may define a set_arena_data function, which (if defined) will be called at the beginning of each fight to provide the pybot some info about the current round parameters (i.e. the arena size, the duration of the round, etc...).

You have also to define a method called "act" which will be called every step.

This routine will be called with just one parameter, which will be a tuple of `(name, pos, damage, scanresult)`, where:
* `name` is the name of the pybot;
* `pos` is the current position in the arena expressed as (x,y) tuple;
* `damage` is the current total damage of the pybot;
* `scanresult` is a list of `(name, pos, dir, speed)` tuples; each tuple represents a pybot that has been found with the last scan request, and contains its name, its position (always an `(x,y)` tuple) and its current travelling direction and speed.

The return value of this function must be a tuple of four elements, which must be:
* direction, expressed in degrees (float or int value from 0 to 360) in which the pybot will travel for the next step;
* speed (integer from 0 to the maximum speed of the pybot) at which the pybot will travel for the next step;
* scanning direction for the next step (see Scanning below);
* list (only a list as the engine will edit it) which contains one element for every shot fired by the pybot for the next step (see SHOOTING below).
Be careful of the length of the tuples and the type contained, because if your routine causes an exception (this includes the applying of the return value which actually happens outside of the act function) your pybot will receive an hit of strength vars.EXCEPTION_COST (the default value is 1000).

When you have created your pybot you can put the file in the `bots` directory and run pybots in single round or tournament mode (see Running Pybots).

## Scanning
Each bot every step can scan in a direction. The scanned area in centred on the direction given and extends clockwise and counter-clockwise from this centre by `10 * scanradius` (or `20 * scanradius` total).

Each pybot which falls in the scanned area will be provided in the next act function call, as specified above.

## Shooting
To fire a shot you can add an element to the list returned by the act function. This element must be a (direction, speed, power) tuple.

Every step the shot advances in the direction and at the speed specified by the tuple, until it exits the arena area or it hits a pybot. In order to a shot to hit its position must be inside the pybot.
A shot can never hit the pybot who fired the shot.

NB: Since every step the engine performs movements for all the pybots and all the shots and THEN checks for hits, it is possible for fast and small bots to go past really fast shots.

## Basic Example
This is a (really basic) example of how a pybot file should be:
```
class bot:
    size = 9
    armour = 1
    maxdamage = 10
    maxspeed = 2
    shotpower = 4
    shotspeed = 4
    scanradius = 3

    def set_arena_data(self, data):
        self.arenaw = data['ARENA_W']
        self.arenah = data['ARENA_H']
        self.walldmg = data['ARENA_WALL_DMG']
        self.round_duration = data['ROUND_DURATION']

    def act(self, data):
        (name, pos, dmg, scanresult) = data
        return (0, 0, 0, [])
```
This pybot just stants still and does nothing, but can be the skeleton of your own pybot. More examples can be found in the "bots" directory.

# Running PyBots
FIXME: How to run PyBots

# Contributing to Development/Roadmap
I am planning to do some cleanup on this codebase and I will likely change the bot APIs/expected arguments/returns. Please feel free to submit issues and pull requests.
Initial plans are as follows:
* Create Abstract Base Class (ABC) for Bot implementations.
* Create a more robust API for creating rounds and tournaments programmatically (e.g. create a tournament via a web backend or a Teams bot!).
* Remove reliance on global variables and move towards more logical OOP.
* Fix spelling errors and make the code more Pythonic (e.g. iterating over a list instead of `range(0, len(list_here))`).
* Create an interactive prompt for creating matches and tournaments in terminal.