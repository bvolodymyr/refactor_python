class Order:
    def __init__(self, client):
        if client is None:
            raise TypeError("Client must not be None")
        self.client = client
        self.dishes = []

    def add_dish(self, dish):
        self.dishes.append(dish)
