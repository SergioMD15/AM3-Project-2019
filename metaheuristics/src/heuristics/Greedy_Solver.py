# from heuristics.LocalSearch import LocalSearch
from solver.Solution import Solution
from solver.Solver import Solver
import sys
sys.path.append("..")

# Inherits from a parent abstract solver.


class Greedy_Solver(Solver):

    def greedyConstruction(self, config, problem):
        # get an empty solution for the problem
        solution = Solution.createEmptySolution(config, problem)
        print(solution)

        # get providers
        providers = problem.get_providers()
        sorted_providers = sorted(
            providers, key=lambda p: p.get_available_workers(), reverse=True)

        elapsedEvalTime = 0
        evaluatedCandidates = 0


        # for each service taken in sorted order
        for i in range(len(sorted_providers)):

            candidate_providers = []

            candidate_providers, hiring_elapsedEvalTime, hiring_evaluatedCandidates = solution.find_feasible_hirings(
                sorted_providers, problem)
            elapsedEvalTime += hiring_elapsedEvalTime
            evaluatedCandidates += hiring_evaluatedCandidates

            # choose the cheapest hiring
            min_best_hiring = float('infinity')
            choosen_hiring = None
            for h in candidate_providers:
                hiring_cost = h.calculate_cost(problem.cost_1, problem.cost_2, problem.cost_3)
                if(min_best_hiring > hiring_cost):
                    min_best_hiring = hiring_cost
                    choosen_hiring = h

            if(choosen_hiring is None):
                solution.makeInfeasible()
                break

            solution.hired.append(choosen_hiring)

        return (solution, elapsedEvalTime, evaluatedCandidates)

    def solve(self, config, problem):
        self.startTimeMeasure()
        self.writeLogLine(float('infinity'), 0)
        solution, elapsedEvalTime, evaluatedCandidates = self.greedyConstruction(
            config, problem)

        solutionValue = solution.calculateCost()

        self.writeLogLine(solutionValue, 1)

        print('Greedy solution: ', solutionValue)

        # localSearch = LocalSearch(config)
        # solution = localSearch.run(solution)

        # solutionValue = solution.calculateCost()

        # print('Local search solution: ', solutionValue)

        # self.writeLogLine(solutionValue, 1)

        # avg_evalTimePerCandidate = 0.0
        # if (evaluatedCandidates != 0):
        #     avg_evalTimePerCandidate = 1000.0 * \
        #         elapsedEvalTime / float(evaluatedCandidates)

        print('')
        print('Greedy Candidate Evaluation Performance:')
        print('  Num. Candidates Eval.', evaluatedCandidates)
        print('  Total Eval. Time     ', elapsedEvalTime, 's')
        print('  Avg. Time / Candidate', avg_evalTimePerCandidate, 'ms')

        # localSearch.printPerformance()

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
