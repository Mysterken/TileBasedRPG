import pygame as pg
from usefulfunction import FUNCTION

class BattleSystem:

    def __init__(self):
    
        self.battle_screen = None

    def battle_init(self, player, ennemy):

        "Initiate and reset the battle variables."

        if player.HP <= 0:
            print("player is ded")
            return

        player.escaped = False
        
        fighters = [player]
        
        if type(ennemy) != list:
            ennemy = [ennemy]
        
        for entity in ennemy:
            
            if entity.randomize:
               entity.randomize_stats()
            
            fighters.append(entity)
        
        self.ennemy = ennemy
        self.fighters = self.turn_order(fighters)
        self.loop = True
        self.turn = 0

    def battle(self, GAME, player, ennemy):

        "Main battle loop"
                
        # Break the loop if an battle ending event is found
        self.loop = self.loop_event(player, ennemy)
        if not self.loop:
            print("event ender found")
            print("The fight has ended")
            return False

        # Skip turn
        if not self.fighters[self.turn].in_fight():
            self.fighters.pop(self.fighters.index(self.fighters[self.turn]))
            if self.turn > len(self.fighters)-1:
                self.turn = 0
            return False

        # Check who are the attacker and defender
        if type(self.fighters[self.turn]).__name__ == "Ennemy":
            
            # action[0] is the skill string, [1] is the target
            action = [self.fighters[self.turn].pick_action()]
            skill = self.fighters[self.turn].do_action(action[0])
            attacker = self.fighters[self.turn]
            defender = player
        
        else:
            
            action = [GAME.BM.sent_action]

            if action[0] is None:
                return True
            else:
                GAME.BM.sent_action = None
            
            skill = self.fighters[self.turn].do_action(action[0])        
            attacker = player
            defender = ennemy[0]#[action[1]] for targeting

        print(f'{self.fighters[self.turn].name} used {action[0]}!')
        FUNCTION.process(skill, attacker, defender)
        print('----')
        print(f'player HP is: {player.HP}')
        print(f'Ennemy HP is: {self.ennemy[0].HP}')
        self.turn += 1
        if self.turn > len(self.fighters)-1:
                self.turn = 0
        print("the turn is over")
        print('----')
        return True

    @staticmethod
    def turn_order(List):

        "Return a sorted fighter list by descending DEX"

        List.sort(key=lambda x: x.DEX, reverse=True)
        return List

    @staticmethod
    def loop_event(player, ennemy):

        "Check for event that end the battle."

        if player.HP <= 0:
            return False

        defeated = 0
        for entity in ennemy:

            if not entity.in_fight():
                defeated += 1

        # If all ennemies are defeated/not in fight
        if defeated == len(ennemy):
            return False
        return True