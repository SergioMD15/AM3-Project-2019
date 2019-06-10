
import copy
import time
from model.Assigns import Assigns
from model.Drives import Drives
import sys
sys.path.append("..")

# Implementation of a local search using First Improvement and Reassignment.


class LocalSearch(object):
    def __init__(self, config):
        self.enabled = config.localSearch
        self.nhStrategy = 'Reassignment'
        self.policy = 'FirstImprovement'

        self.elapsedTime = 0
        self.iterations = 0


    def getServiceCost(self, service, solution):
        solServices = self.getSolutionServices(solution)

        assigns = solution.get_hiring_assigned(service)
        drives = solution.getServiceDriven(service)


        busCost = service.getDuration() * assigns.getBus().getEurosMin() + \
            service.getKm() * assigns.getBus().getEurosKm()

        extra = self.calculateExtra(drives.getDriver(), solution.drives)
        ratio = extra / len(solServices)

        driverCost = service.getDuration() - ratio * drives.getDriver().getCBM() + \
            ratio * drives.getDriver().getCEM()

        return busCost + driverCost

    def getSolutionServices(self, solution):
        solServices = []
        for s in solution.drives:
            solServices.append(s.getService())
        return solServices

    def isFeasibleAssign(self, service, bus, solution):
        aux = 0
        for a in solution.assignments:
            if a.getBus() == bus:
                aux += solution.collides[service.getId()][a.getService().getId()]
        return bus.getCapacity() >= service.getPassengers() and aux == 0

    def isFeasibleDrives(self, service, driver, solution):
        timeWorked = 0
        for d in solution.drives:
            if d.getDriver() == driver:
                timeWorked += d.getService().getDuration()
        checkCollisions = 0
        for d in solution.drives:
            if d.getDriver() == driver:
                checkCollisions += solution.collides[service.getId()
                                                     ][d.getService().getId()]
        timeWorked += service.getDuration()
        return d.getDriver().getMaxMinutes() >= timeWorked and checkCollisions == 0

    def calculateExtra(self, driver, drives):
        aux = 0
        for d in drives:
            if(d.getDriver() == driver):
                aux += d.getService().getDuration()
        return max(0, aux - driver.getBM())

    def exploreNeighborhood(self, solution):
        buses = solution.getBuses()
        drivers = solution.getDrivers()
        services = solution.getServices()

        curCost = solution.calculateCost()
        bestNeighbor = copy.deepcopy(solution)

        if(self.nhStrategy == 'Reassignment'):
            sortedServices = sorted(
                services, key=lambda service: self.getServiceCost(service, bestNeighbor), reverse=False)

            for service in sortedServices:
                for bus in buses:
                    if(self.isFeasibleAssign(service, bus, bestNeighbor)):
                        auxSolution = copy.deepcopy(bestNeighbor)
                        auxSolution.removeAssign(service)
                        auxSolution.assignments.append(Assigns(service, bus))
                        auxCost = auxSolution.calculateCost()
                        if(auxCost <= curCost):
                            bestNeighbor = auxSolution
                            curCost = auxCost
                            break
                
                for driver in drivers:
                    if(self.isFeasibleDrives(service, driver, bestNeighbor)):
                        auxSolution = copy.deepcopy(bestNeighbor)
                        auxSolution.removeDrives(service)
                        auxSolution.drives.append(Drives(service, driver))
                        auxCost = auxSolution.calculateCost()
                        if(auxCost <= curCost):
                            bestNeighbor = auxSolution
                            curCost = auxCost
                            break

        else:
            raise Exception('Unsupported NeighborhoodStrategy(%s)' %
                            self.nhStrategy)

        return(bestNeighbor)

    def run(self, solution):
        if(not self.enabled):
            return(solution)
        if(not solution.isFeasible()):
            return(solution)

        bestSolution = solution
        bestCost = bestSolution.calculateCost()

        startEvalTime = time.time()
        iterations = 0

        # keep iterating while improvements are found
        keepIterating = True
        while(keepIterating):
             keepIterating = False
             iterations += 1

             neighbor = self.exploreNeighborhood(bestSolution)
             curCost = neighbor.calculateCost()
             if(bestCost > curCost):
                bestSolution = neighbor
                bestCost = curCost
                keepIterating = True

        self.iterations += iterations
        self.elapsedTime += time.time() - startEvalTime

        return(bestSolution)

    def printPerformance(self):
        if(not self.enabled):
            return

        avg_evalTimePerIteration = 0.0
        if(self.iterations != 0):
            avg_evalTimePerIteration = 1000.0 * \
                self.elapsedTime / float(self.iterations)

        print('')
        print('Local Search Performance:')
        print('  Num. Iterations Eval.', self.iterations)
        print('  Total Eval. Time     ', self.elapsedTime, 's')
        print('  Avg. Time / Iteration', avg_evalTimePerIteration, 'ms')
