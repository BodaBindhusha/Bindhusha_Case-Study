# exception/CustomerNotFoundException.py
class CustomerNotFoundException(Exception):
    """Raised when a customer ID is not found in the database."""
    def __init__(self, message="Customer not found."):
        super().__init__(message)

