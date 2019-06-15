from heuristics.LocalSearch import LocalSearch
from solver.Solution import Solution
from solver.Solver import Solver
from model.Hired import Hired
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
            providers, key=lambda p: p.get_id(), reverse=False)

        elapsedEvalTime = 0
        evaluatedCandidates = 0

        remaining_workers = problem.workers
        for i in range(len(sorted_providers)):

            candidate_hiring = []

            candidate_hiring, hiring_elapsedEvalTime, hiring_evaluatedCandidates = solution.find_feasible_hirings(
                sorted_providers, problem, remaining_workers)
                
            elapsedEvalTime += hiring_elapsedEvalTime
            evaluatedCandidates += hiring_evaluatedCandidates

            # choose the cheapest hiring
            best_hiring = float('infinity')
            choosen_hiring = None
            for candidate in candidate_hiring:
                difference = remaining_workers - candidate.workers
                if(difference >= 0 and best_hiring > difference):
                    best_hiring = difference
                    choosen_hiring = candidate

            if(choosen_hiring is None):
                if(remaining_workers == 0):
                    solution.add_hired(Hired(sorted_providers[i], 0, problem.cost_1, problem.cost_2, problem.cost_3))
                else:
                    solution.makeInfeasible()
                    break

            solution.hired.append(choosen_hiring)
            remaining_workers -= choosen_hiring.workers

        missing_providers = [i.provider for i in candidate_hiring]
        not_added = list(set(sorted_providers) ^ set(missing_providers))

        for provider in not_added:
            solution.add_hired(Hired(provider, 0, problem.cost_1, problem.cost_2, problem.cost_3))

        return (solution, elapsedEvalTime, evaluatedCandidates)


    ## This function returns the normalized value of the candidate hiring.
    ## First of all, to get a feasible solution we need the exact number of
    ## workers to be hired, then we want to minimize the cost, and finally
    ## it would be interesting looking for candidates with a low number of
    ## incompatibilities (same country).

    ## The idea is to return a cost according to three features:
    ## - The distance to the objective number of workers (with a 70% of importance)
    ## - The cost of the hirings (with a 25% of importance)
    ## - The number of incompatibilities of the provider (with a 5% of importance)
    def calculate_normalized_cost(self, candidates, needed_workers):

        cost = [i.get_cost() for i in candidates]
        min_cost = min(cost)
        max_cost = max(cost)
        normalized_cost = [float(i) - min_cost/(max_cost - min_cost) for i in cost]

        workers = [needed_workers - i.workers if(i.workers <= needed_workers) else 0 for i in candidates]
        min_workers = min(workers)
        max_workers = max(workers)
        normalized_workers = [float(i) - min_workers/(max_workers - min_workers) for i in workers]

        result = []

        for i in range(len(candidates)):
            result.append((i, normalized_workers[i] * 0.7 + normalized_cost[i] * 0.25))

        return result


    
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
        hirings = solution.hired
        sorted_hirings = sorted(
            hirings, key=lambda h: h.get_provider().get_id(), reverse=False)

        for h in sorted_hirings:
            print("Provider %d hires %s workers" % (
                h.get_provider().get_id()+1, h.get_workers()))
