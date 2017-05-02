import hashlib
import getpass


def get_digest(password):
    return hashlib.sha256(password).hexdigest()


def is_password(password, digest):
    return get_digest(password) == digest


def set_password():
    password = getpass.getpass('Please input your Password\n>>> (Cannot see)')
    if len(password) < 8 or password == '':
        print('<<Your password format is incorrect, Please try again>>')
        return set_password()

    password_again = getpass.getpass('Please input your Password AGAIN\n>>> (Cannot see)')

    if password != password_again:
        print('<<Your password entry is inconsistent, Please try again>>')
        return set_password()
    else:
        return get_digest(password.encode())
