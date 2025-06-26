# dao/OrderProcessorRepositoryImpl.py
import mysql.connector
from dao.OrderProcessorRepository import OrderProcessorRepository
from util.DBConnUtil import DBConnUtil
from exception.CustomerNotFoundException import CustomerNotFoundException
from exception.ProductNotFoundException import ProductNotFoundException
from exception.OrderNotFoundException import OrderNotFoundException
from entity.Customer import Customer
from entity.Product import Product

class OrderProcessorRepositoryImpl(OrderProcessorRepository):
    def __init__(self):
        self.conn = DBConnUtil.getConnection()
        self.cursor = self.conn.cursor(dictionary=True)

    def create_customer(self, customer: Customer):
        try:
            query = "INSERT INTO customers (name, email, password) VALUES (%s, %s, %s)"
            values = (customer.get_name(), customer.get_email(), customer.get_password())
            self.cursor.execute(query, values)
            self.conn.commit()
            return True
        except Exception as e:
            print(f"[ERROR] create_customer: {e}")
            return False

    def create_product(self, product: Product):
        try:
            query = """
                INSERT INTO products (name, price, description, stockQuantity)
                VALUES (%s, %s, %s, %s)
            """
            values = (
                product.get_name(),
                product.get_price(),
                product.get_description(),
                product.get_stock_quantity()
            )
            self.cursor.execute(query, values)
            self.conn.commit()
            return True
        except Exception as e:
            print(f"[ERROR] create_product: {e}")
            return False

    def delete_product(self, product_id):
        try:
            self.cursor.execute("SELECT * FROM products WHERE product_id = %s", (product_id,))
            if not self.cursor.fetchone():
                raise ProductNotFoundException(f"Product ID {product_id} not found.")
            self.cursor.execute("DELETE FROM products WHERE product_id = %s", (product_id,))
            self.conn.commit()
            return True
        except ProductNotFoundException:
            raise
        except Exception as e:
            print(f"[ERROR] delete_product: {e}")
            return False

    def delete_customer(self, customer_id):
        try:
            self.cursor.execute("SELECT * FROM customers WHERE customer_id = %s", (customer_id,))
            if not self.cursor.fetchone():
                raise CustomerNotFoundException(f"Customer ID {customer_id} not found.")
            self.cursor.execute("DELETE FROM customers WHERE customer_id = %s", (customer_id,))
            self.conn.commit()
            return True
        except CustomerNotFoundException:
            raise
        except Exception as e:
            print(f"[ERROR] delete_customer: {e}")
            return False

    def add_to_cart(self, customer: Customer, product: Product, quantity: int):
        try:
            query = "INSERT INTO cart (customer_id, product_id, quantity) VALUES (%s, %s, %s)"
            values = (customer.get_customer_id(), product.get_product_id(), quantity)
            self.cursor.execute(query, values)
            self.conn.commit()
            return True
        except Exception as e:
            print(f"[ERROR] add_to_cart: {e}")
            return False

    def remove_from_cart(self, customer: Customer, product: Product):
        try:
            query = "DELETE FROM cart WHERE customer_id = %s AND product_id = %s"
            values = (customer.get_customer_id(), product.get_product_id())
            self.cursor.execute(query, values)
            self.conn.commit()
            return True
        except Exception as e:
            print(f"[ERROR] remove_from_cart: {e}")
            return False

    def get_all_from_cart(self, customer: Customer):
        try:
            query = """
                SELECT p.product_id, p.name, p.price, c.quantity 
                FROM cart c
                JOIN products p ON c.product_id = p.product_id 
                WHERE c.customer_id = %s
            """
            self.cursor.execute(query, (customer.get_customer_id(),))
            return self.cursor.fetchall()
        except Exception as e:
            print(f"[ERROR] get_all_from_cart: {e}")
            return []

    def place_order(self, customer: Customer, product_quantity_list: list, shipping_address: str):
        try:
            total_price = sum(
                product.get_price() * quantity
                for item in product_quantity_list
                for product, quantity in item.items()
            )

            order_query = """
                INSERT INTO orders (customer_id, order_date, total_price, shipping_address)
                VALUES (%s, NOW(), %s, %s)
            """
            self.cursor.execute(order_query, (customer.get_customer_id(), total_price, shipping_address))
            order_id = self.cursor.lastrowid

            for item in product_quantity_list:
                for product, quantity in item.items():
                    item_query = """
                        INSERT INTO order_items (order_id, product_id, quantity)
                        VALUES (%s, %s, %s)
                    """
                    self.cursor.execute(item_query, (order_id, product.get_product_id(), quantity))

            self.cursor.execute("DELETE FROM cart WHERE customer_id = %s", (customer.get_customer_id(),))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"[ERROR] place_order: {e}")
            return False

    def get_orders_by_customer(self, customer_id: int):
        try:
            self.cursor.execute("SELECT * FROM orders WHERE customer_id = %s", (customer_id,))
            orders = self.cursor.fetchall()
            if not orders:
                raise CustomerNotFoundException(f"No orders found for Customer ID {customer_id}.")

            order_details = []
            for order in orders:
                self.cursor.execute("SELECT * FROM order_items WHERE order_id = %s", (order['order_id'],))
                items = self.cursor.fetchall()
                order_details.append({
                    "order_id": order['order_id'],
                    "total_price": order['total_price'],
                    "shipping_address": order['shipping_address'],
                    "order_date": order['order_date'],
                    "items": items
                })

            return order_details
        except CustomerNotFoundException:
            raise
        except Exception as e:
            print(f"[ERROR] get_orders_by_customer: {e}")
            return []
        
    def get_top_customers_by_spending(self, min_total_spent=1000):
        try:
            query = """
                SELECT c.customer_id, c.name, SUM(o.total_price) as total_spent
                FROM customers c
                JOIN orders o ON c.customer_id = o.customer_id
                GROUP BY c.customer_id
                HAVING total_spent >= %s
                ORDER BY total_spent DESC
            """
            self.cursor.execute(query, (min_total_spent,))
            return self.cursor.fetchall()
        except Exception as e:
            print(f"[ERROR] get_top_customers_by_spending: {e}")
            return []
    
    def get_product_order_summary(self):
        try:
            query = """
                SELECT 
                    p.product_id,
                    p.name AS product_name,
                    SUM(oi.quantity) AS total_quantity_sold,
                    SUM(oi.quantity * p.price) AS total_revenue
                FROM 
                    order_items oi
                JOIN 
                    products p ON oi.product_id = p.product_id
                GROUP BY 
                    p.product_id, p.name
            """
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"[ERROR] get_product_order_summary: {e}")
            return []
    def get_most_purchased_products(self, top_n=5):
        try:
            query = """
                SELECT 
                    p.product_id,
                    p.name AS product_name,
                    SUM(oi.quantity) AS total_quantity_sold
                FROM 
                    order_items oi
                JOIN 
                    products p ON oi.product_id = p.product_id
                GROUP BY 
                    p.product_id, p.name
                ORDER BY 
                    total_quantity_sold DESC
                LIMIT %s
            """
            self.cursor.execute(query, (top_n,))
            return self.cursor.fetchall()
        except Exception as e:
            print(f"[ERROR] get_most_purchased_products: {e}")
            return []
    def get_customer_purchase_summary(self):
        try:
            query = """
                SELECT 
                    c.customer_id,
                    c.name,
                    COUNT(o.order_id) AS total_orders,
                    SUM(o.total_price) AS total_spent
                FROM 
                    customers c
                JOIN 
                    orders o ON c.customer_id = o.customer_id
                GROUP BY 
                    c.customer_id, c.name
                ORDER BY 
                    total_spent DESC
            """
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"[ERROR] get_customer_purchase_summary: {e}")
            return []
    def get_product_stock_vs_sales(self):
        try:
            query = """
                SELECT 
                    p.product_id,
                    p.name AS product_name,
                    p.stockQuantity AS current_stock,
                    IFNULL(SUM(oi.quantity), 0) AS total_sold
                FROM 
                    products p
                LEFT JOIN 
                    order_items oi ON p.product_id = oi.product_id
                GROUP BY 
                    p.product_id, p.name, p.stockQuantity
            """
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"[ERROR] get_product_stock_vs_sales: {e}")
            return []



