import os
import random
import math
from model.Model import Model


class InstanceGenerator:
    def __init__(self, data):
        self.data = data

        instancesDirectory = self.data.instancesDirectory

        if (not os.path.isdir(instancesDirectory)):
            raise Exception('Directory(%s) does not exist' %
                            instancesDirectory)

    def generate(self):
        workers_to_generate = random.randint(
            self.data.minNumWorkers, self.data.maxNumWorkers)
        providers_to_generate = random.randint(
            self.data.minNumProviders, self.data.maxNumProviders)
        self.model = Model(workers_to_generate, providers_to_generate)

        self.printToFile()

    def printToFile(self):
        fileToWrite = open(self.data.instancesDirectory + '/' +
                           self.data.fileName + '.' + self.data.fileNameExtension, 'w')

        # Write workers
        aux_str = 'wr=' + str(self.model.numWorkers) + ';\n'
        fileToWrite.write(aux_str)

        # Write providers
        aux_str = 'nProviders=' + str(self.model.numProviders) + ';\n\n'
        fileToWrite.write(aux_str)

        # Write cost_workers
        aux_str = 'cost_worker=['
        for i in range(self.model.numProviders):
            aux_str += ' ' + \
                str(random.randint(self.data.minNumWorkers, self.data.maxNumWorkers))
        aux_str += ' ];\n'
        fileToWrite.write(aux_str)

        # Write available_workers
        aux_str = 'available_workers=['
        for i in range(self.model.numProviders):
            aux_str += ' ' + \
                str(random.randint(self.data.minAvailableWorkers,
                                   self.data.maxAvailableWorkers))
        aux_str += ' ];\n'
        fileToWrite.write(aux_str)

        # Write cost_contract
        aux_str = 'cost_contract=['
        for i in range(self.model.numProviders):
            aux_str += ' ' + \
                str(random.randint(self.data.minCostContract,
                                   self.data.maxCostContract))
        aux_str += ' ];\n'
        fileToWrite.write(aux_str)

        # Write countries
        aux_str = 'country=['
        for i in range(self.model.numProviders):
            aux_str += ' ' + \
                str(random.randint(self.data.minCountryValue,
                                   self.data.maxCountryValue))
        aux_str += ' ];\n'
        fileToWrite.write(aux_str)

        # Write cost1
        fileToWrite.write('cost_1=%s;\n' % (self.data.cost_1))

        # Write cost2
        fileToWrite.write('cost_2=%s;\n' % (self.data.cost_2))

        # Write cost3
        fileToWrite.write('cost_3=%s;\n' % (self.data.cost_3))
