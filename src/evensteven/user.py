import uuid
from dataclasses import dataclass, asdict
import json
class User:
    def __init__(self, name):
        self.name = name
        self.id = uuid.uuid4().hex[:8]  # Generate random user ID

    def __str__(self):
        return f"User(id={self.id}, name='{self.name}')"

class Group:
    def __init__(self, name):
        self.id = uuid.uuid4().hex[:8]  # Generate random group ID
        self.name = name
        self.users = []
        self.transations = []

    def add_user(self, user):
        self.users.append(user)

    def delete_user(self, user_id):
        self.users = [user for user in self.users if user.id != user_id]

    def list_all_users(self):
        return self.users

    def change_user(self, user_id, new_name):
        for user in self.users:
            if user.id == user_id:
                user.name = new_name
                return True
        return False

@dataclass
class Manager:
    groups: list = None
    selected_group: any = None

    def __post_init__(self):
        if self.groups is None:
            self.groups = []

    def to_dict(self):
        return asdict(self)

    @staticmethod
    def save_data(manager, file_path):
        data = manager.to_dict()
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)

    @staticmethod
    def load_data(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            return Manager(**data)
        except FileNotFoundError:
            return Manager()

# Example usage:
if __name__ == "__main__":
    users = Group("group1")
    user1 = User("Alice")
    user2 = User("Bob")
    users.add_user(User("Alice"))
    users.add_user(User("Bob"))

    print("List of users:")
    for user in users.list_all_users():
        print(user)

    user_id_to_delete = user1.id
    users.delete_user(user_id_to_delete)
    print("\nAfter deleting user:")
    for user in users.list_all_users():
        print(user)

    user_id_to_change = user2.id
    new_name = "Charlie"
    if users.change_user(user_id_to_change, new_name):
        print("\nAfter changing user name:")
        for user in users.list_all_users():
            print(user)
    else:
        print(f"\nUser with ID {user_id_to_change} not found.")
