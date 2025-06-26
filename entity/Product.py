# entity/Product.py
class Product:
    def __init__(self, product_id=None, name=None, price=None, description=None, stock_quantity=None):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.description = description
        self.stock_quantity = stock_quantity

    def get_product_id(self):
        return self.product_id

    def get_name(self):
        return self.name

    def get_price(self):
        return self.price

    def get_description(self):
        return self.description

    def get_stock_quantity(self):
        return self.stock_quantity
    def __str__(self):
        return f"Product[ID={self.product_id}, Name={self.name}, Price={self.price}]"
