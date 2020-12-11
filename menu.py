import os
import sys
import pygame as pg
import pygame_menu as pgm
from usefulfunction import FUNCTION

class MenuFunction():

    def __init__(self):

        self.theme_template = pgm.themes.Theme(
                background_color = (64, 64, 64, 200),
                menubar_close_button = False,
                title_bar_style = pgm.widgets.MENUBAR_STYLE_NONE,
                title_background_color = (0, 0, 0, 0),
                widget_background_color = (38, 38, 38, 150),
                widget_font_color = (242, 242, 242),
                widget_font = os.path.join('Font', 'Roboto-Regular.ttf')
            )

    # Used only for title screen
    # -----------------------------------
    
    def start_new_game(self):
        self.new_game = True
        self.title_screen._enabled = False

    def show_title_screen(self, surface, dirty_surface, screen_size):

        background = pg.image.load(os.path.join('img', 'FieldBG.jpg')).convert_alpha()

        while self.title_screen.is_enabled():

            events = pg.event.get()
            dirty_surface.blit(background, (0, 0))

            for event in events:
                if event.type == pg.QUIT:
                    FUNCTION.quit()
                if event.type == pg.KEYDOWN:
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_ESCAPE:
                            FUNCTION.quit()

                    if event.key == pg.K_F12:

                        if not self.fullscreen_enabled:
                            self.fullscreen_enabled = True
                            surface = pg.display.set_mode(screen_size, pg.FULLSCREEN)
                        else:
                            self.fullscreen_enabled = False   
                            surface = pg.display.set_mode(screen_size)

            self.title_screen.draw(dirty_surface)
            self.title_screen.update(events)
            pg.transform.smoothscale(dirty_surface, surface.get_size(), surface)

            pg.display.flip()
    # -----------------------------------
    
    def toggle(self, menu):
        
        # Reset menu to close sub-menu
        if menu.is_enabled():
            menu.full_reset()
        
        self.menu_pause = not self.menu_pause
        menu.toggle()

    # Reset status menu to update value
    def show_status_menu(self):

        # Remove widget from the menu
        self.StatusMenu.Menu.clear()

        # Fetch data
        self.StatusMenu.player_name = self.StatusMenu.GAME.name
        self.StatusMenu.position = str(self.GAME.player.position[0])

        # Create widget with updated data
        self.StatusMenu.Menu.add_button('Back', pgm.events.BACK)
        self.StatusMenu.Menu.add_label(self.StatusMenu.player_name)
        self.StatusMenu.Menu.add_label(self.StatusMenu.position)

        self.Menu._open(self.StatusMenu.Menu)

    def ShowDB(self, NPCName, IsRandom, Dialogue):

        self.DialogBox = DialogBox()

        # Fetch data
        self.DialogBox.player_name = NPCName

        if IsRandom:
            self.Dialogue = Dialogue
        else:
            for text in Dialogue:
                pass

        self.Menu._open(self.StatusMenu.Menu)
    
    def SaveGame(self):
        print("TODO Save system")

    def LoadSave(self):
        print("TODO continue playing by loading a save")

    def MenuOption(self):
        print("TODO option menu")

    def ExitGame(self):
        FUNCTION.quit()

    def About(self):
        print("TODO about section with information on the game, the creator and library used")

    def Inventory(self):
        print("TODO Inventory system")

    def MenuEquip(self):
        print("TODO Equipment system")

    def MenuStatus(self):
        print("TODO Status profile")

