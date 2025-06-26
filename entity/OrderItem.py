# entity/OrderItem.py
class OrderItem:
    def __init__(self, item_id=None, order_id=None, product_id=None, quantity=None):
        self.item_id = item_id
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity

    def get_item_id(self):
        return self.item_id

    def get_order_id(self):
        return self.order_id

    def get_product_id(self):
        return self.product_id

    def get_quantity(self):
        return self.quantity
    def __str__(self):
        return f"OrderItem[ItemID={self.item_id}, ProductID={self.product_id}, Quantity={self.quantity}]"
