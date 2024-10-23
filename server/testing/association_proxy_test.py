import pytest
from app import app, db
from server.models import Customer, Item, Review


class TestAssociationProxy:
    '''Test the association proxy in models.py'''

    @classmethod
    def setup_class(cls):
        # Set up the application context and database for testing
        cls.app = app
        cls.app.config['TESTING'] = True
        cls.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use an in-memory database
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        db.create_all()  # Create all tables

    @classmethod
    def teardown_class(cls):
        # Tear down the application context and drop all tables
        db.session.remove()
        db.drop_all()  # Drop all tables
        cls.app_context.pop()

    def test_has_association_proxy(self):
        '''Test association proxy to items'''
        with app.app_context():
            # Create instances of Customer and Item
            c = Customer(name='John Doe')  # Assuming Customer has a 'name' field
            i = Item(name='Sample Item')    # Assuming Item has a 'name' field

            # Add the instances to the session and commit
            db.session.add_all([c, i])
            db.session.commit()

            # Create a Review and link it to the Customer and Item
            r = Review(comment='great!', customer=c, item=i)
            db.session.add(r)
            db.session.commit()

            # Assert that the association proxy works correctly
            assert hasattr(c, 'items')  # Check if Customer has an 'items' attribute
            assert i in c.items         # Check if the Item is in the Customer's items

