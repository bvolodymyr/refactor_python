from observer import Subscriber

class KitchenSubscriber(Subscriber):
    def update(self, order):
        print(f"[Kitchen] New order received from {order.client.name}:")
        for dish in order.dishes:
            print(f" - {dish.name}")
