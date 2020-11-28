import os, sys
import pygame as pg
import pygame_menu as pgm
from usefulfunction import FUNCTION

class MenuFunction():

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
    def __init__(self):

        super().__init__()
        self.NewGame = False
        self.IsFullscreen = False

        TitleScreenTheme = pgm.themes.Theme(
            background_color = (0, 0, 0, 0),
            menubar_close_button = False,
            title_background_color = (0, 0, 0, 0),
            widget_background_color = (38, 38, 38, 180),
            widget_font_color = (242, 242, 242),
            widget_margin = (0, 12)
        )

        self.TitleScreen = pgm.Menu(
        enabled = True,
        height = 400,
        width = 600,
        theme = TitleScreenTheme,
        title = '',
        menu_position = (50, 100)
        )

        self.TitleScreen.add_button('Start new game', self.StartNewGame)
        self.TitleScreen.add_button('     Load Save     ', self.LoadSave)
        self.TitleScreen.add_button('        Option        ', self.MenuOption)
        self.TitleScreen.add_button('         About         ', self.About)
        self.TitleScreen.add_button('           Exit           ', self.ExitGame)

class InGameMenu(MenuFunction):

    def __init__(self):

        super().__init__()

        InGameMenuTheme = pgm.themes.Theme(
            background_color = (64, 64, 64, 200),
            menubar_close_button = False,
            title_background_color = (0, 0, 0, 0),
            widget_background_color = (38, 38, 38, 150),
            widget_font_color = (242, 242, 242),
            widget_font_size = 35,
            widget_margin = (0, 15),
            title_font_size = 1
        )

        self.InGameM = pgm.Menu(
        enabled = False,
        height = 512,
        width = 320,
        theme = InGameMenuTheme,
        title = '',
        menu_position = (10, 50)
        )

        self.InGameM.add_button('         Item         ', self.Inventory)
        self.InGameM.add_button('        Equip        ', self.MenuEquip)
        self.InGameM.add_button('       Status       ', self.MenuStatus)
        self.InGameM.add_button('       Option       ', self.MenuOption)
        self.InGameM.add_button('         Save         ', self.SaveGame)
        self.InGameM.add_button('         Load         ', self.LoadSave)
        self.InGameM.add_button('         Quit         ', self.ExitGame)

    def toggle(self, MENU):
        MENU.enabled = not MENU.enabled