class KitchenNotifier:
    def notify(self, order):
        message = f"New order for kitchen: {[dish.name for dish in order.dishes]} from {order.client.name}"
        print(message)
        return message
