import unittest
from client import Client
from dish import Dish
from order.order_factory import OrderFactory
from order.order_database import OrderDatabase
from kitchen_subscriber import KitchenSubscriber
from observer import Publisher

class TestPatterns(unittest.TestCase):

    def test_singleton_order_database(self):
        db1 = OrderDatabase()
        db2 = OrderDatabase()
        self.assertIs(db1, db2)

    def test_order_addition_to_singleton(self):
        db = OrderDatabase()
        db._orders.clear()
        client = Client("TestUser")
        order = OrderFactory.create_order("regular", client)
        db.add_order(order)
        self.assertIn(order, db.get_orders())

    def test_factory_creates_order(self):
        client = Client("FactoryUser")
        dishes = [Dish("Cake", 50), Dish("Juice", 30)]
        order = OrderFactory.create_order("regular", client, dishes)
        self.assertEqual(len(order.dishes), 2)
        self.assertEqual(order.client.name, "FactoryUser")

    def test_factory_empty_order(self):
        client = Client("NoDishes")
        order = OrderFactory.create_order("regular", client)
        self.assertEqual(order.dishes, [])

    def test_observer_notifies_kitchen(self):
        client = Client("Ivan")
        dish = Dish("Pelmeni", 80)
        order = OrderFactory.create_order("regular", client, [dish])

        kitchen = KitchenSubscriber()
        publisher = Publisher()
        publisher.subscribe(kitchen)

        try:
            publisher.notify_all(order)
        except Exception as e:
            self.fail(f"Observer notification failed: {e}")

    def test_observer_multiple_kitchens(self):
        client = Client("Group")
        dish = Dish("Steak", 200)
        order = OrderFactory.create_order("regular", client, [dish])

        kitchen1 = KitchenSubscriber()
        kitchen2 = KitchenSubscriber()
        publisher = Publisher()
        publisher.subscribe(kitchen1)
        publisher.subscribe(kitchen2)

        try:
            publisher.notify_all(order)
        except Exception as e:
            self.fail(f"Multiple observers failed: {e}")

    def test_unsubscribe_kitchen(self):
        client = Client("Test")
        dish = Dish("Wok", 110)
        order = OrderFactory.create_order("regular", client, [dish])

        kitchen = KitchenSubscriber()
        publisher = Publisher()
        publisher.subscribe(kitchen)
        publisher.unsubscribe(kitchen)

        try:
            publisher.notify_all(order)  # No error, no output expected
        except Exception as e:
            self.fail(f"Unsubscribe failed: {e}")

    def test_singleton_stores_multiple_orders(self):
        db = OrderDatabase()
        db._orders.clear()
        client1 = Client("C1")
        client2 = Client("C2")
        order1 = OrderFactory.create_order("regular", client1)
        order2 = OrderFactory.create_order("regular", client2)
        db.add_order(order1)
        db.add_order(order2)
        self.assertEqual(len(db.get_orders()), 2)

    def test_order_in_singleton_is_same_object(self):
        db = OrderDatabase()
        db._orders.clear()
        client = Client("SameCheck")
        order = OrderFactory.create_order("regular", client)
        db.add_order(order)
        self.assertIs(db.get_orders()[0], order)

    def test_factory_with_no_dishes_still_valid_order(self):
        client = Client("Test")
        order = OrderFactory.create_order("regular", client)
        self.assertIsNotNone(order)

if __name__ == "__main__":
    unittest.main()
