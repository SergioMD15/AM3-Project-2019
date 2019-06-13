
import random
import time
import sys
from heuristics.LocalSearch import LocalSearch
sys.path.append("..")
from solver.Solver import Solver
from solver.Solution import Solution

# Inherits from a parent abstract solver.


class GRASP_Solver(Solver):
    def selectCandidateAssignments(self, config, candidateList):
        if(len(candidateList) == 0):
            return(None)

        # sort candidate assignments by cost in ascending order
        sortedCL = sorted(
            candidateList, key=lambda assign: assign.calculateCost(), reverse=False)

        # compute boundary cost as a function of the minimum and maximum cost and the alpha parameter
        alpha = config.alpha
        minCost = sortedCL[0].get_cost()
        maxCost = sortedCL[len(sortedCL)-1].calculateCost()
        boundaryCost = minCost + \
            (maxCost - minCost) * alpha

        # find elements that fall into the RCL (those fulfilling: cost < boundaryCost)
        maxIndex = 0
        for x in sortedCL:
            if(x.calculateCost() > boundaryCost):
                break
            maxIndex += 1

        # create RCL and pick an element randomly
        # pick first maxIndex elements starting from element 0
        rcl = sortedCL[0:maxIndex]
        if(len(rcl) == 0):
            return(None)
        # pick an element from rcl at random
        a_sel = random.choice(rcl)
        return(a_sel)

    def selectCandidateDrives(self, config, candidateList):
        if(len(candidateList) == 0):
            return(None)

        # sort candidate drives by cost in ascending order
        sortedCL = sorted(
            candidateList, key=lambda drives: drives.calculateCost(candidateList), reverse=False)

        # compute boundary highest cost as a function of the minimum and maximum cost and the alpha parameter
        alpha = config.alpha
        minCost = sortedCL[0].calculateCost(candidateList)
        maxCost = sortedCL[len(sortedCL)-1].calculateCost(candidateList)
        boundaryCost = minCost + \
            (maxCost - minCost) * alpha

        # find elements that fall into the RCL (those fulfilling: highestCost < boundaryCost)
        maxIndex = 0
        for x in sortedCL:
            if(x.calculateCost(candidateList) > boundaryCost):
                break
            maxIndex += 1

        # create RCL and pick an element randomly
        # pick first maxIndex elements starting from element 0
        rcl = sortedCL[0:maxIndex]
        if(len(rcl) == 0):
            return(None)
        # pick an element from rcl at random
        d_sel = random.choice(rcl)
        return(d_sel)

    def greedyRandomizedConstruction(self, config, problem):
        # get an empty solution for the problem
        solution = Solution.createEmptySolution(config, problem)

        # get services
        services = problem.getServices()
        sortedServices = services

        # get buses and sort them by capacity in descending order
        buses = problem.getBuses()
        sortedBuses = sorted(
            buses, key=lambda bus: bus.getCapacity(), reverse=True)

        # get drivers and sort them by maxMinutes in descending order
        drivers = problem.getDrivers()
        sortedDrivers = sorted(
            drivers, key=lambda driver: driver.getMaxMinutes(), reverse=True)

        elapsedEvalTime = 0
        evaluatedCandidates = 0

        # for each service taken in sorted order
        for service in sortedServices:
            #### BUSES ####

            candidateBuses = []

            candidateBuses, assignment_elapsedEvalTime, assignment_evaluatedCandidates = solution.findFeasibleBuses(
                service, sortedBuses, problem)
            elapsedEvalTime += assignment_elapsedEvalTime
            evaluatedCandidates += assignment_evaluatedCandidates

            # choose the cheapest assignment
            minBestAssignment = float('infinity')
            choosenAssignment = None
            for assignment in candidateBuses:
                auxCalculation = assignment.calculateCost()
                if(minBestAssignment > auxCalculation):
                    minBestAssignment = auxCalculation
                    choosenAssignment = assignment

            #### DRIVES ####

            candidateDrives = []

            candidateDrives, drives_elapsedEvalTime, drives_evaluatedCandidates = solution.findFeasibleDrivers(
                service, sortedDrivers, problem)
            elapsedEvalTime += drives_elapsedEvalTime
            evaluatedCandidates += drives_evaluatedCandidates

            # choose drives with minimum cost
            minBestDrives = float('infinity')
            choosenDrives = None

            for drives in candidateDrives:
                auxCalculation = drives.calculateCost(candidateDrives)
                if(minBestDrives > auxCalculation):
                    minBestDrives = auxCalculation
                    choosenDrives = drives

            if(choosenDrives is None or choosenAssignment is None):
                solution.makeInfeasible()
                break

            ### UP TO HERE, THE CONSTRUCTIVE PHASE IS EXACTLY LIKE THE GREEDY ONE ##

            # select a candidate drives
            candidateDrives = self.selectCandidateDrives(config, candidateDrives)
            if(candidateDrives is None):
                break

            # select a candidate bus
            candidateAssignment = self.selectCandidateAssignments(config, candidateBuses)
            if(candidateAssignment is None):
                break

            # Add the candidate bus and drives 
            solution.assignments.append(candidateAssignment)
            solution.drives.append(candidateDrives)

        return(solution, elapsedEvalTime, evaluatedCandidates)

    def solve(self, config, problem):
        bestSolution = Solution.createEmptySolution(config, problem)
        bestSolution.makeInfeasible()
        bestCost = float('infinity')
        self.startTimeMeasure()
        self.writeLogLine(bestCost, 0)

        total_elapsedEvalTime = 0
        total_evaluatedCandidates = 0

        localSearch = LocalSearch(config)

        iteration = 0
        
        while(time.time() - self.startTime < config.maxExecTime):
            iteration += 1

            # force first iteration as a Greedy execution (alpha == 0)
            originalAlpha = config.alpha
            if(iteration == 1):
                config.alpha = 0

            solution, it_elapsedEvalTime, it_evaluatedCandidates = self.greedyRandomizedConstruction(
                config, problem)
            total_elapsedEvalTime += it_elapsedEvalTime
            total_evaluatedCandidates += it_evaluatedCandidates

            # recover original alpha
            if(iteration == 1):
                config.alpha = originalAlpha

            if(not solution.isFeasible()):
                continue

            solution = localSearch.run(solution)

            solutionCost = solution.calculateCost()
            if(solutionCost < bestCost):
                bestSolution = solution
                bestCost = solutionCost
                self.writeLogLine(bestCost, iteration)

        self.writeLogLine(bestCost, iteration)

        avg_evalTimePerCandidate = 0.0
        if(total_evaluatedCandidates != 0):
            avg_evalTimePerCandidate = 1000.0 * \
                total_elapsedEvalTime / float(total_evaluatedCandidates)

        print('')
        print('GRASP Candidate Evaluation Performance:')
        print('  Num. Candidates Eval.', total_evaluatedCandidates)
        print('  Total Eval. Time     ', total_elapsedEvalTime, 's')
        print('  Avg. Time / Candidate', avg_evalTimePerCandidate, 'ms')

        localSearch.printPerformance()

        return(bestSolution)

    def printSolution(self, solution):
        drives, assignments = solution.drives, solution.assignments
        sorted_assignments = sorted(
            assignments, key=lambda assignment: assignment.getService().getId(), reverse=False)
        sorted_drivers = sorted(
            drives, key=lambda drive: drive.getService().getId(), reverse=False)
        for assignment in sorted_assignments:
            print(assignment)
        for drives in sorted_drivers:
            print(drives)