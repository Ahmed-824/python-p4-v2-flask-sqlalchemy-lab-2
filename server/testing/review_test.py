import pytest
from app import app, db
from server.models import Customer, Item, Review

@pytest.fixture
def client():
    """Create a test client for the app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            # Create the database and the database table
            db.create_all()
        yield client
        with app.app_context():
            # Drop the database tables after tests
            db.drop_all()

class TestReview:
    """Review model in models.py"""

    def test_can_be_instantiated(self):
        """can be invoked to create a Python object."""
        r = Review()
        assert r
        assert isinstance(r, Review)

    def test_has_comment(self):
        """can be instantiated with a comment attribute."""
        r = Review(comment='great product!')
        assert r.comment == 'great product!'

    def test_can_be_saved_to_database(self, client):
        """can be added to a transaction and committed to review table with comment column."""
        with app.app_context():
            # Create a customer and an item first, as they are required by foreign keys
            c = Customer(name='John Doe')
            i = Item(name='Laptop', price=999.99)
            db.session.add_all([c, i])
            db.session.commit()

            # Now create the review with the foreign key relations
            r = Review(comment='great!', customer_id=c.id, item_id=i.id)
            db.session.add(r)
            db.session.commit()

            # Check if review was saved to the database
            assert hasattr(r, 'id')
            assert db.session.query(Review).filter_by(id=r.id).first() is not None

    def test_is_related_to_customer_and_item(self, client):
        """has foreign keys and relationships."""
        with app.app_context():
            # Check if the foreign keys are present in the Review table
            assert 'customer_id' in Review.__table__.columns
            assert 'item_id' in Review.__table__.columns

            # Create a customer and an item for testing relationships
            c = Customer(name='John Doe')
            i = Item(name='Laptop', price=999.99)
            db.session.add_all([c, i])
            db.session.commit()

            # Create the review and link it to the customer and item
            r = Review(comment='great!', customer=c, item=i)
            db.session.add(r)
            db.session.commit()

            # Check if the foreign keys were correctly set
            assert r.customer_id == c.id
            assert r.item_id == i.id

            # Check if the relationships are working correctly
            assert r.customer == c
            assert r.item == i
            assert r in c.reviews
            assert r in i.reviews
