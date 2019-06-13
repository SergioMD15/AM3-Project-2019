from model.Provider import Provider
import sys
sys.path.append("..")


class Problem(object):
    def __init__(self, inputData):
        self.inputData = inputData

        ## Workers & Providers ##
        self.workers = self.inputData.wr
        self.nProviders = self.inputData.nProviders

        ## Arrays ##
        self.cost_worker = list(self.inputData.cost_worker)
        self.available_workers = list(self.inputData.available_workers)
        self.cost_contract = list(self.inputData.cost_contract)
        self.country = list(self.inputData.country)

        ## Costs ##
        self.cost_1 = self.inputData.cost_1
        self.cost_2 = self.inputData.cost_2
        self.cost_3 = self.inputData.cost_3

        self.providers = []
        for i in range(self.nProviders):
            provider = Provider(
                i, self.cost_worker[i], self.available_workers[i], self.cost_contract[i], self.country[i])
            self.providers.append(provider)

        #### CALCULATE SAME COUNTRY ####

        self.same_country = [[0 for i in range(self.nProviders)] for j in range(self.nProviders)] 
        for i in range(0, self.nProviders):
            for j in range(0, self.nProviders):
                if(self.providers[i].get_id() != self.providers[j].get_id()):
                    if(self.providers[i].get_country() == self.providers[j].get_country()):
                        self.providers[i].incompatibilities += 1
                        self.providers[j].incompatibilities += 1
                        self.same_country[i][j] = 1

    def get_providers(self):
        return(self.providers)

    def check_instance(self):
        return sum(self.available_workers) > self.workers
    
    def is_same_country(self, p1, p2):
        return self.same_country[p1.get_id()][p2.get_id()] or self.same_country[p2.get_id()][p1.get_id()]

    def __str__(self):
        aux = ('Workers: %d \n' % self.workers)
        aux += ('Num Providers: %d \n' % self.nProviders)
        aux += ('Cost contracts: [')
        for i in range(self.nProviders):
            aux += ' , %d' % self.providers[i].cost_contract
        aux += ']\n'

        aux += ('Cost workers: [')
        for i in range(self.nProviders):
            aux += ' , %d' % self.providers[i].cost_worker
        aux += ']\n'

        aux += ('Available workers: [')
        for i in range(self.nProviders):
            aux += ' , %d' % self.providers[i].available_workers
        aux += ']\n'

        aux += ('Countries: [')
        for i in range(self.nProviders):
            aux += ' , %d' % self.providers[i].country
        aux += ']\n'
        
        aux += ('Cost_1: %d \n' % self.cost_1)
        aux += ('Cost_2: %d \n' % self.cost_2)
        aux += ('Cost_3: %d \n' % self.cost_3)
        return aux
