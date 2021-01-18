import os
import sys
import json
import pickle
import pygame as pg
from settings import TILESIZE

class FUNCTION:

    "Various useful function, call from here, better code visibility in other file"

    @staticmethod
    def quit():

        "Exit the game."

        pg.quit()
        sys.exit()

    def load_ressource(self):

        "Load various ressource once to avoid needing to later."

        pp = pg.image.load(os.path.join('img', 'DefaultPlayerPortrait.png')).convert_alpha()
        self.player_portrait = pg.transform.smoothscale(pp, (425, 425))

        self.darken = pg.Surface(self.screen_size)
        self.darken.set_alpha(130)
        self.darken.fill((0,0,0))

        self.extended_bar = pg.Surface((500, 200))
        self.extended_bar.set_alpha(200)
        self.extended_bar.fill((64,64,64))

        self.black_bar = pg.Surface((780, 180))
        self.black_bar.set_alpha(200)
        self.black_bar.fill((64,64,64))

        self.box = pg.image.load(os.path.join('img', 'DialogBox.png')).convert_alpha()
        self.box.set_alpha(235)

        self.smallbox = pg.transform.smoothscale(self.box, (400, 80))

        self.plain_battlefield = pg.image.load(os.path.join('img', 'PlainBattlefield.png')).convert_alpha()

        self.Font = pg.font.Font(os.path.join('Font', 'Roboto-Regular.ttf'), 30)
        self.name_font = pg.font.Font(os.path.join('Font', 'Roboto-Regular.ttf'), 25)
        self.objective_font = pg.font.Font(os.path.join('Font', 'Roboto-Regular.ttf'), 15)

        line1 = self.objective_font.render("Code this fucking game.", True, (255, 255, 255))
        line2 = self.objective_font.render("Like, seriously...", True, (255, 255, 255))
        self.co = self.objective_font.render("Current objective:", True, (200, 200, 200))
        self.current_objective = [line1, line2]

    def collision_update(self):

        """
        Account for collision.  
        Check if predicted rect X, Y collide with wall or map limit.  
        If so: do not move on it's axis
        """
    
        # Default axis to change, remove one if collision detected
        ToChangeList = ["X", "Y"]

        for player in self.group.sprites():
            
            if (player.rect_x_temp.collidelist(self.walls) > -1
                or self.player.temp_position[0] < 0
                or self.player.temp_position[0] > self.tmx_data.width -1):
                ToChangeList.remove("X")

            if (player.rect_y_temp.collidelist(self.walls) > -1 
                or self.player.temp_position[1] < 0
                or self.player.temp_position[1] > self.tmx_data.height -1):
                ToChangeList.remove("Y")

        self.player.position_update(ToChangeList)

    def check_action(self):

        "Check if an action should occur after pressing spacebar"

        # Create coordinate depending on player's facing side
        if self.player.facing == "Up":
            direction_to_check = [round(self.player.position[0]), round(self.player.position[1] - 1)]
        elif self.player.facing == "Down":
            direction_to_check = [round(self.player.position[0]), round(self.player.position[1] + 1)]
        elif self.player.facing == "Left":
            direction_to_check = [round(self.player.position[0] - 1), round(self.player.position[1])]
        elif self.player.facing == "Right":
            direction_to_check = [round(self.player.position[0] + 1), round(self.player.position[1])]

        # If the direction to check has an object to it's coordinate: do action based on the object name
        for IO in self.interactive_object:
            if direction_to_check == [IO[0], IO[1]] or self.player.position == [IO[0], IO[1]]:
                
                # If the object is an NPC
                if IO[2] == "NPC":
                    for obj in self.IO_list:
                        if IO[3] == obj[0]:
                            self.show_dialog(obj, True)
                            return
                # If the object is a Props
                elif IO[2] == "Props":
                    for obj in self.IO_list:
                        if IO[3] == obj[0]:
                            self.show_dialog(obj)
                            return
                # If the object is an action
                elif IO[2] == "Action":
                    for obj in self.IO_list:
                        if IO[3] == obj[0]:
                            self.action(self, obj)
                            return

    @staticmethod
    def create_list(string):

        "Convert a string to a list"

        string = string.replace('[', '')
        string = string.replace(']', '')
        string = string.split(', ')

        return string
    
    def special_action(self, obj):

        "Check the object for attributes assigned to action"

        # Return the item(s) as a list
        def item_list(self, obj, action):

            if obj[1][action][0] == '[' and obj[1][action][-1] == ']':
                item = self.create_list(obj[1][action])
            else:
                item = [obj[1][action]]
            return item
        
        # If the action isn't unique or hasn't been done before
        if not "UniqueAction" in obj[1] or not "AlreadyDone" in obj[1]:

            self.added_dialogue = []

            if "AlreadyDone" in obj[1]:
                return False
            
            if "UniqueAction" in obj[1]:
                obj[1]["AlreadyDone"] = True
        
            if "Add Item" in obj[1]:
                
                if type(obj[1]["Add Item"]) != list:
                    obj[1]["Add Item"] = item_list(self, obj, "Add Item")

                for item in obj[1]["Add Item"]:
                    
                    self.inventory.add_item(item)

                    if "Dialogue" in obj[1]:
                        self.added_dialogue.append(self.font_render("You got 1 "+item+"."))

            if "Remove Item" in obj[1]:

                if type(obj[1]["Remove Item"]) != list:
                    obj[1]["Remove Item"] = item_list(self, obj, "Remove Item")

                for item in obj[1]["Remove Item"]:
                    
                    self.inventory.remove_item(item)

                    if "Dialogue" in obj[1]:
                        self.added_dialogue.append(self.font_render("You lost 1 "+item+"."))

            if "GainHP" in obj[1]:
                self.player.gain_HP(obj[1]["GainHP"])

            if "LoseHP" in obj[1]:
                self.player.lose_HP(obj[1]["LoseHP"])

            if not "Dialogue" in obj[1]:
                return False

            return True

    def show_dialog(self, obj, type_NPC=False):

        """
        Manage NPC scripted dialogue  
        Check for action, fetch the dialogue and return it.
        """

        # If not in dialogue reset and fetch dialog data
        if not self.dialog_enabled:

            if not self.special_action(obj):
                return
            
            self.page_count = 0
            self.current_page = 0
            self.NPC_dialogue = type_NPC

            self.dialog_enabled = True
            self.action_pause = True
            
            # Open appropriate json file depending on the type of object
            if type_NPC:
                self.text = self.get_dict("NPCDialog")
            else:
                self.text = self.get_dict("PropsDescription")

            incrementation = 2 if type_NPC else 1

            self.dialog = []

            # Create Dialogue data, new line, page counter from the json
            for i in range(0, len(self.text[(obj[1]["Dialogue"])]), incrementation):

                List = []
                Dialog = (self.text[(obj[1]["Dialogue"])][i]).split('\n')

                for line in Dialog:
                    List.append(self.font_render(line))

                self.dialog.append(List)
                self.page_count += 1
            self.current_page += 1

            # Add line with got/lost (item) for each item
            for item in self.added_dialogue:
                self.dialog.append([item])
                self.page_count += 1

            if type_NPC:

                if self.text[(obj[1]["Dialogue"])][1] == "desc":
                    self.only_text = True
                    return

                self.NPC_name = self.font_render((obj[1]["NPC Name"])+':', "name")
                self.NPC_face = FUNCTION.get_face_expression(self, obj[1]["Face"], self.text[obj[1]["Dialogue"]][1])
            else:
                self.only_text = True

        # If in dialogue either go to next page or end it
        else:

            self.only_text = False

            if self.current_page >= self.page_count:
                self.dialog_enabled = False
                self.action_pause = False
                return

            self.current_page += 1

            # Check if need to display face and name (It's a dialogue, not only_text)
            if self.NPC_dialogue:

                if self.text[obj[1]["Dialogue"]][self.current_page*2-1] == "desc":
                    self.only_text = True
                    return

                if isinstance(self.text[obj[1]["Dialogue"]][self.current_page*2-1], int):
                    self.NPC_name = self.font_render((obj[1]["NPC Name"])+':', "name")
                else:
                    self.NPC_name = self.font_render((self.text[obj[1]["Dialogue"]][self.current_page*2-1][:-5])+':', "name")

                self.NPC_face = FUNCTION.get_face_expression(self, obj[1]["Face"], self.text[obj[1]["Dialogue"]][self.current_page*2-1])
            else:
                self.only_text = True

    def get_face_expression(self, faceSheet, expression):

        "Fetch face expression from NPCDialog.json."

        if isinstance(expression, int):
            Face = pg.image.load(os.path.join('img', faceSheet+'.png')).convert_alpha()
        else:
            Face = pg.image.load(os.path.join('img', (expression[:-1])+'.png')).convert_alpha()
            expression = int(expression[-1])
        
        size = Face.get_size()
        row = 0
        
        if expression >= 4:
            expression -= 4
            row = 1

        Face = Face.subsurface(pg.Rect(expression * (size[0]/4), row * (size[1]/2), size[0]/4, size[1]/2))
        return Face
    
    @classmethod
    def action(cls, self, obj):

        "Manage Action object."

        if obj[1]["Action type"] == "Battle":

            if not self.battle_mode:

                self.battle_mode = True
                self.BS.battle_init(self.player, cls.create_ennemy(obj))
                self.BM.Menu.toggle()

            else:
                pass

    @classmethod
    def create_ennemy(cls, obj):

        "Create and return ennemy(ies) list with the object passed."

        from ennemy import Ennemy
        
        if obj[1]["Ennemy"][0] == '[' and obj[1]["Ennemy"][-1] == ']':
            ennemy_list = cls.create_list(obj[1]["Ennemy"])
        else:
            ennemy_list = [obj[1]["Ennemy"]]

        ennemy_dict = cls.get_dict("Ennemies")
        new_ennemy_list = []
        for entity in ennemy_list:

            entity_dict = ennemy_dict[entity]
            attr = cls.attributes(entity_dict)
            ennemy_created = Ennemy(attr[0], attr[1], attr[2], attr[3], attr[4], attr[5])
            new_ennemy_list.append(ennemy_created)
        return new_ennemy_list

    @staticmethod
    def attributes(dict):

        "Give the ennemy stats based on the Ennemies.json."

        attr_list = []
        attr_list.append(dict["name"])
        attr_list.append(dict["MAXHP"])
        attr_list.append(dict["DEX"])
        attr_list.append(dict["ATK"])
        attr_list.append(dict["DEF"])
        attr_list.append(dict["STAM"])
        return attr_list

    @classmethod
    def fetch_item_desc(cls, item_name):

        "Return given item's description."

        item_dict = cls.get_dict("Items")

        return item_dict[item_name]["desc"]

    def use_item(self, item):

        "Check item property and use it how it's supposed to."

        item_dict = self.get_dict("Items")

        if item_dict[item]["type"] == "heal_item":

            amount = item_dict[item]["heal_amount"]
            self.player.gain_HP(amount)

    @staticmethod
    def get_dict(filename):

        "Return a json file as a dictionnary"
        
        with open(os.path.join("data", filename + ".json")) as dict:
            return json.load(dict)
    
    @classmethod
    def skill(cls, skill):
        
        "Check skill property in data and return a list of effect accordingly."
        
        skill_dict = cls.get_dict("Skills")

        if skill_dict[skill]["type"] == "attack":
            power = skill_dict[skill]["power"]
            stam_consumption = skill_dict[skill]["stam_consumption"]
            return ["atk", power, stam_consumption]

        elif skill_dict[skill]["type"] == "heal":
            heal_amount = skill_dict[skill]["heal_amount"]
            stam_consumption = skill_dict[skill]["stam_consumption"]
            return ["heal", heal_amount, stam_consumption]

    @classmethod
    def process(cls, skill, attacker, defender):

        "Alter the fighter's stats based on the skill used."
        
        # Currently assigned to "Wait" action
        if skill is None:
            return
        
        def check_stam(entity, stam):

            "Check if the stamina needed exceed the entity's"
            
            if skill[2] > attacker.STAM:
                print("not enough stamina")
                return True
            return False
        
        if skill[0] == "atk":
            
            if check_stam(attacker, skill[2]):
                return # Should return a text?
            
            dmg = cls.damage_formula(attacker, defender, skill[1])
            print(f'dmg is {dmg}')
            
            attacker.STAM -= skill[2]
            defender.HP -= dmg
            return

        elif skill[0] == "heal":

            if check_stam(attacker, skill[2]):
                return # Should return a text?

            attacker.STAM -= skill[2]
            attacker.HP += skill[1]
            return

    @staticmethod
    def damage_formula(attacker, defender, power):

        """
        Calculate the damage done after processing the damage formula.

        Formula:
            damage = (attaker.atk * (4 + power - 1) - defender.def * 2)
            
        """

        dmg = (attacker.ATK*(4+power-1)-defender.DEF*2)
        # Prevent negative damage
        if dmg < 0:
            dmg = 0
        return dmg

    def font_render(self, string, font="default", color=(255, 255, 255)):

        "Convert a string to a pygame text surface"

        if font == "default":
            return self.Font.render(string, True, color)
        elif font == "name":
            return self.name_font.render(string, True, (200, 200, 200))

    @staticmethod
    def create_save(game_object):

        "Pickle data in a savefile located in the save folder"

        game = [
            game_object.inventory.content,
            game_object.current_map
        ]
        
        player = [
            game_object.player._position,
            game_object.player.counter,
            game_object.player.facing,
            game_object.player.MAXHP,
            game_object.player.HP,
            game_object.player.DEX,
            game_object.player.ATK,
            game_object.player.DEF,
            game_object.player.STAM,
            game_object.player.rect.x,
            game_object.player.rect.y
        ]

        savepath = open(os.path.join("save", "game_save"), "wb")
        pickle.dump([game, player], savepath)
        savepath.close()

    @staticmethod
    def load_save(game_object):

        "Load a pickled data in the save folder"

        from menu import MenuFunction
        
        savepath = open(os.path.join("save", "game_save"), "rb")
        save = pickle.load(savepath)
        savepath.close()

        game = save[0]
        player = save[1]

        game_object.new()

        game_object.inventory.content = game[0]
        game_object.current_map = game[1]

        game_object.load_map(game[1])

        game_object.player._position = player[0]
        game_object.player.counter = player[1]
        game_object.player.facing = player[2]
        game_object.player.MAXHP = player[3]
        game_object.player.HP = player[4]
        game_object.player.DEX = player[5]
        game_object.player.ATK = player[6]
        game_object.player.DEF = player[7]
        game_object.player.STAM = player[8]
        game_object.player.rect.x = player[9]
        game_object.player.rect.y = player[10]

        game_object.group.add(game_object.player)

        if game_object.menu_pause:
            MenuFunction.toggle(game_object, game_object.IGM.Menu)