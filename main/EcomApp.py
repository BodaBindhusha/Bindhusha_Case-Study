import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from entity.Customer import Customer
from entity.Product import Product
from dao.OrderProcessorRepositoryImpl import OrderProcessorRepositoryImpl
from exception.CustomerNotFoundException import CustomerNotFoundException
from exception.ProductNotFoundException import ProductNotFoundException

def show_menu():
    print("\n========= E-COMMERCE MENU =========")
    print("1. Register Customer")
    print("2. Create Product")
    print("3. Delete Product")
    print("4. Add to Cart")
    print("5. View Cart")
    print("6. Place Order")
    print("7. View Customer Orders")
    print("8. Product Order Summary")
    print("9. Most Purchased Products")
    print("10. Customer Purchase Summary")
    print("11. Product Stock vs Sales Report")
    print("12. Exit")
    print("===================================")

# STEP 1: Validate customer input
def get_validated_customer_input():
    name = input("Enter name: ").strip()
    email = input("Enter email: ").strip()
    password = input("Enter password (min 6 chars): ").strip()

    if '@' not in email or '.' not in email:
        print("❌ Invalid email format.")
        return None
    if len(password) < 6:
        print("❌ Password too short.")
        return None

    return Customer(name=name, email=email, password=password)

# STEP 2: Validate product input
def get_validated_product_input():
    name = input("Enter product name: ").strip()
    try:
        price = float(input("Enter price: "))
        if price <= 0:
            print("❌ Price must be greater than 0.")
            return None
        stock = int(input("Enter stock quantity: "))
        if stock < 0:
            print("❌ Stock must be non-negative.")
            return None
    except ValueError:
        print("❌ Invalid numeric input.")
        return None

    description = input("Enter description: ").strip()
    return Product(name=name, price=price, description=description, stock_quantity=stock)

def main():
    repo = OrderProcessorRepositoryImpl()

    while True:
        show_menu()
        choice = input("Enter your choice (1-12): ").strip()

        try:
            if choice == '1':
                customer = get_validated_customer_input()
                if not customer:
                    continue
                if repo.create_customer(customer):
                    print("✅ Customer registered successfully!")
                else:
                    print("❌ Customer registration failed.")

            elif choice == '2':
                product = get_validated_product_input()
                if not product:
                    continue
                if repo.create_product(product):
                    print("✅ Product added successfully!")
                else:
                    print("❌ Failed to add product.")

            elif choice == '3':
                try:
                    product_id = int(input("Enter product ID to delete: "))
                    if repo.delete_product(product_id):
                        print("✅ Product deleted.")
                except ValueError:
                    print("❌ Please enter a valid product ID.")

            elif choice == '4':
                try:
                    customer_id = int(input("Enter your customer ID: "))
                    product_id = int(input("Enter product ID to add: "))
                    quantity = int(input("Enter quantity: "))
                    if quantity <= 0:
                        print("❌ Quantity must be positive.")
                        continue

                    customer = Customer(customer_id=customer_id)
                    product = Product(product_id=product_id)

                    if repo.add_to_cart(customer, product, quantity):
                        print("✅ Product added to cart.")
                    else:
                        print("❌ Failed to add to cart.")
                except ValueError:
                    print("❌ Please enter valid numeric values.")

            elif choice == '5':
                customer_id = int(input("Enter your customer ID: "))
                customer = Customer(customer_id=customer_id)
                items = repo.get_all_from_cart(customer)

                if items:
                    print("🛒 Your Cart Items:")
                    for item in items:
                        print(f"📦 {item['name']} - ₹{item['price']} x {item['quantity']}")
                else:
                    print("🛒 Your cart is empty.")

            elif choice == '6':
                customer_id = int(input("Enter your customer ID: "))
                customer = Customer(customer_id=customer_id)
                shipping = input("Enter shipping address: ")

                cart_items = repo.get_all_from_cart(customer)
                if not cart_items:
                    print("❌ Your cart is empty.")
                    continue

                product_quantity_list = []
                for item in cart_items:
                    product = Product(product_id=item['product_id'], price=item['price'])
                    product_quantity_list.append({product: item['quantity']})

                if repo.place_order(customer, product_quantity_list, shipping):
                    print("✅ Order placed successfully!")
                else:
                    print("❌ Failed to place order.")

            elif choice == '7':
                customer_id = int(input("Enter your customer ID: "))
                orders = repo.get_orders_by_customer(customer_id)
                if orders:
                    for order in orders:
                        print("\n🧾 Order ID:", order['order_id'])
                        print("   Total: ₹", order['total_price'])
                        print("   Date:", order['order_date'])
                        print("   Address:", order['shipping_address'])
                        print("   Items:")
                        for item in order['items']:
                            print(f"     📦 Product ID: {item['product_id']} - Qty: {item['quantity']}")
            
                else:
                    print("❌ No orders found.")

            elif choice == '8':
                print("👋 Exiting the application. Thank you!")
                break

            elif choice == '8':
                summary = repo.get_product_order_summary()
                if summary:
                    print("\n📊 Product Order Summary:")
                    for row in summary:
                        print(f"📦 Product: {row['product_name']} | Total Sold: {row['total_quantity_sold']} | Revenue: ₹{row['total_revenue']}")
                else:
                    print("ℹ️ No order data available.")
            elif choice == '9':
                top_products = repo.get_most_purchased_products(5)
                print("\n🔥 Most Purchased Products:")
                for p in top_products:
                    print(f"📦 {p['product_name']} - Sold: {p['total_quantity_sold']} units")

            elif choice == '10':
                summary = repo.get_customer_purchase_summary()
                print("\n🧑‍💼 Customer Purchase Summary:")
                for c in summary:
                    print(f"👤 {c['name']} - Orders: {c['total_orders']} - Spent: ₹{c['total_spent']}")

            elif choice == '11':
                stock_report = repo.get_product_stock_vs_sales()
                print("\n📊 Product Stock vs Sales:")
                for p in stock_report:
                    print(f"📦 {p['product_name']} - Stock: {p['current_stock']}, Sold: {p['total_sold']}")
            elif choice == '12':
                print("👋 Exiting the application. Thank you!")
                break
            else:
                print("⚠️ Invalid choice. Please enter a number between 1 and 12.")
        except CustomerNotFoundException as e:
            print("🚫", e)
        except ProductNotFoundException as e:
            print("🚫", e)
        except ValueError:
            print("⚠️ Please enter valid numeric input.")
        except Exception as e:
            print(f"❗ Unexpected Error: {e}")

if __name__ == "__main__":
    main()
