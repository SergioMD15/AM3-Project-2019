from model.Model import Model
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

        self.same_country = [[0 for x in range(self.nProviders)] for y in range(self.nProviders)] 
        for i in range(0, self.nProviders):
            for j in range(0, self.nProviders):
                if(self.providers[i].get_id() != self.providers[j].get_id()):
                    if(self.providers[i].get_country() == self.providers[j].get_country()):
                        self.same_country[i][j] = 1

    def get_providers(self):
        return(self.providers)

    def check_instance(self):
        return sum(self.available_workers) > self.workers
    
    def is_same_country(self, p1, p2):
        return self.same_country[p1][p2] or self.same_country[p2][p1]
