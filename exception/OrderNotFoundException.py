# exception/OrderNotFoundException.py
class OrderNotFoundException(Exception):
    """Raised when an order ID is not found in the database."""
    def __init__(self, message="Order not found."):
        super().__init__(message)


