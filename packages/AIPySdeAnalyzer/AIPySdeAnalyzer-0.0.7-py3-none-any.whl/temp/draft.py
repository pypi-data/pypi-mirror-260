from aipysAnalyser.simulation.runSimulation import runSimulation

if __name__ == '__main__':
    runSimulation(targetNum = 5, geneNum = 100, effectSgRNA = 4,tpRatio = 40, n = 10, p = 0.1,low = 1, high = 5,size = 1_000,FalseLimits = (0.01,0.5),ObservationNum = (10,3))
   