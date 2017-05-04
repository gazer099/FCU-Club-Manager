import password_module
import csv


class User:
    log_in = False
    user_name = None
    user_table = []

    def __init__(self):
        with open('user_table.csv', 'r') as file_user_table:
            for row in csv.DictReader(file_user_table):
                print(row['Name'])
                User.user_table.append(row['Name'])
        print(User.user_table)

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
        print(User.user_table)

    @staticmethod
    # https://openhome.cc/Gossip/Python/WithAs.html
    def verify():
        with open('demo.py', 'r', encoding='UTF-8') as file:
            pass
