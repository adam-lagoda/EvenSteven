"""
An open-source expense splitting app built with Beeware for seamless and equitable bill division among groups, promoting financial transparency and harmony.
"""

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from toga import Button, TextInput, Label, Box, Table, Selection
from evensteven.user import Group, Manager, User
from evensteven.transaction import Transaction

MANAGER = Manager()
BACKGROUND_COLOR="#435585"
TOPBAR_COLOR="#363062"
BUTTON_COLOR="#818FB4"
TEXT_COLOR="#F5E8C7"
# build\evensteven\android\gradle\app\src\main\res\values\colors.xml
# <?xml version="1.0" encoding="utf-8"?>
# <resources>
#     <color name="colorPrimary">#818FB4</color>
#     <color name="colorPrimaryDark">#363062</color>
#     <color name="colorAccent">#818FB4</color>
#     <color name="colorSplashScreenBackground">#435585</color>
# </resources>
class EvenSteven(toga.App):
    def startup(self):
        # Create the UI components
        self.group_name_input = TextInput(placeholder="Enter group name")
        self.group_name_input.style.padding = 20
        self.group_name_input.style.flex = 1
        self.group_name_input.style.color = TEXT_COLOR
        self.group_name_input.style.background_color = BUTTON_COLOR
        create_group_button = Button("Create Group", on_press=self.create_group)
        create_group_button.style.padding = 20
        create_group_button.style.flex = 1
        create_group_button.style.color = TEXT_COLOR
        create_group_button.style.background_color = BUTTON_COLOR
        self.group_selector = Selection(
            "Select Group", items=self.get_groups(), on_change=self.select_group
        )
        self.group_selector.style.padding = 20
        self.group_selector.style.flex = 1
        self.group_selector.style.color = TEXT_COLOR
        self.group_selector.style.background_color = BUTTON_COLOR
        self.user_name_input = TextInput(placeholder="Enter user name")
        self.user_name_input.style.padding = 20
        self.user_name_input.style.flex = 1
        self.user_name_input.style.color = TEXT_COLOR
        self.user_name_input.style.background_color = BUTTON_COLOR
        add_user_button = Button("Add User", on_press=self.add_user)
        add_user_button.style.padding = 20
        add_user_button.style.flex = 1
        add_user_button.style.color = TEXT_COLOR
        add_user_button.style.background_color = BUTTON_COLOR
        self.user_name_delete = Selection(items=self.list_users())
        self.user_name_delete.style.padding = 20
        self.user_name_delete.style.flex = 1
        self.user_name_delete.style.color = TEXT_COLOR
        self.user_name_delete.style.background_color = BUTTON_COLOR
        delete_user_button = Button("Remove User", on_press=self.delete_user)
        delete_user_button.style.padding = 20
        delete_user_button.style.flex = 1
        delete_user_button.style.color = TEXT_COLOR
        delete_user_button.style.background_color = BUTTON_COLOR

        # Create the first OptionContainer
        self.users_in_group_box = toga.DetailedList(
            on_refresh=True, style=Pack(padding=20, flex=1)
        )
        self.users_in_group_box.style.padding = 20
        self.users_in_group_box.style.flex = 1
        self.users_in_group_box.style.color = TEXT_COLOR
        self.users_in_group_box.style.background_color = BACKGROUND_COLOR
        self.update_users_in_group_box()

        self.transaction_name = TextInput(placeholder="Name")
        self.transaction_name.style.padding = 5
        self.transaction_name.style.flex = 1
        self.transaction_name.style.color = TEXT_COLOR
        self.transaction_name.style.background_color = BACKGROUND_COLOR
        self.transaction_paid = Selection("Paid", items=self.list_users())
        self.transaction_paid.style.padding = 5
        self.transaction_paid.style.flex = 1
        self.transaction_paid.style.color = TEXT_COLOR
        self.transaction_paid.style.background_color = BACKGROUND_COLOR
        self.transaction_owes = Selection("Owes", items=self.list_users())
        self.transaction_owes.style.padding = 5
        self.transaction_owes.style.flex = 1
        self.transaction_owes.style.color = TEXT_COLOR
        self.transaction_owes.style.background_color = BACKGROUND_COLOR
        self.transaction_amount = TextInput(placeholder="Amount")
        self.transaction_amount.style.padding = 5
        self.transaction_amount.style.flex = 1
        self.transaction_amount.style.color = TEXT_COLOR
        self.transaction_amount.style.background_color = BACKGROUND_COLOR
        self.transaction_currency = Selection(
            "Currency", items=["PLN", "EUR", "DKK"] #, on_change=self.select_group
        )
        self.transaction_currency.style.padding = 5
        self.transaction_currency.style.flex = 1
        self.transaction_currency.style.color = TEXT_COLOR
        self.transaction_currency.style.background_color = BACKGROUND_COLOR
        add_transaction_button = Button(
            "Add Transaction", on_press=self.add_transaction
        )
        add_transaction_button.style.padding = 20
        add_transaction_button.style.flex = 1
        add_transaction_button.style.color = TEXT_COLOR
        add_transaction_button.style.background_color = BACKGROUND_COLOR

        self.summary_table = Table(headings=["User", "Amount"])
        self.refresh_summary_button = Button(
            "Refresh Summary", on_press=self.refresh_summary
        )

        option_container_1 = Box(style=Pack(direction=COLUMN, padding=0, flex=1, background_color=(BACKGROUND_COLOR)))
        option_container_1.add(
            Box(children=[self.group_name_input, create_group_button]),
            Box(children=[self.group_selector]),
            Box(children=[self.user_name_input, add_user_button]),
            Box(children=[self.user_name_delete, delete_user_button]),
            Box(children=[self.users_in_group_box], style=Pack(flex=1)),
        )

        # Create the second OptionContainer
        transaction_details = Box(style=Pack(direction=COLUMN, padding=0, flex=1, background_color=(BACKGROUND_COLOR)))
        transaction_details.add(
            Box(
                children=[
                    self.transaction_name
                ]
            ),
            Box(
                children=[
                    self.transaction_paid
                ]
            ),
            Box(
                children=[
                    self.transaction_owes
                ]
            ),
            Box(
                children=[
                    self.transaction_amount
                ]
            ),
            Box(
                children=[
                    self.transaction_currency
                ]
            ),
        )
        # transaction_details.style.padding = 20
        # transaction_details.style.flex = 1
        # transaction_details.style.color = TEXT_COLOR
        # transaction_details.style.background_color = BACKGROUND_COLOR
        new_transaction = Box(style=Pack(direction=ROW, padding=0, flex=1, background_color=(BACKGROUND_COLOR)))
        new_transaction.add(
            Box(
                children=[
                    transaction_details
                ], style=Pack(flex=1)
            ),
            Box(
                children=[
                    add_transaction_button
                ], style=Pack(flex=1)
            ),
        )
        option_container_2 = Box(style=Pack(direction=COLUMN, padding=0, flex=1, background_color=(BACKGROUND_COLOR)))
        option_container_2.add(
            Box(
                children=[
                    new_transaction
                ], style=Pack(flex=1)
            ),
            Box(
                children=[
                    Label("Summary:"),
                    self.summary_table,
                    self.refresh_summary_button,
                ]
            ),
        )

        main_box = toga.OptionContainer(
            content=[
                ("Users&Groups", option_container_1, toga.Icon("resources/users")),
                ("Transactions", option_container_2, toga.Icon("resources/transfer")),
            ], style=Pack(color=(BACKGROUND_COLOR))
        )

        # Create the main window
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.content.style.update(direction=COLUMN, flex=0, background_color=(BACKGROUND_COLOR))
        self.main_window.show()

    def create_group(self, widget):
        group_name = self.group_name_input.value.strip()
        if group_name:
            MANAGER.groups.append(Group(group_name))
            self.group_name_input.value = ""
            self.group_selector.items = self.get_groups()
            print(self.group_selector.items)
            print(f"Group '{group_name}' created.")

    def select_group(self, widget):
        group_name = self.group_selector.value.strip()
        _found = False
        for group in MANAGER.groups:
            if group.name == group_name:
                _found = True
                MANAGER.selected_group = group
                self.update_users_in_group_box()
                print(f"Group '{group_name}' has been selected.")
                continue
        if not _found:
            print(f"Group '{group_name}' has not been founds.")

    def get_groups(self):
        return [group.name for group in MANAGER.groups]

    def add_user(self, widget):
        user_name = self.user_name_input.value.strip()
        if user_name:
            MANAGER.selected_group.add_user(User(user_name))
            self.user_name_input.value = ""
            self.transaction_paid.items = self.list_users()
            self.transaction_owes.items = self.list_users()
            self.user_name_delete.items = self.list_users()
            self.update_users_in_group_box()
            print(f"User '{user_name}' added.")

    def delete_user(self, widget):
        user_name = self.user_name_delete.value.strip()
        if user_name:
            for user in MANAGER.selected_group.users:
                if user.name == user_name:
                    user_id = user.id
            MANAGER.selected_group.delete_user(user_id)
            self.user_name_input.value = ""
            self.transaction_paid.items = self.list_users()
            self.transaction_owes.items = self.list_users()
            self.user_name_delete.items = self.list_users()
            self.update_users_in_group_box()
            print(f"User '{user_name}' removed.")

    def list_users(self):
        if MANAGER.selected_group is None:
            return []
        else:
            return [user.name for user in MANAGER.selected_group.users]

    def update_users_in_group_box(self):
        user_list = self.list_users()
        data = []
        for user in set(user_list):
            data.append({"icon": toga.Icon("resources/user"), "title": f"{user}"})
        self.users_in_group_box.data = data

    def add_transaction(self, widget):
        if all(
            self.transaction_name.value,
            self.transaction_paid.value,
            self.transaction_owes.value,
            self.transaction_amount.value,
            self.transaction_currency.value) is not None:
            new_payment = Transaction(
                name=self.transaction_name.value.strip(),
                paid_by=self.transaction_paid.value.strip(),
                owed_by=self.transaction_owes.value.strip(),
                amount=float(self.transaction_owes.value.strip()),
                currency=self.transaction_currency.value.strip()
            )
            MANAGER.selected_group.transactions.apend(new_payment)
            print(
                f"Transaction '{new_payment.name}' added with amount '{new_payment.amount}'."
            )

    def refresh_summary(self, widget):
        # Your logic to refresh the summary
        print("Refreshing summary...")


def main():
    return EvenSteven()
