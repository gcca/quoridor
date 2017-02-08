import os
import shutil
import importlib
import argparse


def quoridor():
    parser = argparse.ArgumentParser(description='Quoridor')
    parser.add_argument('target', help='Target unit name')
    parser.add_argument('destination', help='Destination directory.')
    args = parser.parse_args()

    unit = {}
    for filename in os.listdir('units'):
        if filename.endswith('.py'):
            name = filename[:-3]
            lib = importlib.import_module('units.' + name)
            instance = lib.Unit()
            instance.destination = args.destination
            unit[name] = instance

    if os.path.exists(args.destination):
        shutil.rmtree(args.destination)
    os.mkdir(args.destination)

    start_unit(unit, args.target)


def start_unit(unitby, target):
    unit = unitby[target]
    if unit.before:
        for parent_unit in unit.before:
            start_unit(unitby, parent_unit)
    unit.start()


if '__main__' == __name__:
    quoridor()
