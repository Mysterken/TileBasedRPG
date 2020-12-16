class Inventory:

    def __init__(self):

        self.content = []

    def add_item(self, item):
        
        self.content.append(item)

    def remove_item(self, item):

        self.content.remove(item)

    # Check if given item is in the inventory, return True or False
    def check_item(self, item):

        if item in self.content:
            return True
        return False