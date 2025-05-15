import unittest
from menu import Menu
from dish import Dish
from client import Client
from order.order import Order
from kitchen_notifier import KitchenNotifier

class TestFoodOrderTDD(unittest.TestCase):

    def test_add_dish_to_menu(self):
        menu = Menu()
        dish = Dish("Pizza", 150)
        menu.add_dish(dish)
        self.assertTrue(menu.contains_dish(dish))

    def test_fail_add_duplicate_dish(self):
        menu = Menu()
        dish = Dish("Pizza", 150)
        menu.add_dish(dish)
        menu.add_dish(dish)  # Очікується подвійне додавання
        self.assertEqual(menu.get_dishes().count(dish), 2)

    def test_create_order_for_client(self):
        client = Client("Alice")
        order = Order(client)
        self.assertEqual(order.client.name, "Alice")

    def test_add_dish_to_order(self):
        client = Client("Bob")
        order = Order(client)
        dish = Dish("Burger", 120)
        order.add_dish(dish)
        self.assertIn(dish, order.dishes)

    def test_create_order_with_multiple_dishes(self):
        client = Client("Tom")
        order = Order(client)
        order.add_dish(Dish("Tea", 20))
        order.add_dish(Dish("Cake", 50))
        self.assertEqual(len(order.dishes), 2)

    def test_order_without_client_should_fail(self):
        with self.assertRaises(TypeError):
            Order(None)

    def test_notify_kitchen(self):
        client = Client("Emma")
        order = Order(client)
        order.add_dish(Dish("Soup", 80))
        notifier = KitchenNotifier()
        try:
            notifier.notify(order)
        except Exception as e:
            self.fail(f"KitchenNotifier raised exception: {e}")

    def test_kitchen_notification_format(self):
        client = Client("Ivan")
        order = Order(client)
        order.add_dish(Dish("Fries", 40))
        notifier = KitchenNotifier()
        output = notifier.notify(order)
        self.assertIn("Fries", output)
        self.assertIn("Ivan", output)

    def test_add_dish_to_order_with_no_dishes(self):
        client = Client("Anna")
        order = Order(client)
        self.assertEqual(order.dishes, [])

    def test_menu_contains_added_dishes(self):
        menu = Menu()
        dish1 = Dish("Sushi", 200)
        dish2 = Dish("Ramen", 180)
        menu.add_dish(dish1)
        menu.add_dish(dish2)
        self.assertIn(dish1, menu.get_dishes())
        self.assertIn(dish2, menu.get_dishes())

if __name__ == '__main__':
    unittest.main()
