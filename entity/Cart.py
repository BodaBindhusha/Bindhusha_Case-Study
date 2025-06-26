# entity/Cart.py
class CartItem:
    def __init__(self, customer_id=None, product_id=None, quantity=None):
        self.customer_id = customer_id
        self.product_id = product_id
        self.quantity = quantity

    def get_customer_id(self):
        return self.customer_id

    def get_product_id(self):
        return self.product_id

    def get_quantity(self):
        return self.quantity
    def __str__(self):
        return f"CartItem[CustomerID={self.customer_id}, ProductID={self.product_id}, Quantity={self.quantity}]"