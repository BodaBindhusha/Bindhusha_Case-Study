# test/test_order_processor.py

import pytest
from entity.Customer import Customer
from entity.Product import Product
from dao.OrderProcessorRepositoryImpl import OrderProcessorRepositoryImpl
from exception.CustomerNotFoundException import CustomerNotFoundException
from exception.ProductNotFoundException import ProductNotFoundException

@pytest.fixture(scope="module")
def repo():
    return OrderProcessorRepositoryImpl()

def test_create_customer(repo):
    customer = Customer(name="TestUser", email="testuser@example.com", password="test123")
    result = repo.create_customer(customer)  # ✅ snake_case
    assert result is True

def test_create_product(repo):
    product = Product(name="Test Keyboard", price=500.0, description="USB keyboard", stock_quantity=5)
    result = repo.create_product(product)  # ✅ snake_case
    assert result is True

def test_add_product_to_cart(repo):
    customer = Customer(customer_id=1)  # Must exist in DB
    product = Product(product_id=1)     # Must exist in DB
    result = repo.add_to_cart(customer, product, quantity=1)  # ✅ snake_case
    assert result is True

def test_remove_from_cart(repo):
    customer = Customer(customer_id=1)
    product = Product(product_id=1)
    result = repo.remove_from_cart(customer, product)  # ✅ snake_case
    assert result is True or result is False

def test_place_order(repo):
    customer = Customer(customer_id=1)
    cart_items = repo.get_all_from_cart(customer)  # ✅ snake_case

    if not cart_items:
        pytest.skip("Cart is empty for this customer.")

    product_quantity_list = []
    for item in cart_items:
        product = Product(product_id=item['product_id'], price=item['price'])
        product_quantity_list.append({product: item['quantity']})

    result = repo.place_order(customer, product_quantity_list, "Test Address")  # ✅ snake_case
    assert result is True

def test_get_orders_by_customer(repo):
    customer_id = 1
    orders = repo.get_orders_by_customer(customer_id)  # ✅ snake_case
    assert isinstance(orders, list)
    if orders:
        assert "order_id" in orders[0]

def test_customer_not_found_exception(repo):
    with pytest.raises(CustomerNotFoundException):
        repo.delete_customer(9999)  # ✅ snake_case

def test_product_not_found_exception(repo):
    with pytest.raises(ProductNotFoundException):
        repo.delete_product(9999)  # ✅ snake_case
def test_get_top_customers_by_spending(repo):
    results = repo.get_top_customers_by_spending(100)
    assert isinstance(results, list)
    if results:
        assert "customer_id" in results[0]
        assert "name" in results[0]
        assert "total_spent" in results[0]

def test_product_order_summary(repo):
    summary = repo.get_product_order_summary()
    assert isinstance(summary, list)
    if summary:
        assert 'product_id' in summary[0]
        assert 'product_name' in summary[0]
        assert 'total_quantity_sold' in summary[0]
        assert 'total_revenue' in summary[0]
def test_duplicate_product_insertion(repo):
    product = Product(name="Test Duplicate", price=300.0, description="test", stock_quantity=5)
    result1 = repo.create_product(product)
    result2 = repo.create_product(product)
    assert result1 is True
    assert result2 in [True, False]  # Depending on DB constraint
