# exception/ProductNotFoundException.py
class ProductNotFoundException(Exception):
    """Raised when a product ID is not found in the database."""
    def __init__(self, message="Product not found."):
        super().__init__(message)


