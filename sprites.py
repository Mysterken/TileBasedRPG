import os
import pygame as pg
from settings import TILESIZE, ANIMATION_SPEED
from typing import List
from usefulfunction import FUNCTION

class Player(pg.sprite.Sprite):

    "Player class: this is the player you control"
    
    def __init__(self):

        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(os.path.join('img', 'DefaultPlayer.png')).convert_alpha()
        self.image = self.image.subsurface(pg.Rect(TILESIZE, 0, TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.velocity = 1
        self._position = [0, 0]
        self.counter = 0
        self.facing = "Down"

        # Temporary hard coded stats / might change to definable starting stats
        self.name = "Dummy Name"
        MAXHP, DEX, ATK, DEF, STAM = 25, 5, 5, 5, 5
        
        # Stats => HP, ATK, DEF
        self.MAXHP = MAXHP
        self.HP = self.MAXHP
        self.DEX = DEX
        self.ATK = ATK
        self.DEF = DEF
        self.STAM = STAM

        self.escaped = False

    @property
    def position(self) -> List[float]:

        "Return the player's coordinate."

        return list(self._position)

    @property
    def _rect(self):

        "Return the player's pygame rect."

        return self.rect

    @property
    def get_HP(self):

        "Return the player's HP"

        return self.HP

    def lose_HP(self, amount):

        "Deduct an amount from the player's HP"

        if self.HP - amount <= 0:
            self.HP = 0
        else:
            self.HP -= amount

    def gain_HP(self, amount):

        "Add an amount to the player's HP"

        if self.HP + amount >= self.MAXHP:
            self.HP = self.MAXHP
        else:
            self.HP += amount
            
    def key_pressed(self):

        "Function assigned to what keys are pressed"

        keys = pg.key.get_pressed()
        self.temp_velocity = self.velocity
        self.sprinting = False

        if keys[pg.K_LSHIFT]:

            self.temp_velocity = self.velocity * 2
            self.sprinting = True

        if keys[pg.K_LEFT]:
            self.temp_position[0] -= (round(self.temp_velocity * 0.25, 2)/2)
            self.temp_list.append("Left")
        if keys[pg.K_RIGHT]:
            self.temp_position[0] += (round(self.temp_velocity * 0.25, 2)/2)
            self.temp_list.append("Right")
        if keys[pg.K_UP]:
            self.temp_position[1] -= (round(self.temp_velocity * 0.25, 2)/2)
            self.temp_list.append("Up")
        if keys[pg.K_DOWN]:
            self.temp_position[1] += (round(self.temp_velocity * 0.25, 2)/2)
            self.temp_list.append("Down")

    def update(self, dt):

        "Update the player"

        self.temp_list = []
        self.temp_position = self.position
        self.old_position = self.position

        self.key_pressed()

        # Create a list of coordinate according to movement
        self.rect_x_temp = self._rect.move((self.temp_position[0]-self.old_position[0]) * TILESIZE, 0)
        self.rect_y_temp = self._rect.move(0, (self.temp_position[1]-self.old_position[1]) * TILESIZE)

    def position_update(self, move_list):

        "Receive a list and apply movement present in the list"

        for i in move_list:

            # If element in list apply temp_position to current position
            if i == "X":
                self._position[0] = self.temp_position[0]
            else:
                self._position[1] = self.temp_position[1]

        # Assign surface according to position and TILESIZE then animate the character
        self.rect.x = self._position[0] * TILESIZE
        self.rect.y = self._position[1] * TILESIZE
        self.animation(self.temp_list)

    def animation(self, direction):

        "Change player's animation depending on direction"

        def spritesheet_area(facing, anim):

            "Check player.facing and .anim to give an area in the player's sprite-sheet"
            
            offset = TILESIZE
            direction_list = ['Down', 'Left', 'Right', 'Up']

            for direction in direction_list:
                if facing == direction:
                    ID = direction_list.index(direction)
                    break

            if anim == 'Move1':
                offset -= TILESIZE
            elif anim == 'Move2':
                offset += TILESIZE
                
            area = [offset, ID*TILESIZE]
            return area

        # Counter for animation, change animation speed in settings (ANIMATION_SPEED)
        self.counter += 1
        anim_speed = ANIMATION_SPEED

        if self.sprinting:
            anim_speed /= 2
        
        if direction:

            if "Up" in direction:
                self.facing = "Up"
            elif "Down" in direction:
                self.facing = "Down"
            elif "Left" in direction:
                self.facing = "Left"
            elif "Right" in direction:
                self.facing = "Right"

            if self.counter > anim_speed / 2:
                anim = "Move1"
            else:
                anim = "Move2"
        else:
            anim = "Still"

        # Reset counter
        if self.counter > anim_speed:
            self.counter = 0

        self.sprite_area = spritesheet_area(self.facing, anim)
        self.image = pg.image.load(os.path.join('img', 'DefaultPlayer.png')).convert_alpha()
        self.image = self.image.subsurface(pg.Rect(self.sprite_area[0], self.sprite_area[1], TILESIZE, TILESIZE))

    def dead(self):
        
        "Return whether or not the player is dead"
        
        if self.HP <= 0:
            return True
        return False

    def do_action(self, action):

        "Make the player perform the given skill"
        
        if action == "Run":
            self.escaped = True
            return
        
        elif action == "Wait":
            return

        return FUNCTION.skill(action)
    
    def in_fight(self):
        
        if self.dead() or self.escaped:
            return False
        return True