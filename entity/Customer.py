# entity/Customer.py
class Customer:
    def __init__(self, customer_id=None, name=None, email=None, password=None):
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.password = password

    def get_customer_id(self):
        return self.customer_id

    def get_name(self):
        return self.name

    def get_email(self):
        return self.email

    def get_password(self):
        return self.password
    def __str__(self):
        return f"Customer[ID={self.customer_id}, Name={self.name}, Email={self.email}]"
