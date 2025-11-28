class Customer:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def get_info(self):
        return (
            f"Username: {self.username}, Email: {self.email}, Password: {self.password}"
        )
