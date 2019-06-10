from heuristics.LocalSearch import LocalSearch
from solver.Solution import Solution
from solver.Solver import Solver
import sys
sys.path.append("..")

# Inherits from a parent abstract solver.


class Greedy_Solver(Solver):

    def greedyConstruction(self, config, problem):
        # get an empty solution for the problem
        solution = Solution.createEmptySolution(config, problem)

        # get providers
        providers = problem.get_providers()
        sorted_providers = sorted(
            providers, key=lambda p: p.get_available_workers(), reverse=True)

        elapsedEvalTime = 0
        evaluatedCandidates = 0

        # for each service taken in sorted order
        for provider in sorted_providers:
            #### BUSES ####

            candidateBuses = []

            candidateBuses, assignment_elapsedEvalTime, assignment_evaluatedCandidates = solution.find_feasible_hirings(
                provider, sorted_providers, problem)
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

            # choose drives with the minimum cost
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

            # Assign the current service to the corresponding assignment (Bus with Service),
            # and to the corresponding drives (Driver with Service)
            solution.assignments.append(choosenAssignment)
            solution.drives.append(choosenDrives)

        return (solution, elapsedEvalTime, evaluatedCandidates)

    def solve(self, config, problem):
        self.startTimeMeasure()
        self.writeLogLine(float('infinity'), 0)
        solution, elapsedEvalTime, evaluatedCandidates = self.greedyConstruction(
            config, problem)

        solutionValue = solution.calculateCost()

        self.writeLogLine(solutionValue, 1)

        print('Greedy solution: ', solutionValue)

        localSearch = LocalSearch(config)
        solution = localSearch.run(solution)

        solutionValue = solution.calculateCost()

        print('Local search solution: ', solutionValue)

        self.writeLogLine(solutionValue, 1)

        avg_evalTimePerCandidate = 0.0
        if (evaluatedCandidates != 0):
            avg_evalTimePerCandidate = 1000.0 * \
                elapsedEvalTime / float(evaluatedCandidates)

        print('')
        print('Greedy Candidate Evaluation Performance:')
        print('  Num. Candidates Eval.', evaluatedCandidates)
        print('  Total Eval. Time     ', elapsedEvalTime, 's')
        print('  Avg. Time / Candidate', avg_evalTimePerCandidate, 'ms')

        localSearch.printPerformance()

        return(solution)

    def printSolution(self, solution):
        drives, assignments = solution.drives, solution.assignments
        sorted_assignments = sorted(
            assignments, key=lambda assignment: assignment.getService().getId(), reverse=False)
        sorted_drivers = sorted(
            drives, key=lambda drive: drive.getService().getId(), reverse=False)

        print('Se vienen los assignments')

        for assignment in sorted_assignments:
            print("Hay un uno en: %s, %s" % (
                assignment.getService().getId()+1, assignment.getBus().getId()+1))

        print("Se vienen los drivers")

        for drive in sorted_drivers:
            print("Hay un uno en: %s, %s" %
                  (drive.getService().getId()+1, drive.getDriver().getId()+1))
