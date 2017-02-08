import os
import json


class Unit:

    before = ['package']

    def start(self):
        package_path = os.path.join(self.destination, 'package.json')
        with open(package_path) as package_file:
            package = json.load(package_file)

        package['devDependencies']['typescript'] = '~2.0.10'

        with open(package_path, 'w') as package_file:
            json.dump(package, package_file, indent=2)

        print('TypeScript created')
