'''
AMMM - Course Project Instance generator
'''

import argparse
import sys
from parser import ConfigurationParser as parser
from parser import ConfigurationValidator as validator
from generator.InstanceGenerator import InstanceGenerator


def run():
    aux = argparse.ArgumentParser(description='AMMM - Course Project Instance generator')
    aux.add_argument('file', help='File with the configuration required for the instance')
    params = aux.parse_args()

    print('Parsing the configuration')
    config = parser.ConfigurationParser().parse(params.file)
    validator.ConfigurationValidator().validate(config)
    print('Parsed and validated')

    print('Generating the instance')
    igenerator = InstanceGenerator(config)
    igenerator.generate()
    print('The instance has been succesfully generated.')

    return (0)


if __name__ == '__main__':
    sys.exit(run())