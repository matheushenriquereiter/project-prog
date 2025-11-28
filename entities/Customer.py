class Customer:
    def __init__(self, id, username, email, password):
        self.id = id
        self.username = username
        self.email = email
        self.password = password

    def get_info(self):
        return (
            f"Username: {self.username}, Email: {self.email}, Password: {self.password}"
        )
