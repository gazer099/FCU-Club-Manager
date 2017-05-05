import password_module
import csv


class User:
    log_in = False
    user_name = None
    user_table = []
    user_dict = {}

    def __init__(self):
        self.load_user_table()

    def sign_up(self):
        self.user_name = input('Please input your Username\n>>> ')
        while self.user_name in User.user_table:
            self.user_name = input('This name is be use, try another\n>>> ')
        user_password = password_module.set_password()
        # user_password = '########################'
        User.user_table.append(self.user_name)
        with open('user_table.csv', 'a', newline='') as file_user_table:
            w = csv.writer(file_user_table)
            w.writerow([self.user_name, user_password])
        self.user_dict[self.user_name] = user_password
        print(User.user_table)
        print('Account Create!!')

    def log_in(self):
        self.user_name = input('Username\n>>> ')
        if self.pass_verify(self.user_name):
            print('Username NOT found')
        password_hash = password_module.receive_password_hash()

    # https://openhome.cc/Gossip/Python/WithAs.html
    def pass_verify(self, username):
        if username not in User.user_table:
            return False

    def load_user_table(self):
        with open('user_table.csv', 'r') as file_user_table:
            for row in csv.DictReader(file_user_table):
                print(row['Name'])
                User.user_table.append(row['Name'])
                self.user_dict[row['Name']] = row['Password']
        print(User.user_table)
