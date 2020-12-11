import os
import sys
import json
import pygame as pg
from settings import TILESIZE

# Various useful function, call from here, better code visibility in other file
class FUNCTION():

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
    def check_action(self, GAME):

        # Create coordinate depending on player's facing side
        if GAME.player.facing == "Up":
            direction_to_check = [round(GAME.player.position[0]), round(GAME.player.position[1] - 1)]
        elif GAME.player.facing == "Down":
            direction_to_check = [round(GAME.player.position[0]), round(GAME.player.position[1] + 1)]
        elif GAME.player.facing == "Left":
            direction_to_check = [round(GAME.player.position[0] - 1), round(GAME.player.position[1])]
        elif GAME.player.facing == "Right":
            direction_to_check = [round(GAME.player.position[0] + 1), round(GAME.player.position[1])]

        # If the direction to check has an object to it's coordinate: do action based on the object name
        for IO in GAME.interactive_object:
            if direction_to_check == [IO[0], IO[1]]:
                
                # If the object is an NPC
                if IO[2] == "NPC":
                    for obj in GAME.IO_list:
                        if IO[3] == obj[0]:
                            FUNCTION.show_dialog(self, GAME, obj, True)
                            return
                # If the object is a Props => WIP
                elif IO[2] == "Props":
                    for obj in GAME.IO_list:
                        if IO[3] == obj[0]:
                            FUNCTION.show_dialog(self, GAME, obj)
                            return

    # Manage NPC scripted dialogue
    def show_dialog(self, GAME, obj, type_NPC=False):

        # If not in dialogue reset and fetch dialog data
        if not GAME.dialog_enabled:

            self.page_count = 0
            self.current_page = 0

            GAME.dialog_enabled = True
            GAME.action_pause = True

            self.box = pg.image.load(os.path.join('img', 'DialogBox.png')).convert_alpha()
            self.box.set_alpha(235)
            
            with open("NPCDialogFile.json") as Text:
                self.text = json.load(Text)

            self.name_font = pg.font.Font(os.path.join('Font', 'Roboto-Regular.ttf'), 25)

            self.dialog = []
        
            # Create Dialogue data, new line, page counter
            for i in range(0, len(self.text[(obj[1]["Dialogue"])]), 2):
                List = []
                Dialog = (self.text[(obj[1]["Dialogue"])][i]).rsplit('\n')
                for line in Dialog:
                    List.append(GAME.Font.render(line, True, (255, 255, 255)))
                self.dialog.append(List)
                self.page_count += 1
            self.current_page += 1

            if type_NPC:
                self.NPC_name = self.name_font.render((obj[1]["NPCName"])+':', True, (200, 200, 200))
                self.NPC_face = FUNCTION.get_face_expression(self, obj[1]["Face"], self.text[obj[1]["Dialogue"]][1])
        
        # If in dialogue either go to next page or end it
        else:

            if self.current_page >= self.page_count:
                GAME.dialog_enabled = False
                GAME.action_pause = False
                return

            self.current_page += 1
            self.NPC_face = FUNCTION.get_face_expression(self, obj[1]["Face"], self.text[obj[1]["Dialogue"]][self.current_page*2-1])

            if isinstance(self.text[obj[1]["Dialogue"]][self.current_page*2-1], int):
                self.NPC_name = self.name_font.render((obj[1]["NPCName"])+':', True, (200, 200, 200))
            else:
                self.NPC_name = self.name_font.render((self.text[obj[1]["Dialogue"]][self.current_page*2-1][:-5])+':', True, (200, 200, 200))

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