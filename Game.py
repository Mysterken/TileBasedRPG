import os
import sys
import pygame as pg
import sprites
import pyscroll, pyscroll.data
from menu import MenuFunction, TitleScreenMenu, InGameMenu
from pyscroll.group import PyscrollGroup
from sprites import Player
from settings import WIDTH, HEIGHT, FPS, TITLE, TILESIZE
from pytmx.util_pygame import load_pygame
from usefulfunction import FUNCTION
from inventory import Inventory

class Game(FUNCTION):

    def __init__(self):

        # Set the display
        self.FPSCap = pg.time.Clock()
        self.screen_size = [WIDTH, HEIGHT]
        self.screen = pg.display.set_mode(self.screen_size)
        self.dirty_screen = self.screen.copy()
        self.fullscreen_enabled = False
        self.Font = pg.font.Font(os.path.join('Font', 'Roboto-Regular.ttf'), 30)
        self.MF = MenuFunction()
        self.IGM = InGameMenu(self)
        self.action_pause = False
        self.menu_pause = False
        self.dialog_enabled = False
        self.inventory = Inventory()

        pg.display.set_caption(TITLE)

    # Create a new game
    def new(self):

        # Choose a map for new game and load it
        self.NG_map = os.path.join('map', 'Map1.tmx')
        self.load_map(self.NG_map)

        self.player = Player()

        # Set player's spawn position
        self.player._position = self.spawn_point

        # Add player to the group
        self.group.add(self.player)       

    # Load given map to display
    def load_map(self, MAP):

        # Load data from pytmx
        self.tmx_data = load_pygame(MAP)

        self.spawn_point = self.tmx_data.get_object_by_name("SpawnPoint")
        self.spawn_point = [self.spawn_point.x / TILESIZE, self.spawn_point.y / TILESIZE]

        # Setup level geometry with simple pygame rects, loaded from pytmx, walls are based on "Obstacle" object layer
        self.walls = []
        Obstacle = self.tmx_data.get_layer_by_name("Obstacle")
        for obj in Obstacle:
            self.walls.append(pg.Rect(obj.x, obj.y, obj.width, obj.height))

        # Setup Interactive object for action
        self.interactive_object, self.IO_list = [], []
        self.IObj = self.tmx_data.get_layer_by_name("InteractiveObject")
        for obj in self.IObj:
            self.interactive_object.append([round(obj.x / TILESIZE), round(obj.y / TILESIZE), obj.name, obj.id])
            self.IO_list.append([obj.id, obj.properties.copy()])

        # Create new data source for pyscroll
        map_data = pyscroll.data.TiledMapData(self.tmx_data)

        # Create the camera by BufferedRenderer class
        self.map_layer = pyscroll.BufferedRenderer(
            map_data, self.dirty_screen.get_size(), clamp_camera=True, tall_sprites=1
        )
        self.map_layer.zoom = 1.5

        self.group = PyscrollGroup(map_layer=self.map_layer, default_layer=4)

    # Main loop for the game
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

    def events(self):

        self.events_list = pg.event.get()

        # Catch all events here
        for event in self.events_list:

            # Quit if:
            if event.type == pg.QUIT:
                FUNCTION.quit()
            
            if event.type == pg.KEYDOWN:

                if event.key == pg.K_ESCAPE:
                    FUNCTION.quit()

                if event.key == pg.K_x:

                    if not self.action_pause:
                        MenuFunction.toggle(self, self.IGM.Menu)

                if event.key == pg.K_SPACE:
                    if not self.IGM.Menu.is_enabled():
                        self.check_action()

                if event.key == pg.K_F12:

                    if not self.fullscreen_enabled:
                        self.screen = pg.display.set_mode(self.screen_size, pg.FULLSCREEN)
                    else: 
                        self.screen = pg.display.set_mode(self.screen_size)
                    self.fullscreen_enabled = not self.fullscreen_enabled

            # Zoom and dezoom
            if event.type == pg.MOUSEBUTTONDOWN:
                
                if event.button == 4:
                    self.map_layer.zoom += 0.1
                elif event.button == 5:
                    self.map_layer.zoom -= 0.1
    
    def update(self, dt):

        # If the In-game menu is enabled don't update the game, only the menu
        if self.menu_pause:
            self.IGM.Menu.update(self.events_list)
            return

        # Tasks that occur over time are handled here
        self.group.update(dt)

        # If an action is in place don't update player movement
        if not self.action_pause:
            # Move player while taking in account collision
            self.collision_update()

    def draw(self):

        # Center player
        self.group.center(self.player.rect.center)

        # Draw the map and all sprites
        self.group.draw(self.dirty_screen)

        # If an action is in place
        if self.action_pause:

            # Draw dialog box
            if self.dialog_enabled:

                self.dirty_screen.blit(self.box, (11.5, 438.5))

                # Text position according to if it's 'only_text' or not
                text_position = [200, 455] if not self.only_text else [50, 440]

                # Draw each line under the previous one
                for line in self.dialog[self.current_page-1]:
                    text_position[1] += 35
                    self.dirty_screen.blit(line, text_position)

                # Add face image and name to the box if it's an NPC dialogue and not 'only_text'
                if self.NPC_dialogue and not self.only_text:
                    
                    self.dirty_screen.blit(self.NPC_face, (33, 461))
                    self.dirty_screen.blit(self.NPC_name, (200, 450))


        # Darken the screen and display the menu
        elif self.IGM.Menu.is_enabled():

            darken = pg.Surface(self.screen_size)
            darken.set_alpha(130)
            darken.fill((0,0,0))

            self.dirty_screen.blit(darken, (0,0))
            self.IGM.Menu.draw(self.dirty_screen)

        # Draw screen from the dirty_screen and scale if Fullscreen
        if self.fullscreen_enabled:
            pg.transform.smoothscale(self.dirty_screen, self.screen.get_size(), self.screen)
        else:
            self.screen.blit(self.dirty_screen, (0, 0))

# Initiate pygame
pg.init()

# Run the game
g = Game()

# Title screen launch and import new_game state
TS = TitleScreenMenu(g)
TS.show_title_screen(g.screen, g.dirty_screen, g.screen_size)

# If a new game is launched set everythings
if TS.new_game:
    g.new()

while True:
    g.main()