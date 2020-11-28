import os, sys
import pygame as pg
import tilerender
import sprites
import pyscroll, pyscroll.data
from pyscroll.group import PyscrollGroup
from sprites import Player
from menu import MenuFunction, TitleScreenMenu, InGameMenu
from pygame.locals import *
from settings import WIDTH, HEIGHT, FPS, TITLE, TILESIZE
from pytmx.util_pygame import load_pygame
from usefulfunction import FUNCTION

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
        
        self.SpawnPoint = self.tmx_data.get_object_by_name("SpawnPoint")
        self.SpawnPoint = [self.SpawnPoint.x / 32, self.SpawnPoint.y / 32]
        
        # Setup level geometry with simple pygame rects, loaded from pytmx
        self.walls = []
        Obstacle = self.tmx_data.get_layer_by_name("Obstacle")
        for obj in Obstacle:
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
        self.player._position = self.SpawnPoint

        # Add player to the group
        self.group.add(self.player)

        # Create menu
        self.IGM = InGameMenu()

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
        
        # If the In-game menu is enabled don't update the game, only the menu
        if self.IGM.InGameM.is_enabled():
            self.IGM.InGameM.update(self.EventsList)
            return
        
        # Tasks that occur over time are handled here
        self.group.update(dt)
        
        # Move player while taking in account collision
        #self.player.MoveUpdate()
        FUNCTION.UpdateAndCollision(self)
                         
    def draw(self):

        # Center player
        self.group.center(self.player.rect.center)

        # Draw the map and all sprites
        self.group.draw(self.DirtyScreen)  

        if self.IGM.InGameM.is_enabled():

            # Darken the screen and display the menu
            darken = pg.Surface(self.ScreenSize)
            darken.set_alpha(130)
            darken.fill((0,0,0))

            self.DirtyScreen.blit(darken, (0,0))
            self.IGM.InGameM.draw(self.DirtyScreen)

        # Draw screen from the DirtyScreen and scale if Fullscreen
        if self.IsFullscreen:
            pg.transform.smoothscale(self.DirtyScreen, self.Screen.get_size(), self.Screen)
        else:
            self.Screen.blit(self.DirtyScreen, (0, 0))
        
    def events(self):

        self.EventsList = pg.event.get()

        # Catch all events here
        for event in self.EventsList:
            
            # Quit if:
            if event.type == pg.QUIT:
                FUNCTION.quit(self)
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    FUNCTION.quit(self)
                if event.key == pg.K_x:
                    self.IGM.InGameM.toggle()
                if event.key == pg.K_F12:
                    
                    if not self.IsFullscreen:
                        self.Screen = pg.display.set_mode(self.ScreenSize, pg.FULLSCREEN)
                    else: 
                        self.Screen = pg.display.set_mode(self.ScreenSize)
                    self.IsFullscreen = not self.IsFullscreen
            
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
TS.ShowTS(g.Screen, g.DirtyScreen, g.ScreenSize)

# If a new game is launched
if TS.NewGame:
    g.new()

while True:
    g.main()