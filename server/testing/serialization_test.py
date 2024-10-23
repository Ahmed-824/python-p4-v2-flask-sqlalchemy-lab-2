import unittest
from app import app, db
from models import Customer, Item, Review

class TestSerialization(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = app
        cls.app.config['TESTING'] = True
        cls.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    def test_customer_is_serializable(self):
        '''Test that Customer object can be serialized.'''
        with app.app_context():
            # Create a customer
            c = Customer(name='Phil')
            db.session.add(c)
            db.session.commit()

            # Serialize the customer
            serialized = {
                'id': c.id,
                'name': c.name,
            }

            # Check the serialization
            self.assertEqual(serialized['name'], 'Phil')
            self.assertIsNotNone(serialized['id'])

    def test_item_is_serializable(self):
        '''Test that Item object can be serialized.'''
        with app.app_context():
            # Create an item
            i = Item(name='Insulated Mug', price=9.99)
            db.session.add(i)
            db.session.commit()

            # Serialize the item
            serialized = {
                'id': i.id,
                'name': i.name,
                'price': i.price,
            }

            # Check the serialization
            self.assertEqual(serialized['name'], 'Insulated Mug')
            self.assertEqual(serialized['price'], 9.99)
            self.assertIsNotNone(serialized['id'])

    def test_review_is_serializable(self):
        '''Test that Review object can be serialized.'''
        with app.app_context():
            # Create customer and item first
            c = Customer(name='Phil')
            i = Item(name='Insulated Mug', price=9.99)
            db.session.add(c)
            db.session.add(i)
            db.session.commit()

            # Now create a review
            r = Review(comment='great!', customer=c, item=i)
            db.session.add(r)
            db.session.commit()

            # Serialize the review
            serialized = {
                'id': r.id,
                'comment': r.comment,
                'customer_id': r.customer_id,
                'item_id': r.item_id,
            }

            # Check the serialization
            self.assertEqual(serialized['comment'], 'great!')
            self.assertEqual(serialized['customer_id'], c.id)
            self.assertEqual(serialized['item_id'], i.id)
            self.assertIsNotNone(serialized['id'])

if __name__ == '__main__':
    unittest.main()
