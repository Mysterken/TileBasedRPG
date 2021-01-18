from random import randint
from usefulfunction import FUNCTION

class Ennemy:

    def __init__(self, name, MAXHP, DEX, ATK, DEF, STAM, **kwargs):

        """
        Initiate the ennemy with the given stats.
        
        Necessary stats:
            MAXHP
            DEX
            ATK
            DEF
            STAM

        Kwargs stats (if not given, default value):
            runnaway : Rate at which the ennemy run from the fight
            randomize : Randomize attribute in this range point
            hit_rate : Rate of hitting player
            dodge_rate : Rate of dodging the player's attack
            crit_rate : Rate of a critical hit
            exp_drop : Amount of XP dropped
            item_drop : Item(s) dropped
            gold_drop : Amount of gold(s) dropped
            skills_list : string list of ennemy's skill

        """

        self.name = name
        self.MAXHP = MAXHP
        self.HP = MAXHP
        self.DEX = DEX
        self.ATK = ATK
        self.DEF = DEF
        self.STAM = STAM

        self.runnaway = self._get(kwargs, 'runnaway')
        self.randomize = self._get(kwargs, 'randomize', 2)
        self.hit_rate = self._get(kwargs, 'hit_rate', 85)
        self.dodge_rate = self._get(kwargs, 'dodge_rate', 5)
        self.crit_rate = self._get(kwargs, 'crit_rate', 5)
        self.exp_drop = self._get(kwargs, 'exp_drop', [0, 0])
        self.item_drop = self._get(kwargs, 'item_drop')
        self.gold_drop = self._get(kwargs, 'gold_drop')
        self.skills_list = self._get(kwargs, 'skills_list', ["Attack"])

        self.escaped = False

    @staticmethod
    def _get(kwargs, attribute, default=[]):
        
        "Return a value from a dictionary, else return the default value."

        if attribute in kwargs:
            return kwargs[attribute]
        return default

    def randomize_stats(self):

        "Randomize stats in the range of the randomize attribute."

        if self.randomize:
            
            random_num = [] 
            for unused in range(0, 3):
                random_num.append(randint(-self.randomize, self.randomize))

            self.DEX += random_num[0]
            self.ATK += random_num[1]
            self.DEF += random_num[2]
        
    def pick_action(self):

        "Randomly choose an action to perform."

        if self.runnaway:
            if self.runnaway <= randint(1, 100):
                return "Run"
        
        skill = self.skills_list[randint(0, len(self.skills_list)-1)]
        return skill

    def do_action(self, action):

        "Make the ennemy perform the given skill"

        if action == "Run":
            self.escaped = True
            return
        return FUNCTION.skill(action)

    def lose_HP(self, amount):

        "Deduct an amount from the ennemy's HP"

        if self.HP - amount <= 0:
            self.HP = 0
        else:
            self.HP -= amount

    def gain_HP(self, amount):

        "Add an amount to the ennemy's HP"

        if self.HP + amount >= self.MAXHP:
            self.HP = self.MAXHP
        else:
            self.HP += amount

    def dead(self):

        "Return whether or not the ennemy is dead"
        
        if self.HP <= 0:
            return True
        return False

    def in_fight(self):

        "Return whether or not the ennemy is still in the fight"

        if self.dead() or self.escaped:
            return False
        return True