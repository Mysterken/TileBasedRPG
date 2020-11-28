import sys
import pygame as pg

# Various useful function, call from here, better code visibility in other file
class FUNCTION():

    def quit(self):
        pg.quit()
        sys.exit()

    # Check if predicted rect X, Y collide with wall or map limit, if so: do not move on it's axis  
    def UpdateAndCollision(self):
    
        # Default axis to change, remove one if collision detected
        ToChangeList = ["X", "Y"]

        for player in self.group.sprites():
            
            if (player.RectXChanged.collidelist(self.walls) > -1 
                or self.player.TemPosition[0] < 0
                or self.player.TemPosition[0] > self.tmx_data.width -1):
                ToChangeList.remove("X")

            if (player.RectYChanged.collidelist(self.walls) > -1 
                or self.player.TemPosition[1] < 0
                or self.player.TemPosition[1] > self.tmx_data.height -1):
                ToChangeList.remove("Y")

        self.player.PositionUpdate(ToChangeList)