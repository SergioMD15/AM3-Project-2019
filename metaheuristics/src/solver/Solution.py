from model.Hired import Hired
import copy
import time
import sys
from solver.Problem import Problem
sys.path.append("..")

# Solution includes functions to manage the solution, to perform feasibility
# checks and to dump the solution into a string or file.


class Solution():
    @staticmethod
    def createEmptySolution(config, problem):
        solution = Solution(problem.inputData)
        return(solution)

    def __init__(self, inputData):
        # super(Solution, self).__init__(inputData)
        self.feasible = True
        self.hired = []

    def makeInfeasible(self):
        self.feasible = False

    def isFeasible(self):
        return self.feasible

    def calculateCost(self):
        hired_workers = self.hired
        total_cost = 0
        for hired in hired_workers:
            total_cost += hired.calculate_cost()
        return total_cost

    def find_hired(self, provider):
        for element in self.hired:
            if element.get_provider().get_id() == provider.get_id():
                return element

    def remove_hired(self, provider):
        hire_provider = self.find_hired(provider)
        if(hire_provider != None):
            self.hired.remove(hire_provider)

    def find_feasible_hirings(self, sorted_providers, problem):
        startEvalTime = time.time()
        evaluatedCandidates = 0
        feasible_hires = []
        feasible = None
        valid = True
        hired_amount = 0
        for provider in sorted_providers:
            print(len(feasible_hires))
            if(hired_amount == problem.workers):
                feasible = Hired(provider, 0)
            else:
                if(self.is_in_solution(provider)):
                    continue
                for h in self.hired:
                    if(problem.is_same_country(h.get_provider(), provider)):
                        valid = False
                        break
                if(not valid):
                    continue
                workers_to_hire = self.calculate_feasible_workers(
                    hired_amount, provider, problem.workers)

                feasible = Hired(provider, workers_to_hire)
                feasible_hires.append(feasible)

                evaluatedCandidates += 1
                hired_amount += workers_to_hire
        elapsedEvalTime = time.time() - startEvalTime
        return(feasible_hires, elapsedEvalTime, evaluatedCandidates)

    def calculate_feasible_workers(self, already_hired, provider, objective_workers):
        remaining_workers = objective_workers - already_hired
        available = provider.get_available_workers()

        if(remaining_workers < available / 2):
            return 0
        elif (remaining_workers == available / 2 or (remaining_workers > available / 2 and remaining_workers < available)):
            return available / 2
        elif (remaining_workers == available):
            return available
        elif (remaining_workers >= 2 * available):
            return 2 * available
        elif (remaining_workers < 2 * available and remaining_workers > available):
            return remaining_workers

    def is_in_solution(self, provider):
        for h in self.hired:
            if(provider == h.get_provider()):
                return True
        return False

    def usedProviders(self):
        providers = []
        for element in self.hired:
            providers.append(element.get_provider())
        return len(set(providers))

    def get_hiring_assigned(self, provider):
        for hiring in self.hired:
            if(hiring.get_provider().get_id() == provider.get_id()):
                return hiring
        return None

    def saveToFile(self, filePath):
        f = open(filePath, 'w')
        print(filePath)
        f.write(self.__str__())
        f.close()

    def __str__(self):
        hired = self.hired
        aux = "Hirings: \n\n"
        sorted_hired = sorted(
            hired, key=lambda h: h.getService().get_id(), reverse=False)
        for h in sorted_hired:
            aux += h + "\n"

        aux += ("\n\nObjective value: %.2f" % (self.calculateCost()))
        return aux
