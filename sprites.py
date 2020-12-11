import os
import pygame as pg
from settings import TILESIZE, CounterMax
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
        self.Facing = "Down"

    @property
    def position(self) -> List[float]:
        return list(self._position)

    @property
    def GetRect(self):
        return self.rect

    # Function assigned to what keys are pressed
    def KeyPress(self):

        keys = pg.key.get_pressed()
        self.TempVelocity = self.velocity
        self.Sprinting = False

        if keys[pg.K_LSHIFT]:

            self.TempVelocity = self.velocity * 2
            self.Sprinting = True

        if keys[pg.K_LEFT]:
            self.TemPosition[0] -= (round(self.TempVelocity * 0.25, 2)/2)
            self.TemPList.append("Left")
        if keys[pg.K_RIGHT]:
            self.TemPosition[0] += (round(self.TempVelocity * 0.25, 2)/2)
            self.TemPList.append("Right")
        if keys[pg.K_UP]:
            self.TemPosition[1] -= (round(self.TempVelocity * 0.25, 2)/2)
            self.TemPList.append("Up")
        if keys[pg.K_DOWN]:
            self.TemPosition[1] += (round(self.TempVelocity * 0.25, 2)/2)
            self.TemPList.append("Down")

    # Create a list of coordinate according to movement
    def update(self, dt):

        self.TemPList = []
        self.TemPosition = self.position
        self.OldPosition = self.position
        self.OldRect = self.GetRect

        self.KeyPress()

        self.RectXChanged = self.GetRect.move((self.TemPosition[0]-self.OldPosition[0]) * TILESIZE, 0)
        self.RectYChanged = self.GetRect.move(0, (self.TemPosition[1]-self.OldPosition[1]) * TILESIZE)

    # Receive a list and apply movement present in the list
    def PositionUpdate(self, ReceivedList):

        for i in ReceivedList:

            # If element in list apply TemPosition to current position
            if i == "X":
                self._position[0] = self.TemPosition[0]
            else:
                self._position[1] = self.TemPosition[1]

        # Assign surface according to position and TILESIZE then animate the character
        self.rect.x = self._position[0] * TILESIZE
        self.rect.y = self._position[1] * TILESIZE
        self.animation(self.TemPList)

    # Change player's animation depending on direction
    def animation(self, direction):
    
        def AreaToDraw(facing, anim):
            
            offset = TILESIZE
            List = ['Down', 'Left', 'Right', 'Up']

            for direction in List:
                if facing == direction:
                    ID = List.index(direction)
                    break

            if anim == 'Move1':
                offset -= TILESIZE
            elif anim == 'Move2':
                offset += TILESIZE
                
            Area = [offset, ID*TILESIZE]
            return Area

        # Counter for animation, change animation speed in settings (CounterMax)
        self.counter += 1
        AnimationSpeed = CounterMax

        if self.Sprinting:
            AnimationSpeed /= 2
        
        if direction:

            if "Up" in direction:
                self.Facing = "Up"
            elif "Down" in direction:
                self.Facing = "Down"
            elif "Left" in direction:
                self.Facing = "Left"
            elif "Right" in direction:
                self.Facing = "Right"

            if self.counter > AnimationSpeed / 2:
                anim = "Move1"
            else:
                anim = "Move2"
        else:
            anim = "Still"

        # Reset counter
        if self.counter > AnimationSpeed:
            self.counter = 0

        self.SpriteArea = AreaToDraw(self.Facing, anim)
        self.image = pg.image.load(os.path.join('img', 'DefaultPlayer.png')).convert_alpha()
        self.image = self.image.subsurface(pg.Rect(self.SpriteArea[0], self.SpriteArea[1], TILESIZE, TILESIZE))