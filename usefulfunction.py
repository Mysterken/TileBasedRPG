import os
import sys
import json
import pygame as pg
from settings import TILESIZE

# Various useful function, call from here, better code visibility in other file
class FUNCTION:

    @staticmethod
    def quit():
        pg.quit()
        sys.exit()

    # Check if predicted rect X, Y collide with wall or map limit, if so: do not move on it's axis
    def collision_update(self):
    
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

    # Called to check if an action should occur after pressing spacebar
    def check_action(self):

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
                            FUNCTION.show_dialog(self, obj, True)
                            return
                # If the object is a Props => WIP
                elif IO[2] == "Props":
                    for obj in self.IO_list:
                        if IO[3] == obj[0]:
                            FUNCTION.show_dialog(self, obj)
                            return

    # Manage NPC scripted dialogue
    def show_dialog(self, obj, type_NPC=False):

        # If not in dialogue reset and fetch dialog data
        if not self.dialog_enabled:

            self.page_count = 0
            self.current_page = 0
            self.NPC_dialogue = type_NPC

            self.dialog_enabled = True
            self.action_pause = True

            self.box = pg.image.load(os.path.join('img', 'DialogBox.png')).convert_alpha()
            self.box.set_alpha(235)
            
            # Open appropriate json file depending on the type of object
            if type_NPC:
                with open("NPCDialogFile.json") as Text:
                    self.text = json.load(Text)
            else:
                with open("PropsDescriptionFile.json") as Text:
                    self.text = json.load(Text)

            incrementation = 2 if type_NPC else 1

            self.name_font = pg.font.Font(os.path.join('Font', 'Roboto-Regular.ttf'), 25)
            self.dialog = []
        
            # Create Dialogue data, new line, page counter from the json
            for i in range(0, len(self.text[(obj[1]["Dialogue"])]), incrementation):

                List = []
                Dialog = (self.text[(obj[1]["Dialogue"])][i]).rsplit('\n')

                for line in Dialog:
                    List.append(self.font_render(line))
                    
                self.dialog.append(List)
                self.page_count += 1
            self.current_page += 1

            if "AddItem" in obj[1]:
                self.inventory.add_item(obj[1]["AddItem"])

            if "RemoveItem" in obj[1]:
                self.inventory.remove_item(obj[1]["RemoveItem"])

            if type_NPC:

                if self.text[(obj[1]["Dialogue"])][1] == "desc":
                    self.only_text = True
                    return

                self.NPC_name = self.font_render((obj[1]["NPCName"])+':', "name")
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
                    self.NPC_name = self.font_render((obj[1]["NPCName"])+':', "name")
                else:
                    self.NPC_name = self.font_render((self.text[obj[1]["Dialogue"]][self.current_page*2-1][:-5])+':', "name")

                self.NPC_face = FUNCTION.get_face_expression(self, obj[1]["Face"], self.text[obj[1]["Dialogue"]][self.current_page*2-1])
            else:
                self.only_text = True

    # Fetch face expression in NPCDialogFile.json
    def get_face_expression(self, faceSheet, expression):

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

    # Return given item's description
    def fetch_item_desc(self, item_name):

        with open("ItemDescription.json") as dict:
            item_dict = json.load(dict)

        return item_dict[item_name]["desc"]

    # convert a string to a pygame text surface
    def font_render(self, string, font="default", color=(255, 255, 255)):

        if font == "default":
            return self.Font.render(string, True, color)
        elif font == "name":
            return self.name_font.render(string, True, (200, 200, 200))