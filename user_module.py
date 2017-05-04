class User:
    def __init__(self, name, password):
        self.name = name
        self.password = password

    @staticmethod
    # https://openhome.cc/Gossip/Python/WithAs.html
    def verify():
        with open('demo.py', 'r', encoding='UTF-8') as file:
            pass
