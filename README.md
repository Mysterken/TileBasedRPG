# Introduction

This is my project of a tile based rpg written in python.  
The game was mostly written with versability in mind, feel free to add content or tweak values.  
You can easily do so by modifying files in the data folder.

### Library and programs used:

- [pygame](https://www.pygame.org/news)   
- [PyTMX](https://github.com/bitcraft/pytmx)  
- [pyscroll](https://github.com/bitcraft/pyscroll)  
- [pygame-menu](https://github.com/ppizarror/pygame-menu)  
- [Tiled](https://www.mapeditor.org/) 

### Ressource:

- [moonwind](http://moonwind.pw/index.html)  
- [pipoya](https://pipoya.net/blog/)  
- [yuuhina](https://blog.goo.ne.jp/akarise)

# Installation

Clone or download the repository and install all the Library (Tiled is not necesary).  
pygame v2+ needed  
pygame-menu v3.4.4+ needed.  

# How to play

### Launching the game

Launch Game.py to play the game

### Controls

Move the player with:  
- __[z]__ Move up  
- __[q]__ Move left  
- __[s]__ Move down  
- __[d]__ Move right  

Other key:  
- __[x]__ Open/close pause menu  
- __[spacebar]__ Action (Talk/Check)  
- __[enter-key]__ Select button in menu  
- __[scrollwheel]__ Zoom/Dezoom the map
- __[F12]__ Fullscreen/Windowed
- __[echap]__ Exit game

# Adding/Modifying content

### Ennemies
Stored in `Ennemies.json`.  
You can modify or create a new one.  
An ennemy should necessarely have those values:  
```
ennemy: {
  "name": string,
  "MAXHP": int,
  "DEX": int,
  "ATK": int,
  "DEF": int,
  "STAM": int,
}
```
WIP => Not immplemented yet: Optionnal argument
```
runnaway : int : Rate at which the ennemy run from the fight
randomize : int : Randomize attribute in this range point
hit_rate : int : Rate of hitting player
dodge_rate : int : Rate of dodging the player's attack
crit_rate : int : Rate of a critical hit
exp_drop : [int, int] : Amount of XP dropped
item_drop : string : Item(s) dropped
gold_drop : int : Amount of gold(s) dropped
skills_list : [string, string] : string list of ennemy's skill
```
