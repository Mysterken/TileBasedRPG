import os, sys
import pygame as pg
import pygame_menu as pgm
from usefulfunction import FUNCTION
###############################################
# Plan to make the menu showed from a function show() rather than directly from the class, will prevent __init__ problem
###############################################
class MenuFunction():

    def __init__(self):

        self.ThemeTemplate = pgm.themes.Theme(
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
    
    def StartNewGame(self):
        self.NewGame = True
        self.TitleScreen._enabled = False

    def ShowTS(self, surface, DirtySurface, ScreenSize):

        Background = pg.image.load(os.path.join('img', 'FieldBG.jpg')).convert_alpha()
        BG = Background

        while self.TitleScreen.is_enabled():

            events = pg.event.get()
            DirtySurface.blit(BG, (0, 0))

            for event in events:
                if event.type == pg.QUIT:
                    FUNCTION.quit(self)
                if event.type == pg.KEYDOWN:
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_ESCAPE:
                            FUNCTION.quit(self)

                    if event.key == pg.K_F12:

                        if not self.IsFullscreen:
                            self.IsFullscreen = True
                            surface = pg.display.set_mode(ScreenSize, pg.FULLSCREEN)
                        else:
                            self.IsFullscreen = False   
                            surface = pg.display.set_mode(ScreenSize)

            self.TitleScreen.draw(DirtySurface)
            self.TitleScreen.update(events)
            pg.transform.smoothscale(DirtySurface, surface.get_size(), surface)

            pg.display.flip()
    # -----------------------------------
    
    def toggle(self, MENU):
        
        # Reset menu to close sub-menu
        if MENU.is_enabled():
            MENU.full_reset()
        
        self.GamePaused = not self.GamePaused
        MENU.toggle()

    # Reset status menu to update value
    def ShowStatus(self):

        # Remove widget from the menu
        self.StatusMenu.Menu.clear()

        # Fetch data
        self.StatusMenu.NAME = self.StatusMenu.GAME.name
        self.StatusMenu.position = str(self.GAME.player._position[0])

        # Create widget with updated data
        self.StatusMenu.Menu.add_button('Back', pgm.events.BACK)
        self.StatusMenu.Menu.add_label(self.StatusMenu.NAME)
        self.StatusMenu.Menu.add_label(self.StatusMenu.position)

        self.Menu._open(self.StatusMenu.Menu)

    def ShowDB(self, NPCName, IsRandom, Dialogue):

        self.DialogBox = DialogBox()

        # Fetch data
        self.DialogBox.NAME = NPCName

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

    def CloseMenu(self):
        self._enabled = False

    def ExitGame(self):
        FUNCTION.quit(self)

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

        self.NewGame = False
        self.IsFullscreen = False

        TitleScreenTheme = self.ThemeTemplate.copy()
        TitleScreenTheme.background_color = (0, 0, 0, 0)
        TitleScreenTheme.widget_background_color = (38, 38, 38, 180)
        TitleScreenTheme.widget_margin = (0, 12)

        self.TitleScreen = pgm.Menu(
        enabled = True,
        height = 400,
        width = 600,
        onclose = pgm.events.EXIT,
        theme = TitleScreenTheme,
        title = '',
        menu_position = (50, 100)
        )

        # Initiate sub-menu class
        self.OptionMenu = OptionMenu()

        self.TitleScreen.add_button('Start new game', self.StartNewGame)
        self.TitleScreen.add_button('     Load Save     ', self.LoadSave)
        self.TitleScreen.add_button('        Option        ', self.OptionMenu.Menu)
        self.TitleScreen.add_button('         About         ', self.About)
        self.TitleScreen.add_button('           Exit           ', self.ExitGame)

class InGameMenu(MenuFunction):

    def __init__(self, GAME):

        super().__init__()

        InGameMenuTheme = self.ThemeTemplate.copy()
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
        self.Menu.add_button('       Status       ', self.ShowStatus)
        self.Menu.add_button('       Option       ', self.OptionMenu.Menu)
        self.Menu.add_button('         Save         ', self.SaveGame)
        self.Menu.add_button('         Load         ', self.LoadSave)
        self.Menu.add_button('         Quit         ', self.ExitGame)

class OptionMenu(MenuFunction):

    def __init__(self):

        super().__init__()

        OptionMenuTheme = self.ThemeTemplate.copy()
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

        StatusMenuTheme = self.ThemeTemplate.copy()

        self.Menu = pgm.Menu(
        enabled = False,
        height = 640,
        width = 266,
        theme = StatusMenuTheme,
        title = '',
        menu_position = (100, 50)
        )

        self.GAME = GAME

class DialogBox(MenuFunction):

    def __init__(self):

        super().__init__()

        DialogBoxTheme = self.ThemeTemplate.copy()

        self.Menu = pgm.Menu(
        enabled = False,
        height = 640,
        width = 266,
        theme = DialogBoxTheme,
        title = '',
        menu_position = (100, 50)
        )