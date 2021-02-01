# Introduction

This is my project of a tile based rpg written in python.  
The game was mostly written with versability in mind, feel free to add content or tweak values.  
You can easily do so by [modifying](https://github.com/Mysterken/TileBasedRPG#addingmodifying-content) files in the data folder.

### Library and programs used:

- [pygame](https://github.com/pygame/pygame)  
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
- __[key_up]__ Move up  
- __[key_left]__ Move left  
- __[key_down]__ Move down  
- __[key_right]__ Move right  

Other key:  
- __[x]__ Open/close pause menu  
- __[spacebar]__ Action (Talk/Check)  
- __[enter-key]__ Select button in menu  
- __[scrollwheel]__ Zoom/Dezoom the map
- __[F12]__ Fullscreen/Windowed
- __[escape]__ Exit game

# Adding/Modifying content

### Enemies
Stored in `Ennemies.json`.  
You can modify or create a new one.  
An enemy should necessarily have those values:  
```
enemy: {
  "name": string,
  "MAXHP": int,
  "DEX": int,
  "ATK": int,
  "DEF": int,
  "STAM": int,
}
```
The enemy can also have those stats, if not given they're set at a default value.  
WIP => Not implemented yet: Optionnal argument  
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

### Items
Stored in `Items.json`.  
Item should have a `desc` and a `type`.  
```
"Item": {
  "desc": "Here should be written the item's description!",
  "type": "item_type"
}
```
Only supported type for now is `heal_item` which require an additionnal `heal_amount` key with a int value.

### NPC dialogue
Stored in `NPCDialog.json`.  
Should be written as a list in pair, with the `text` and the `face` see below:
```
"NPCDialogue": [
  "Here's what the NPC should say!", "desc",
  "Hello i'm an NPC.\nHow are you?", 2
]
```
Result in:  
![alt text](https://i.imgur.com/r0OJ1MP.png) ![alt text](https://i.imgur.com/TRusxCZ.png)  
The face should either be an integer (0-7) or `"desc"`, passing an integer pick a face from the facesheet 
to show on the side of the Dialog box while passing `"desc"` don't show the face and act as a description box.  
You can also break line with `\n` but keep in mind that no more than 3 line should be on the same page to avoid text overflow.  

### Props description
Stored in `PropsDescription.json`.  
Act like NPC dialogue but don't accept the `face`, instead just text.
```
"PropsDescription": [
  "Here is written the description of the props\nHere we break a line.",
  "Here's another page of description."
]
```
![alt text](https://i.imgur.com/Ku9mycl.png) ![alt text](https://i.imgur.com/nOm4pKi.png)  

### Skills
Stored in `Skills.json`.  
The skill should have a `desc`, `type` and `stam_consumption`.  
```
"Powerful Attack": {
  "desc": "A powerful blow dealing massive damage",
  "type": "attack",
  "power": 6,
  "stam_consumption": 4
}
```
Currently supported `type` are `attack` and `heal`.  
If the `type` is `attack`: a `power` key with a int value should be included.  
If the `type` is `heal`: a `heal_amount` key with a int value should be included.  
