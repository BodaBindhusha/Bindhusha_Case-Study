# entity/Order.py
class Order:
    def __init__(self, order_id=None, customer_id=None, order_date=None, total_price=None, shipping_address=None):
        self.order_id = order_id
        self.customer_id = customer_id
        self.order_date = order_date
        self.total_price = total_price
        self.shipping_address = shipping_address

    def get_order_id(self):
        return self.order_id

    def get_customer_id(self):
        return self.customer_id

    def get_order_date(self):
        return self.order_date

    def get_total_price(self):
        return self.total_price

    def get_shipping_address(self):
        return self.shipping_address
    def __str__(self):
        return f"Order[ID={self.order_id}, CustomerID={self.customer_id}, Total={self.total_price}]"

    