# Need to .toggle then .mainloop(surface)
class TitleScreenMenu(MenuFunction):

    # Create Title
    def __init__(self, GAME):

        super().__init__()

        self.new_game = False
        self.fullscreen_enabled = False

        title_screenTheme = self.theme_template.copy()
        title_screenTheme.background_color = (0, 0, 0, 0)
        title_screenTheme.widget_background_color = (38, 38, 38, 180)
        title_screenTheme.widget_margin = (0, 12)

        self.title_screen = pgm.Menu(
        enabled = True,
        height = 400,
        width = 600,
        onclose = pgm.events.EXIT,
        theme = title_screenTheme,
        title = '',
        menu_position = (50, 100)
        )

        # Initiate sub-menu class
        self.OptionMenu = OptionMenu()

        self.title_screen.add_button('Start new game', self.start_new_game)
        self.title_screen.add_button('     Load Save     ', self.LoadSave)
        self.title_screen.add_button('        Option        ', self.OptionMenu.Menu)
        self.title_screen.add_button('         About         ', self.About)
        self.title_screen.add_button('           Exit           ', self.ExitGame)

class InGameMenu(MenuFunction):

    def __init__(self, GAME):

        super().__init__()

        InGameMenuTheme = self.theme_template.copy()
        InGameMenuTheme.widget_font_size = 35
        InGameMenuTheme.widget_margin = (0, 15)
        InGameMenuTheme.title_font_size = 1

        self.Menu = pgm.Menu(
        enabled = False,
        height = 512,
        width = 320,
        theme = InGameMenuTheme,
        title = '',
        menu_position = (10, 50)
        )

        self.GAME = GAME
        self.OptionMenu = OptionMenu()
        self.StatusMenu = StatusMenu(GAME)

        self.Menu.add_button('         Item         ', self.Inventory)
        self.Menu.add_button('        Equip        ', self.MenuEquip)
        self.Menu.add_button('       Status       ', self.show_status_menu)
        self.Menu.add_button('       Option       ', self.OptionMenu.Menu)
        self.Menu.add_button('         Save         ', self.SaveGame)
        self.Menu.add_button('         Load         ', self.LoadSave)
        self.Menu.add_button('         Quit         ', self.ExitGame)

class OptionMenu(MenuFunction):

    def __init__(self):

        super().__init__()

        OptionMenuTheme = self.theme_template.copy()
        OptionMenuTheme.widget_font_size = 35
        OptionMenuTheme.widget_margin = (0, 25)
        OptionMenuTheme.title_background_color = (0, 0, 0, 100)
        OptionMenuTheme.title_bar_style = pgm.widgets.MENUBAR_STYLE_ADAPTIVE
        OptionMenuTheme.title_offset = (5, -3)
        OptionMenuTheme.title_font_size = 35

        self.Menu = pgm.Menu(
        enabled = False,
        height = 512,
        width = 703,
        theme = OptionMenuTheme,
        title = 'Option',
        menu_position = (50, 50)
        )

        # music / sfx / display / zoom / always sprint / Auto save
        self.Menu.add_button('Back', pgm.events.BACK)
        self.Menu.add_selector('Music Volume', [("0", 0), ("5", 0.5), ("10", 0.1)])
        self.Menu.add_selector('SFX Volume', [("0", 0), ("5", 0.5), ("10", 0.1)])
        self.Menu.add_selector('Display', [("Windowed", False), ("Fullscreen", True)])
        self.Menu.add_selector('Zoom Level', [("0", 0), ("5", 0.5), ("10", 0.1)])
        self.Menu.add_selector('Auto Save', [("Disabled", False), ("Enabled", True)])

class StatusMenu(MenuFunction):

    def __init__(self, GAME):

        super().__init__()

        StatusMenuTheme = self.theme_template.copy()

        self.Menu = pgm.Menu(
        enabled = False,
        height = 640,
        width = 266,
        theme = StatusMenuTheme,
        title = '',
        menu_position = (100, 50)
        )

        self.GAME = GAME

class InventoryMenu(MenuFunction):

    def __init__(self, GAME):

        super().__init__()

        InventoryMenuTheme = self.theme_template.copy()

        self.Menu = pgm.Menu(
        enabled = False,
        height = 512,
        width = 703,
        theme = InventoryMenuTheme,
        title = '',
        menu_position = (50, 50)
        )