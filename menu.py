import os
import sys
import pygame as pg
import pygame_menu as pgm
from usefulfunction import FUNCTION

class MenuFunction:

    def __init__(self):

        "Default template for menu theme."

        self.theme_template = pgm.themes.Theme(
                background_color = (64, 64, 64, 200),
                menubar_close_button = False,
                title_bar_style = pgm.widgets.MENUBAR_STYLE_NONE,
                title_background_color = (0, 0, 0, 0),
                widget_background_color = (38, 38, 38, 150),
                background_inflate = (16, 8),
                widget_font_color = (242, 242, 242),
                widget_font = os.path.join('Font', 'Roboto-Regular.ttf')
            )
    
    def toggle(self, menu):

        "Toggle the menu."
        
        # Reset menu to close sub-menu
        if menu.is_enabled():
            menu.full_reset()
        
        self.menu_pause = not self.menu_pause
        menu.toggle()

    def SaveGame(self):
        FUNCTION.create_save(self.GAME)

    def LoadSave(self):
        FUNCTION.load_save(self.GAME)

    def ExitGame(self):
        FUNCTION.quit()

    def About(self):
        print("TODO about section with information on the game, the creator and library used")

    def MenuEquip(self):
        print("TODO Equipment system")

    def MenuStatus(self):
        print("TODO Status profile")

# Need to .toggle then .mainloop(surface)
class TitleScreenMenu(MenuFunction):

    "Title Screen menu."

    # Create Title
    def __init__(self, GAME):

        super().__init__()

        self.GAME = GAME
        self.new_game = False
        self.fullscreen_enabled = False

        title_screenTheme = self.theme_template.copy()
        title_screenTheme.background_color = (0, 0, 0, 0)
        title_screenTheme.widget_background_color = (38, 38, 38, 180)
        title_screenTheme.widget_margin = (12, 12)

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
        self.BattleMenu = BattleMenu()

        self.title_screen.add_button('Start new game', self.start_new_game)
        self.title_screen.add_button('Load Save', self.load_save, padding=(0, 36, 0, 35))
        self.title_screen.add_button('Option', self.OptionMenu.Menu, padding=(0, 60, 0, 60))
        self.title_screen.add_button('About', self.About, padding=(0, 64, 0, 64))
        self.title_screen.add_button('Exit', self.ExitGame, padding=(0, 80, 0, 80))

    def start_new_game(self):

        "Initiate a new game."

        self.new_game = True
        self.title_screen._enabled = False

    def load_save(self):

        "Load a save from the save folder, the file should be game_save"

        self.title_screen._enabled = False
        self.LoadSave()

    def show_title_screen(self, surface, dirty_surface, screen_size):

        "Display the title screen, pygame events are processed within the function."

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
                            surface = pg.display.set_mode(screen_size, pg.FULLSCREEN)
                        else:
                            surface = pg.display.set_mode(screen_size)
                        self.fullscreen_enabled = not self.fullscreen_enabled

            self.title_screen.draw(dirty_surface)
            self.title_screen.update(events)
            pg.transform.smoothscale(dirty_surface, surface.get_size(), surface)

            pg.display.flip()

class InGameMenu(MenuFunction):

    "Menu displayed In-Game whenever the game is paused"

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
        self.InventoryMenu = InventoryMenu(GAME)

        self.Menu.add_button('Item', self.show_inventory_menu, padding=(0, 75, 0, 75))
        self.Menu.add_button('Equip', self.MenuEquip, padding=(0, 66, 0, 67))
        self.Menu.add_button('Status', self.show_status_menu, padding=(0, 61, 0, 61))
        self.Menu.add_button('Option', self.OptionMenu.Menu, padding=(0, 59, 0, 59))
        self.Menu.add_button('Save', self.SaveGame, padding=(0, 72, 0, 73))
        self.Menu.add_button('Load', self.LoadSave, padding=(0, 71, 0, 72))
        self.Menu.add_button('Quit', self.ExitGame, padding=(0, 79, 0, 79))

    def show_inventory_menu(self):

        "Display the inventory menu."

        # Remove item and reset the inventory data
        def use_item(item):

            "Use and remove the passed item from the inventory."

            self.GAME.use_item(item)
            self.GAME.inventory.remove_item(item)
            self.show_inventory_menu()
       
        self.InventoryMenu.Menu.clear()
        self.InventoryMenu.item_list = []

        # Dynamically adjust row count to fit items
        item_count = len(self.InventoryMenu.GAME.inventory.content)
        if item_count % 2 != 0:
            item_count += 1
        self.InventoryMenu.Menu._rows = round(item_count/2)

        # Add items to the Menu
        for item in self.InventoryMenu.GAME.inventory.content:

            self.InventoryMenu.Menu.add_button(item, use_item, item)
            self.InventoryMenu.item_list.append(item)
        # TODO: check Menu._select to force select an item and not reset each time
        self.Menu._open(self.InventoryMenu.Menu)

    def show_status_menu(self):

        "Display the status menu."

        # Remove widget from the menu
        self.StatusMenu.Menu.clear()

        # Fetch data
        player_name = self.StatusMenu.GAME.player.name
        player_maxhp = str(self.StatusMenu.GAME.player.MAXHP)
        player_hp = str(self.StatusMenu.GAME.player.HP)
        player_atk = str(self.StatusMenu.GAME.player.ATK)
        player_def = str(self.StatusMenu.GAME.player.DEF)
        player_dex = str(self.StatusMenu.GAME.player.DEX)
        player_stam = str(self.StatusMenu.GAME.player.STAM)

        # Create widget with updated data
        self.StatusMenu.Menu.add_button('Back', pgm.events.BACK)
        self.StatusMenu.Menu.add_label(player_name)
        self.StatusMenu.Menu.add_label(player_maxhp + 'HP / ' + player_hp + 'HP')
        self.StatusMenu.Menu.add_label("ATK: " + player_atk)
        self.StatusMenu.Menu.add_label("DEF: " + player_def)
        self.StatusMenu.Menu.add_label("DEXTERITY: " + player_dex)
        self.StatusMenu.Menu.add_label("STAMINA: " + player_stam)

        self.Menu._open(self.StatusMenu.Menu)

