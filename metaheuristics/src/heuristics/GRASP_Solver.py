
import random
import time
import sys
# from heuristics.LocalSearch import LocalSearch
sys.path.append("..")
from solver.Solver import Solver
from solver.Solution import Solution

# Inherits from a parent abstract solver.


class GRASP_Solver(Solver):
    def select_candidate_hiring(self, config, candidateList, remaining_workers):
        if(len(candidateList) == 0):
            return(None)

        # sort candidate hirings by cost in ascending order
        sortedCL = sorted(
            candidateList, key=lambda h: h.workers, reverse=False)

        # compute boundary highest cost as a function of the minimum and maximum cost and the alpha parameter
        alpha = config.alpha
        minCost = remaining_workers - sortedCL[0].workers
        maxCost = remaining_workers - sortedCL[-1].workers
        boundaryCost = minCost + \
            (maxCost - minCost) * alpha

        # create RCL and pick an element randomly
        # pick first maxIndex elements starting from element 0
        rcl = [i for i in candidateList if (remaining_workers - i.workers) < boundaryCost]
        if(len(rcl) == 0):
            return(None)
        # pick an element from rcl at random
        d_sel = random.choice(rcl)
        return(d_sel)

    def greedyRandomizedConstruction(self, config, problem):
        # get an empty solution for the problem
        solution = Solution.createEmptySolution(config, problem)

        # get providers and sort them by available workers
        providers = problem.get_providers()
        sorted_hirings = sorted(
            providers, key=lambda p: p.get_id(), reverse=True)

        elapsedEvalTime = 0
        evaluatedCandidates = 0
        remaining_workers = problem.workers

        # for each provider taken in sorted order
        for p in providers:

            candidate_hirings = []

            candidate_hirings, hirings_elapsedEvalTime, hirings_evaluatedCandidates = solution.find_feasible_hirings(
                sorted_hirings, problem, remaining_workers)
            elapsedEvalTime += hirings_elapsedEvalTime
            evaluatedCandidates += hirings_evaluatedCandidates

            # choose the cheapest hiring
            min_best_hiring = float('infinity')
            choosen_hiring = None
            for h in candidate_hirings:
                difference = remaining_workers - h.workers
                if(difference >= 0 and min_best_hiring > difference):
                    min_best_hiring = difference
                    choosen_hiring = h

            if(choosen_hiring is None):
                solution.makeInfeasible()
                break

            ### UP TO HERE, THE CONSTRUCTIVE PHASE IS EXACTLY LIKE THE GREEDY ONE ##

            # select a candidate hiring
            candidate = self.select_candidate_hiring(config, candidate_hirings, remaining_workers)
            if(candidate is None):
                break

            # Add the candidate hiring 
            solution.hired.append(candidate)
            remaining_workers -= candidate.workers

        return(solution, elapsedEvalTime, evaluatedCandidates, remaining_workers)

    def solve(self, config, problem):
        bestSolution = Solution.createEmptySolution(config, problem)
        bestSolution.makeInfeasible()
        bestCost = float('infinity')
        self.startTimeMeasure()
        self.writeLogLine(bestCost, 0)

        total_elapsedEvalTime = 0
        total_evaluatedCandidates = 0
        remaining_workers = problem.workers

        # localSearch = LocalSearch(config)

        iteration = 0
        
        while(time.time() - self.startTime < config.maxExecTime or remaining_workers == 0):
            iteration += 1

            # force first iteration as a Greedy execution (alpha == 0)
            originalAlpha = config.alpha
            if(iteration == 1):
                config.alpha = 0

            solution, it_elapsedEvalTime, it_evaluatedCandidates, workers = self.greedyRandomizedConstruction(
                config, problem)
            total_elapsedEvalTime += it_elapsedEvalTime
            total_evaluatedCandidates += it_evaluatedCandidates

            # recover original alpha
            if(iteration == 1):
                config.alpha = originalAlpha

            if(not solution.isFeasible()):
                continue

            # solution = localSearch.run(solution)

            solutionCost = solution.calculateCost()
            if(problem.workers - workers <= remaining_workers and solutionCost < bestCost):
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

        # localSearch.printPerformance()

        return(bestSolution)

    def printSolution(self, solution):
        hirings = solution.hired
        sorted_hiring = sorted(
            hirings, key=lambda h: h.get_id(), reverse=False)
        for h in sorted_hiring:
            print(h)