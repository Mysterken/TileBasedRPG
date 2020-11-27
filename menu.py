import os, sys
import pygame as pg
import pygame_menu as pgm

class MenuFunction():

    def SaveGame(self):
        print("TODO Save system")

    def LoadSave(self):
        print("TODO continue playing by loading a save")

    def Option(self):
        print("TODO option menu")

    def CloseMenu(self):
        self._enabled = False

    def ExitGame(self):
        pg.quit()
        sys.exit()

    def About(self):
        print("TODO about section with information on the game, the creator and library used")
        

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
            widget_font_color = (242, 242, 242)
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
        self.TitleScreen.add_button('Load Save', self.LoadSave)
        self.TitleScreen.add_button('Option', self.Option)
        self.TitleScreen.add_button('About', self.About)
        self.TitleScreen.add_button('Exit', self.ExitGame)

    def StartNewGame(self):
        
        self.NewGame = True
        self.TitleScreen._enabled = False

    def Show(self, surface, DirtySurface, ScreenSize):

        Background = pg.image.load(os.path.join('img', 'FieldBG.jpg')).convert_alpha()
        BG = Background

        while self.TitleScreen.is_enabled():
    
            events = pg.event.get()
            DirtySurface.blit(BG, (0, 0))
            
            for event in events:
                if event.type == pg.QUIT:
                    self.ExitGame()
                if event.type == pg.KEYDOWN:
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_ESCAPE:
                            pg.quit()
                            sys.exit()
                    
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

class InGameMenu(MenuFunction):

    def __init__(self):
        pass