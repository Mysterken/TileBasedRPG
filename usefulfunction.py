import os, sys
import pygame as pg
import json
from settings import TILESIZE

# Various useful function, call from here, better code visibility in other file
class FUNCTION():

    def quit(self):
        pg.quit()
        sys.exit()

    # Check if predicted rect X, Y collide with wall or map limit, if so: do not move on it's axis
    def UpdateAndCollision(self):
    
        # Default axis to change, remove one if collision detected
        ToChangeList = ["X", "Y"]

        for player in self.group.sprites():
            
            if (player.RectXChanged.collidelist(self.walls) > -1
                or self.player.TemPosition[0] < 0
                or self.player.TemPosition[0] > self.tmx_data.width -1):
                ToChangeList.remove("X")

            if (player.RectYChanged.collidelist(self.walls) > -1 
                or self.player.TemPosition[1] < 0
                or self.player.TemPosition[1] > self.tmx_data.height -1):
                ToChangeList.remove("Y")

        self.player.PositionUpdate(ToChangeList)

    # Called to check if an action should occur after pressing spacebar
    def CheckAction(self, GAME):

        # Create coordinate depending on player's facing side
        if GAME.player.Facing == "Up":
            DirectionToCheck = [round(GAME.player._position[0]), round(GAME.player._position[1] - 1)]
        elif GAME.player.Facing == "Down":
            DirectionToCheck = [round(GAME.player._position[0]), round(GAME.player._position[1] + 1)]
        elif GAME.player.Facing == "Left":
            DirectionToCheck = [round(GAME.player._position[0] - 1), round(GAME.player._position[1])]
        elif GAME.player.Facing == "Right":
            DirectionToCheck = [round(GAME.player._position[0] + 1), round(GAME.player._position[1])]

        # If the direction to check has an object to it's coordinate: do action based on the object name
        for IO in GAME.InteractiveObject:
            if DirectionToCheck == [IO[0], IO[1]]:
                
                # If the object is an NPC
                if IO[2] == "NPC":
                    for obj in GAME.IOList:
                        if IO[3] == obj[0]:
                            FUNCTION.ShowDialog(self, GAME, obj)
                            return

    # Manage NPC scripted dialogue
    def ShowDialog(self, GAME, obj):

        # If not in dialogue reset and fetch dialog data
        if not GAME.InDialog:

            self.PageCounter = 0
            self.CurrentPage = 0

            GAME.InDialog = True
            GAME.ActionPaused = not GAME.ActionPaused

            self.BOX = pg.image.load(os.path.join('img', 'DialogBox.png')).convert_alpha()
            self.BOX.set_alpha(235)
            
            with open("NPCDialogFile.json") as Text:
                self.text = json.load(Text)

            NameFont = pg.font.Font(os.path.join('Font', 'Roboto-Regular.ttf'), 25)

            self.NPCName = NameFont.render((obj[1]["NPCName"])+':', True, (200, 200, 200))
            self.NPCFace = FUNCTION.FaceImage(self, obj[1]["Face"], self.text[obj[1]["Dialogue"]][1])
            self.Dialog = []
        
            # Create Dialogue data, new line, page counter
            for i in range(0, len(self.text[(obj[1]["Dialogue"])]), 2):
                List = []
                Dialog = (self.text[(obj[1]["Dialogue"])][i]).rsplit('\n')
                for line in Dialog:
                    List.append(GAME.Font.render(line, True, (255, 255, 255)))
                self.Dialog.append(List)
                self.PageCounter += 1
            self.CurrentPage += 1
        
        # If in dialogue either go to next page or end it
        else:
            
            if self.CurrentPage >= self.PageCounter:
                GAME.InDialog = False
                GAME.ActionPaused = False
                return
            
            self.CurrentPage += 1
            self.NPCFace = FUNCTION.FaceImage(self, obj[1]["Face"], self.text[obj[1]["Dialogue"]][self.CurrentPage+1])

    # Fetch face expression in NPCDialogFile.json
    def FaceImage(self, FaceSheet, expression):

        Face = pg.image.load(os.path.join('img', FaceSheet+'.png')).convert_alpha()
        size = Face.get_size()
        row = 0
        
        if expression >= 4:
            expression -= 4
            row = 1

        Face = Face.subsurface(pg.Rect(expression * (size[0]/4), row * (size[1]/2), size[0]/4, size[1]/2))
        return Face