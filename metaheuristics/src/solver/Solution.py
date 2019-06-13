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
            total_cost += hired.get_cost()
        return total_cost

    def find_hired(self, provider):
        for element in self.hired:
            if element.get_provider().get_id() == provider.get_id():
                return element

    def remove_hired(self, provider):
        hire_provider = self.find_hired(provider)
        if(hire_provider != None):
            self.hired.remove(hire_provider)

    def find_feasible_hirings(self, sorted_providers, problem, needed_providers):
        startEvalTime = time.time()
        evaluatedCandidates = 0
        feasible_hires = []
        feasible = None
        valid = True
        cost_1 = problem.cost_1
        cost_2 = problem.cost_2
        cost_3 = problem.cost_3
        
        for provider in sorted_providers:
            if(self.is_in_solution(provider)):
                continue
            elif(needed_providers == 0):
                feasible_hires.append(Hired(provider, 0, cost_1, cost_2, cost_3))
                break
            for h1 in self.hired:
                if(problem.is_same_country(h1.get_provider(), provider)):
                    valid = False
                    break
            if(not valid):
                valid = True
                continue
            workers_to_hire = self.calculate_feasible_workers(provider, needed_providers)
            for i in workers_to_hire:
                feasible = Hired(provider, i, cost_1, cost_2, cost_3)
                feasible_hires.append(feasible)
                evaluatedCandidates += 1
        elapsedEvalTime = time.time() - startEvalTime
        return(feasible_hires, elapsedEvalTime, evaluatedCandidates)

    def calculate_feasible_workers(self, provider, objective_workers):
        valid_options = []
        available = provider.get_available_workers()

        if(objective_workers == 0):
            valid_options.append(0)
        if (objective_workers >= available / 2):
            valid_options.append(available / 2)
        if (objective_workers >= available):
            valid_options.append(available)
        if (objective_workers >= 2 * available):
            valid_options.append(2 * available)
        if (objective_workers > available):
            valid_options = valid_options + list(range(available + 1, available * 2))
        return valid_options

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
            hired, key=lambda h: h.provider.get_id(), reverse=False)
        for h in sorted_hired:
            aux += h.__str__() + "\n"

        aux += ("\nObjective value: %d \n" % (self.calculateCost()))
        return aux
