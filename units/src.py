import os


class Unit:

    before = []

    def start(self):
        os.mkdir(os.path.join(self.destination, 'src'))
        print('SRC created')
