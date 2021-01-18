class Inventory:

    "Inventory class, the item passed are stored as strings."

    def __init__(self):

        self.content = []

    def add_item(self, item):

        "Add given item to the inventory."
        
        self.content.append(item)

    def remove_item(self, item):

        "Remove given item from the inventory."

        self.content.remove(item)

    def check_item(self, item):

        "Check if given item is in the inventory, return True or False"

        if item in self.content:
            return True
        return False