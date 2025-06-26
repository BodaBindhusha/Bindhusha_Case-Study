from exception.CustomerNotFoundException import CustomerNotFoundException
try:
    raise CustomerNotFoundException("No such customer exists!")
except CustomerNotFoundException as e:
    print(e)
def test_get_most_purchased_products(repo):
    result = repo.get_most_purchased_products(3)
    assert isinstance(result, list)

def test_get_customer_purchase_summary(repo):
    result = repo.get_customer_purchase_summary()
    assert isinstance(result, list)

def test_get_product_stock_vs_sales(repo):
    result = repo.get_product_stock_vs_sales()
    assert isinstance(result, list)
