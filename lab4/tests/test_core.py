import unittest
from menu import Menu
from dish import Dish
from client import Client
from order.order import Order
from kitchen_notifier import KitchenNotifier

class TestCoreSystem(unittest.TestCase):

    def test_create_dish(self):
        dish = Dish("Pizza", 150)
        self.assertEqual(dish.name, "Pizza")
        self.assertEqual(dish.price, 150)

    def test_add_dish_to_menu(self):
        menu = Menu()
        dish = Dish("Burger", 100)
        menu.add_dish(dish)
        self.assertIn(dish, menu.get_dishes())

    def test_contains_dish_in_menu(self):
        menu = Menu()
        dish = Dish("Sushi", 200)
        menu.add_dish(dish)
        self.assertTrue(menu.contains_dish(dish))

    def test_create_client(self):
        client = Client("Alice")
        self.assertEqual(client.name, "Alice")

    def test_create_order(self):
        client = Client("Bob")
        order = Order(client)
        self.assertEqual(order.client.name, "Bob")
        self.assertEqual(order.dishes, [])

    def test_add_dish_to_order(self):
        client = Client("Eve")
        order = Order(client)
        dish = Dish("Salad", 80)
        order.add_dish(dish)
        self.assertIn(dish, order.dishes)

    def test_add_multiple_dishes_to_order(self):
        client = Client("Tom")
        order = Order(client)
        d1 = Dish("Steak", 300)
        d2 = Dish("Juice", 50)
        order.add_dish(d1)
        order.add_dish(d2)
        self.assertEqual(len(order.dishes), 2)

    def test_kitchen_notifier_output(self):
        client = Client("Anna")
        order = Order(client)
        order.add_dish(Dish("Pasta", 120))
        notifier = KitchenNotifier()
        # Here we only ensure notify method doesn't raise exceptions
        try:
            notifier.notify(order)
        except Exception as e:
            self.fail(f"Notifier raised exception: {e}")

    def test_empty_menu(self):
        menu = Menu()
        self.assertEqual(len(menu.get_dishes()), 0)

    def test_order_without_dishes(self):
        client = Client("Nina")
        order = Order(client)
        self.assertEqual(order.dishes, [])

if __name__ == '__main__':
    unittest.main()