class OptionMenu(MenuFunction):

    "Option menu."

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

        # Only for display as of now except for "Back"
        self.Menu.add_button('Back', pgm.events.BACK)
        self.Menu.add_selector('Music Volume', [("0", 0), ("5", 0.5), ("10", 0.1)])
        self.Menu.add_selector('SFX Volume', [("0", 0), ("5", 0.5), ("10", 0.1)])
        self.Menu.add_selector('Display', [("Windowed", False), ("Fullscreen", True)])
        self.Menu.add_selector('Zoom Level', [("0", 0), ("5", 0.5), ("10", 0.1)])
        self.Menu.add_selector('Auto Save', [("Disabled", False), ("Enabled", True)])

class StatusMenu(MenuFunction):

    "Status menu."

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

    "Inventory menu."

    def __init__(self, GAME):

        super().__init__()

        InventoryMenuTheme = self.theme_template.copy()
        InventoryMenuTheme.widget_margin = (0, 15)
        InventoryMenuTheme.widget_alignment = pgm.locals.ALIGN_LEFT
        InventoryMenuTheme.widget_offset = (15, 15)
        InventoryMenuTheme.title_font_size = 128
        InventoryMenuTheme.title_bar_style = pgm.widgets.MENUBAR_STYLE_SIMPLE
        InventoryMenuTheme.title_background_color = (0, 0, 0, 90)

        self.Menu = pgm.Menu(
        enabled = False,
        center_content = False,
        height = 512,
        width = 703,
        columns = 2,
        rows = 1,
        theme = InventoryMenuTheme,
        title = '',
        menu_position = (50, 50)
        )

        self.GAME = GAME

    def item_desc(self):

        "Fetch the description of the item pointed and return it."
        
        text = []
        if self.item_list:
            
            desc = FUNCTION.fetch_item_desc(self.item_list[self.Menu.get_index()]).split('\n')
            for line in desc:

                text_surface = FUNCTION.font_render(self.GAME, line)
                text.append(text_surface)
        else:
            text = [FUNCTION.font_render(self.GAME, "")]
        return text

class BattleMenu(MenuFunction):

    "Battle menu to select the player's action during the fight."

    def __init__(self):

        super().__init__()

        BattleMenuTheme = self.theme_template.copy()
        BattleMenuTheme.widget_margin = (0, 15)
        BattleMenuTheme.title_font_size = 1

        self.Menu = pgm.Menu(
            enabled = False,
            height = 200,
            width = 300,
            columns = 2,
            rows = 3,
            column_max_width = [1, 1],
            theme = BattleMenuTheme,
            title = '',
            menu_position = (0, 100)
        )

        self.sent_action = None

        self.Menu.add_button('Attack', self.attack, padding=(0, 4, 0, 4))
        self.Menu.add_button('Skill', self.skill, padding=(0, 21, 0, 21))
        self.Menu.add_button('Defend', self.defend)
        self.Menu.add_button('Wait', self.wait, padding=(0, 18, 0, 18))
        self.Menu.add_button('Item', self.About, padding=(0, 18, 0, 18))
        self.Menu.add_button('Run', self.run, padding=(0, 22, 0, 22))

    def attack(self):
        
        self.sent_action = "Attack"

    def skill(self):

        print("TODO skill handling")

    def defend(self):

        print("TODO Defend")

    def wait(self):

        self.sent_action = "Wait"

    def item(self):

        print("TODO item handling")

    def run(self):

        self.sent_action = "Run"