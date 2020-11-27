import os, sys
import pygame as pg
import tilerender
import sprites
import pyscroll, pyscroll.data
from pyscroll.group import PyscrollGroup
from sprites import Player
from menu import MenuFunction, TitleScreenMenu
from pygame.locals import *
from settings import WIDTH, HEIGHT, FPS, TITLE, TILESIZE
from pytmx.util_pygame import load_pygame

class Game:
    
    def __init__(self):       
        
        pg.init()

        # Set the display
        self.FPSCap = pg.time.Clock()
        self.ScreenSize = [WIDTH, HEIGHT]
        self.Screen = pg.display.set_mode(self.ScreenSize)
        self.DirtyScreen = self.Screen.copy()
        self.IsFullscreen = False
        pg.display.set_caption(TITLE)

    # Load given map to display
    def LoadData(self, MAP):
        
        # Load data from pytmx
        self.tmx_data = load_pygame(MAP)

        # Setup level geometry with simple pygame rects, loaded from pytmx
        self.walls = []
        for obj in self.tmx_data.objects:
            self.walls.append(pg.Rect(obj.x, obj.y, obj.width, obj.height))

        # Create new data source for pyscroll
        map_data = pyscroll.data.TiledMapData(self.tmx_data)

        # Create the camera by BufferedRenderer class
        self.map_layer = pyscroll.BufferedRenderer(
            map_data, self.DirtyScreen.get_size(), clamp_camera=True, tall_sprites=1
        )
        self.map_layer.zoom = 1.5

        self.group = PyscrollGroup(map_layer=self.map_layer, default_layer=4) 

    # Create a new game
    def new(self):
        
        # Choose a map for new game and load it
        self.MapChosen = "Map1.tmx"
        self.LoadData(self.MapChosen)
        
        self.player = Player()

        # Set player's spawn position
        self.player._position[0] += 12
        self.player._position[1] += 10

        # Add player to the group
        self.group.add(self.player)
 
    def main(self):

        while True:
            
            dt = self.FPSCap.tick(FPS) / 1000

            # Event handler
            self.events()

            # Update
            self.update(dt)

            # Display
            self.draw()
            pg.display.flip()

    def quit(self):      
        pg.quit()
        sys.exit()
    
    def update(self, dt):   
        
        # Tasks that occur over time are handled here
        self.group.update(dt)
        
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
        
        # Move player while taking in account collision
        #self.player.MoveUpdate()
        UpdateAndCollision(self)
                             
    def draw(self):
        
        # Center player
        self.group.center(self.player.rect.center)

        # Draw the map and all sprites
        self.group.draw(self.DirtyScreen)

        # Draw screen from the DirtyScreen and scale if Fullscreen
        if self.IsFullscreen:
            pg.transform.smoothscale(self.DirtyScreen, self.Screen.get_size(), self.Screen)
        else:
            self.Screen.blit(self.DirtyScreen, (0, 0))
        

    def events(self):

        # Catch all events here
        for event in pg.event.get():

            # Quit if:
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_F12:
                    
                    if not self.IsFullscreen:
                        self.IsFullscreen = True
                        self.Screen = pg.display.set_mode(self.ScreenSize, pg.FULLSCREEN)
                    else:
                        self.IsFullscreen = False   
                        self.Screen = pg.display.set_mode(self.ScreenSize)
            
            # Zoom and dezoom
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 4:
                    self.map_layer.zoom += 0.1
                elif event.button == 5:
                    self.map_layer.zoom -= 0.1

# Run the game
g = Game()

# Title screen launch
TS = TitleScreenMenu()
TS.Show(g.Screen, g.DirtyScreen, g.ScreenSize)

# If a new game is launched
if TS.NewGame:
    g.new()

while True:
    g.main()