import time
from solver.Logger import Logger


class Solver(object):
    def __init__(self):
        logFields = []
        logFields.append({'id': 'elapTime',   'name': 'Elap. Time (s)',
                          'headerformat': '{:>14s}', 'valueformat': '{:>14.8f}'})
        logFields.append({'id': 'objValue',   'name': 'Obj. Value',
                          'headerformat': '{:>10s}', 'valueformat': '{:>10.1f}'})
        logFields.append({'id': 'workers',   'name': 'Workers Hired',
                          'headerformat': '{:>10s}', 'valueformat': '{:>10.1f}'})
        logFields.append({'id': 'iterations', 'name': 'Iterations',
                          'headerformat': '{:>12s}', 'valueformat': '{:>12d}'})
        self.logger = Logger(fields=logFields)
        self.logger.printHeaders()

    def startTimeMeasure(self):
        self.startTime = time.time()

    def writeLogLine(self, objValue, workers, iterations):
        logValues = {}
        logValues['elapTime'] = time.time() - self.startTime
        logValues['objValue'] = objValue
        logValues['workers'] = workers
        logValues['iterations'] = iterations
        self.logger.printValues(logValues)

    def solve(self, config, problem):
        raise Exception('Abstract method cannot be called')
