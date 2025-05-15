from order import Order

class OrderDatabase:
    _instance = None
    _orders = []

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(OrderDatabase, cls).__new__(cls)
            cls._orders = []
        return cls._instance

    def add_order(self, order: Order):
        self._orders.append(order)

    def get_orders(self):
        return self._orders
