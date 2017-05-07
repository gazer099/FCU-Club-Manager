import csv
import password_module


class User:
    user_dict = {}
    username = None

    def __init__(self):
        self.load_data_in_table()
        print(self.user_dict)

    def load_data_in_table(self):
        with open('user_table.csv', 'r') as file_user_table:
            for row in csv.DictReader(file_user_table):
                self.user_dict[row['Name']] = row['Password']

    def sign_up(self):
        # set username
        username = input('Please input your Username\n>>> ')
        while username in User.user_dict:
            username = input('This name is be use, try another\n>>> ')
        # set password
        password = password_module.set_password()
        password_digest = password_module.get_digest(password.encode())
        # add user into csv
        self.add_user_into_csv(username, password_digest)
        # add user into user_dict
        self.add_user_into_dict(username, password_digest)

    def sgin_in(self):
        pass

    def is_log_in(self, user, password_digest):
        pass

    def add_user_into_csv(self, username, password_digest):
        with open('user_table.csv', 'a', newline='') as file_user_table:
            w = csv.writer(file_user_table)
            w.writerow([username, password_digest])

    def add_user_into_dict(self, username, password_digest):
        User.user_dict[username] = password_digest
