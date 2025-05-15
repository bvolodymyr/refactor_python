from order import Order
from client import Client

class OrderFactory:
    @staticmethod
    def create_order(order_type: str, client: Client, dishes=None):
        order = Order(client)
        if dishes:
            for dish in dishes:
                order.add_dish(dish)
        return order
