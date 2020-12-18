import os
import pygame as pg
from settings import TILESIZE, ANIMATION_SPEED
from typing import List

class Player(pg.sprite.Sprite):
    
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
        MAXHP, ATK, DEF, STAM = 25, 5, 5, 5
        
        # Stats => HP, ATK, DEF
        self.MAXHP = MAXHP
        self.HP = self.MAXHP
        self.ATK = ATK
        self.DEF = DEF
        self.STAM = STAM

    @property
    def position(self) -> List[float]:
        return list(self._position)

    @property
    def _rect(self):
        return self.rect

    @property
    def get_HP(self):
        return self.HP

    # Function assigned to what keys are pressed
    def key_pressed(self):

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

    # Create a list of coordinate according to movement
    def update(self, dt):

        self.temp_list = []
        self.temp_position = self.position
        self.old_position = self.position

        self.key_pressed()

        self.rect_x_temp = self._rect.move((self.temp_position[0]-self.old_position[0]) * TILESIZE, 0)
        self.rect_y_temp = self._rect.move(0, (self.temp_position[1]-self.old_position[1]) * TILESIZE)

    # Receive a list and apply movement present in the list
    def position_update(self, move_list):

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

    # Change player's animation depending on direction
    def animation(self, direction):
    
        # Check player.facing and .anim to give an area in the player's sprite-sheet
        def spritesheet_area(facing, anim):
            
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