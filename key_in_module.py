import password_module


def sign_up():
    user_name = input('Please input your Username\n>>> ')
    user_password = password_module.set_password()
    print(user_name, user_password)
