import argparse
import sys

from parser.DATParser import DATParser
from parser.ValidateConfig import ValidateConfig
from heuristics.Greedy_Solver import Greedy_Solver
# from heuristics.GRASP_Solver import GRASP_Solver
from solver.Problem import Problem
from solver.Solution import Solution


def run():
    try:
        argp = argparse.ArgumentParser(
            description='AMMM Course Project Heuristics')
        argp.add_argument('configFile', help='configuration file path')
        args = argp.parse_args()

        print('AMMM Course Project Heuristics')
        print('-------------------')

        print('Reading Config file %s...' % args.configFile)
        config = DATParser.parse(args.configFile)
        ValidateConfig.validate(config)

        print('Reading Input Data file %s...' % config.inputDataFile)
        inputData = DATParser.parse(config.inputDataFile)

        print('Creating Problem...')
        problem = Problem(inputData)

        if(problem.check_instance()):
            print('Solving Problem...')
            solver = None
            solution = None
            if(config.solver == 'Greedy'):
                solver = Greedy_Solver()
                solution = solver.solve(config, problem)
            # elif(config.solver == 'GRASP'):
            #     solver = GRASP_Solver()
            #     solution = solver.solve(config, problem)
            solution.saveToFile(config.solutionFile)
        else:
            print('Instance is infeasible.')
            solution = Solution.createEmptySolution(config, problem)
            solution.makeInfeasible()
            solution.saveToFile(config.solutionFile)

        return(0)
    except Exception as e:
        print
        print('Exception:', e)
        print
        return(1)


if __name__ == '__main__':
    sys.exit(run())
