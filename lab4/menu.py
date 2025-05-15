class Menu:
    def __init__(self):
        self._dishes = []

    def add_dish(self, dish):
        self._dishes.append(dish)

    def get_dishes(self):
        return self._dishes

    def contains_dish(self, dish):
        return dish in self._dishes
