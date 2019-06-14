
import copy
import time
from model.Hired import Hired
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

    def find_feasible_hirings_cheap(self, hiring):
        valid_options = []
        cost_1 = hiring.cost_1
        cost_2 = hiring.cost_2
        cost_3 = hiring.cost_3
        provider = hiring.get_provider()
        available = provider.get_available_workers()
        workers = hiring.workers

        if (workers == 0):
            valid_options.append(Hired(provider,0, cost_1, cost_2, cost_3))
        if (workers <= available / 2):
            valid_options.append(Hired(provider, available / 2, cost_1, cost_2, cost_3))
        if (workers <= available):
            valid_options.append(Hired(provider, available, cost_1, cost_2, cost_3))
        if (workers >= available):
            valid_options = valid_options + [Hired(provider, i, cost_1, cost_2, cost_3) for i in list(range(workers, available * 2))]
        return valid_options

    def find_feasible_hirings_expensive(self, hiring):
        valid_options = []
        cost_1 = hiring.cost_1
        cost_2 = hiring.cost_2
        cost_3 = hiring.cost_3
        provider = hiring.get_provider()
        available = provider.get_available_workers()
        workers = hiring.workers

        if(workers == 0):
            valid_options.append(Hired(provider, 0, cost_1, cost_2, cost_3))
        if (workers >= available / 2):
            valid_options.append(Hired(provider, available / 2, cost_1, cost_2, cost_3))
        if (workers >= available):
            valid_options = valid_options + [Hired(provider, i, cost_1, cost_2, cost_3) for i in list(range(available, workers))]
        return valid_options

    def is_incompatible(self, hiring, hirings_list):
        already_hiring = [i[0].provider for i in hirings_list if (i[0].workers > 0 and hiring.provider != i[0].provider)]
        if(len(already_hiring) == 0):
            return False
        for tp in already_hiring:
            if(tp.get_country == hiring.provider.get_country()):
                return True
        return False

    def exploreNeighborhood(self, solution):
        hirings = solution.hired
        curCost = solution.calculateCost()
        bestNeighbor = copy.deepcopy(solution)

        # We find the most expensive element in solution
        sorted_hirings = sorted(hirings, key=lambda h: h.cost, reverse=True)
        expensive_h = sorted_hirings[0]

        cheapest = [(i,i.get_cost_hiring()) for i in hirings if i.workers < i.provider.get_available_workers() * 2]
        # We look for the potentially cheapest element in solution not having incompatibilities
        sorted_cheapest = sorted(cheapest, key=lambda h: h[1], reverse=False)
        cheapest_h = None
        for hiring in sorted_cheapest:
            # print(hiring[0].provider)
            if(not self.is_incompatible(hiring[0], sorted_cheapest)):
                cheapest_h = hiring[0]
                break
        if(cheapest_h == None):
            return bestNeighbor

        feasible_cheapest = self.find_feasible_hirings_cheap(cheapest_h)
        feasible_expensive = self.find_feasible_hirings_expensive(expensive_h)
        remaining_workers = solution.get_remaining_workers()

        if(self.nhStrategy == 'Reassignment'):
            sol = False
            for i in feasible_cheapest:
                for j in feasible_expensive:
                    difference = -cheapest_h.workers + i.workers - expensive_h.workers + j.workers - remaining_workers
                    if(remaining_workers >= difference and difference >= 0):
                        auxSolution = copy.deepcopy(bestNeighbor)
                        
                        if(i.cost + j.cost <= cheapest_h.cost + expensive_h.cost):
                            auxSolution.remove_hired(cheapest_h.provider)
                            auxSolution.add_hired(i)
                            auxSolution.remove_hired(expensive_h.provider)
                            auxSolution.add_hired(j)
                        if(auxSolution.calculateCost() <= curCost):
                            bestNeighbor = auxSolution
                            curCost = auxSolution.calculateCost()
                            sol = True
                            break
                if(sol):
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
