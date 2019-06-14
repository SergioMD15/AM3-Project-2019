class ConfigurationValidator:
    def validate(self, data):
        self.checkAllParams(data)
        self.chekNonEmptyParameters(data)
        self.checkValidTypes(data)


    def checkAllParams(self, data):
        # Check that there are all the parameters needed
        names= ['instancesDirectory' , 'fileName' , 'fileNameExtension', 'minNumWorkers', 'maxNumWorkers' , 'minNumProviders' , 'maxNumProviders' , 'minCostWorker' , 'maxCostWorker' , 'minAvailableWorkers' , 'maxAvailableWorkers' , 'minCostContract' , 'maxCostContract', 'minCountryValue', 'maxCountryValue' , 'cost_1' , 'cost_2' , 'cost_3']
        for name in names:
            if (not name in data.__dict__):
                raise Exception('Parameter (%s) is missing from the given configuration' % str(name))

    def chekNonEmptyParameters(self, data):
        instancesDirectory = data.instancesDirectory
        fileName = data.fileName
        fileNameExtension = data.fileNameExtension
        if (len(instancesDirectory) == 0 or len(fileName) == 0 or len(fileNameExtension) == 0 ):
            raise Exception('The parameters %s, %s, %s must not be empty.' %(instancesDirectory,fileName,fileNameExtension))

    def checkValidTypes(self, data):
        minNumWorkers = data.minNumWorkers
        if (not isinstance(minNumWorkers, int) or (minNumWorkers <= 0)):
            raise Exception('minNumWorkers has to be a positive integer value.' % str(minNumWorkers))

        maxNumWorkers = data.maxNumWorkers
        if (not isinstance(maxNumWorkers, int) or (maxNumWorkers <= 0) or (maxNumWorkers < minNumWorkers)):
            raise Exception('numWorkers has to be a positive integer value.' % str(maxNumWorkers))

        minNumProviders = data.minNumProviders
        if (not isinstance(minNumProviders, int) or (minNumProviders <= 0)):
            raise Exception('minNumProviders has to be a positive integer value.' % str(minNumProviders))

        maxNumProviders = data.maxNumProviders
        if (not isinstance(maxNumProviders, int) or (maxNumProviders <= 0) or (maxNumProviders < minNumProviders)):
            raise Exception('maxNumProviders has to be a positive integer value.' % str(maxNumProviders))

        minCostWorker = data.minCostWorker
        if (not isinstance(minCostWorker, int) or (minCostWorker <= 0)):
            raise Exception('minCostWorker has to be a positive integer value.' % str(minCostWorker))

        maxCostWorker = data.maxCostWorker
        if (not isinstance(maxCostWorker, int) or (maxCostWorker <= 0) or (maxCostWorker < minCostWorker)):
            raise Exception('maxCostWorker(%s) has to be a positive integer value.' % str(maxCostWorker))

        minAvailableWorkers = data.minAvailableWorkers
        if (not isinstance(minAvailableWorkers, int) or (minAvailableWorkers <= 0)):
            raise Exception('minAvailableWorkers(%s) has to be a positive integer value.' % str(minAvailableWorkers))

        maxAvailableWorkers = data.maxAvailableWorkers
        if (not isinstance(maxAvailableWorkers, int) or (maxAvailableWorkers <= 0) or (maxAvailableWorkers < minAvailableWorkers)):
            raise Exception('maxAvailableWorkers has to be a positive integer value.' % str(maxAvailableWorkers))

        minCostContract = data.minCostContract
        if (not isinstance(minCostContract, int) or (minCostContract <= 0)):
            raise Exception('minCostContract has to be a positive integer value.' % str(minCostContract))

        maxCostContract = data.maxCostContract
        if (not isinstance(maxCostContract, int) or (maxCostContract <= 0) or (maxCostContract < minCostContract)):
            raise Exception('maxCostContract has to be a positive integer value.' % str(maxCostContract))

        minCountryValue = data.minCountryValue
        if (not isinstance(minCountryValue, int) or (minCountryValue <= 0)):
            raise Exception('minCountryValue has to be a positive integer value.' % str(minCountryValue))

        maxCountryValue = data.maxCountryValue
        if (not isinstance(maxCountryValue, int) or (maxCountryValue <= 0) or (maxCountryValue < minCountryValue)):
            raise Exception('maxCountryValue has to be a positive integer value.' % str(maxCountryValue))

        cost_1 = data.cost_1
        if (not isinstance(cost_1, int) or (cost_1 <= 0)):
            raise Exception('cost_1 has to be a positive integer value.' % str(cost_1))

        cost_2 = data.cost_2
        if (not isinstance(cost_2, int) or (cost_2 <= 0) or (cost_2 < cost_1)):
            raise Exception('cost_2 has to be a positive integer value.' % str(cost_2))

        cost_3 = data.cost_3
        if (not isinstance(cost_3, int) or (cost_3 <= 0) or (cost_3 < cost_2)):
            raise Exception('cost_3 has to be a positive integer value.' % str(cost_3))