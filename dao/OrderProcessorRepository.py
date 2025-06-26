# dao/OrderProcessorRepository.py
from abc import ABC, abstractmethod

class OrderProcessorRepository(ABC):
    """Interface for ecommerce operations like customer/product management, cart, and orders."""

    @abstractmethod
    def create_customer(self, customer):
        """Insert a new customer into the database."""
        pass

    @abstractmethod
    def create_product(self, product):
        """Insert a new product into the database."""
        pass

    @abstractmethod
    def delete_product(self, product_id):
        """Delete a product from the database by ID."""
        pass

    @abstractmethod
    def delete_customer(self, customer_id):
        """Delete a customer from the database by ID."""
        pass

    @abstractmethod
    def add_to_cart(self, customer, product, quantity):
        """Add a product with quantity to the customer's cart."""
        pass

    @abstractmethod
    def remove_from_cart(self, customer, product):
        """Remove a product from the customer's cart."""
        pass

    @abstractmethod
    def get_all_from_cart(self, customer):
        """Get all items in a customer's cart."""
        pass

    @abstractmethod
    def place_order(self, customer, product_quantity_list, shipping_address):
        """Place an order for the items in the cart."""
        pass

    @abstractmethod
    def get_orders_by_customer(self, customer_id):
        """Retrieve all orders placed by a customer."""
        pass
