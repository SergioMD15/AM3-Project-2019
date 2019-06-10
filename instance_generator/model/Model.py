class Model:
    def __init__(self, numWorkers, numProviders):
        self.numWorkers = numWorkers
        self.numProviders = numProviders
        self.cost_worker = []
        self.available_workers = []
        self.cost_contract = []
        self.countries = []

    def getNumWorkers(self):
        return self.numWorkers

    def getNumProviders(self):
        return self.numProviders

    def getCostWorker(self):
        return self.cost_worker

    def getAvailableWorkera(self):
        return self.available_workers

    def getCostContract(self):
        return self.cost_contract

    def getCountries(self):
        return self.countries

