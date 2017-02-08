import os
import json


CONTENT = '''{
  "name": "CiX-Lab",
  "version": "0.0.0",
  "description": "CiX Lab.",
  "scripts": {
    "build": "tsc -p src/",
    "build:watch": "tsc -p src/ -w",
    "serve": "lite-server -c=bs-config.json",
    "start": "concurrently \\"npm run build:watch\\" \\"npm run serve\\""
  },
  "keywords": [],
  "author": "",
  "license": "CiX",
  "dependencies": {
    "systemjs": "0.19.40",
    "core-js": "^2.4.1",
    "rxjs": "5.0.1",
    "zone.js": "^0.7.4"
  },
  "devDependencies": {
    "concurrently": "^3.1.0",
    "lite-server": "^2.2.2",
    "@types/node": "^6.0.46",
    "@types/jasmine": "^2.5.36"
  },
  "repository": {}
}
'''


class Unit:

    before = []

    def start(self):
        dest = os.path.join(self.destination, 'package.json')
        with open(dest, 'w') as pjsonfile:
            pjsonfile.write(CONTENT)
        print('Package created')
