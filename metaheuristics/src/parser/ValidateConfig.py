
import os

# Validate config attributes read from a DAT file.
class ValidateConfig(object):
    @staticmethod
    def validate(data):
        # Validate that mandatory input parameters were found
        for paramName in ['inputDataFile', 'solutionFile', 'solver']:
            if(not paramName in data.__dict__):
                raise Exception('Parameter/Set(%s) not contained in Configuration' % str(paramName))

        # Validate input data file
        inputDataFile = data.inputDataFile
        if(len(inputDataFile) == 0):
            raise Exception('Value for inputDataFile is empty')
        if(not os.path.exists(inputDataFile)):
            raise Exception('inputDataFile(%s) does not exist' % inputDataFile)
        
        # Validate solution file
        solutionFile = data.solutionFile
        if(len(solutionFile) == 0):
            raise Exception('Value for solutionFile is empty')

        # Validate max execution time
        if(not 'maxExecTime' in data.__dict__):
                raise Exception('MaxExecTime not contained in Configuration')
        maxExecTime = data.maxExecTime
        if(not isinstance(maxExecTime, (int, float)) or (maxExecTime <= 0)):
                raise Exception('maxExecTime(%s) has to be a positive float value.' % str(maxExecTime))

        # Validate localSearch
        if(not 'localSearch' in data.__dict__):
                raise Exception('localSearch not contained in Configuration')
        localSearch = data.localSearch
        if(not isinstance(localSearch, (bool)) or (localSearch not in [True, False])):
            raise Exception('localSearch(%s) has to be a boolean value.' % str(localSearch))

        
        # Validate solver and per-solver parameters
        solver = data.solver
        if(solver == 'GRASP'):
            # Validate that mandatory input parameters for GRASP solver were found
            for paramName in ['alpha']:
                if(not paramName in data.__dict__):
                    raise Exception('Parameter/Set(%s) not contained in Configuration. Required by GRASP solver.' % str(paramName))
            
            # Validate alpha
            alpha = data.alpha
            if(not isinstance(alpha, (int, float)) or (alpha < 0) or (alpha > 1)):
                raise Exception('alpha(%s) has to be a float value in range [0, 1].' % str(alpha))
        elif(solver == 'Greedy'):
            pass
        else:
            raise Exception('Unsupported solver specified(%s) in Configuration. Supported solvers are: Greedy or GRASP.' % str(solver))