#!/usr/bin/env python3

import numpy as np
# %matplotlib inline
import matplotlib.pyplot as plt
from utils import withinRotatingRange, writeToCsvFile

PI = 180  # np.pi
ParticleNum = 1000
RepeatitionNum = 100
Theta_A = 0
Theta_B = 60
Theta_C = 120


"""# A B + B C + A C >= 1"""


def getOneStateMeasurements(leftSideAngle, rightSideAngle):
    "Returns A B ,  B C, A C"
    isA_L = withinRotatingRange(leftSideAngle, Theta_A-PI/2+2*PI, Theta_A+PI/2)  # A
    isA_R = withinRotatingRange(rightSideAngle, Theta_A-PI/2+2*PI, Theta_A+PI/2)  # A
    isB_L = withinRotatingRange(leftSideAngle, Theta_B-PI/2+2*PI, Theta_B+PI/2)  # B
    isB_R = withinRotatingRange(rightSideAngle, Theta_B-PI/2+2*PI, Theta_B+PI/2)  # B
    isC_L = withinRotatingRange(leftSideAngle, Theta_C-PI/2, Theta_C+PI/2)  # C
    isC_R = withinRotatingRange(rightSideAngle, Theta_C-PI/2, Theta_C+PI/2)  # C
    # oneState = np.array([(isA_L and isB_R) or (not isA_L and not isB_R), (isB_L and isC_R) or (not isB_L and not isC_R), (isA_L and isC_R) or (not isA_L and not isC_R)])
    oneState = np.array([isA_L and not isB_R, isB_L and not isC_R, isA_R and not isC_L])
    # print(leftSideAngle, rightSideAngle, oneState)
    return oneState

# define statistic variables in a numpy array

def runTest(differentDistance):
    """
    Generate number of particls and perform the quantum entanglement test
    Return the result as a list with three items: [N(a !b), N(b !c), N(a !c)]
    """
    particles = np.random.uniform(0, 2*PI, ParticleNum)
    distanceAngleShift = np.random.normal(0, 2*PI, ParticleNum)
    stats = np.array([0, 0, 0])  # Psame(A,B), Psame(B,C), Psame(A,C),
    for indx in range(ParticleNum):
        oneStat = getOneStateMeasurements(
            particles[indx], (particles[indx] + distanceAngleShift[indx] if differentDistance else 0) % (2*PI))
        stats = stats + oneStat
    stats = stats / ParticleNum

    return stats

# results_sum = np.round(np.sum(results_mean), 2)
# print(f"Results sum: {results_sum}")
# y_error = [np.std(results, axis=0)]



# # write results into CSV file
# # writeToCsvFile("A B _ B C_A C.csv", range(1, int(0.5*PI)), results_mean, y_errormin, y_errormax)


if __name__ == "__main__":
    distanceStatus = [False, True]
    resultsAll =[]
    for differentDistance in distanceStatus:
        resultsPerRepetition =[]
        for j in range(RepeatitionNum):
            results = runTest(differentDistance = differentDistance) # dim: [N(a !b), N(b !c), N(a !c)]
            resultsPerRepetition.append(results)
        resultsAll.append(resultsPerRepetition)
    resultsAll = np.array(resultsAll) # Dimension: 2 x RepetitionNum x 3
    cases_results_mean = np.mean(resultsAll, axis=1) # Dimension: 2 x 3
    for i, differentDistance in enumerate(distanceStatus):
        isBellInequalityValid = cases_results_mean[i, 0] + cases_results_mean[i, 1] >= cases_results_mean[i, 2] # N(a !b) + N(b !c) >= N(a !c)
        print("Different" if differentDistance else "Identical", "distance results (Sum/Count):",
            cases_results_mean[i, 0] + cases_results_mean[i, 1], ">=", cases_results_mean[i, 2],
            ", Bell's inequality (N(a !b) + N(b !c) >= N(a !c)) is", "" if isBellInequalityValid else "not", "valid.")
    cases_results_min = np.min(resultsAll, axis=1)
    cases_results_max = np.max(resultsAll, axis=1)
    # Build the plot
    cases = ["Identical (N(a !b) + N(b !c))", "Identical (N(a !c))", "Different (N(a !b) + N(b !c))", "Different (N(a !c))"]
    x_pos = [0, 1, 3, 4]
    cases_results = [cases_results_mean[0,0]+cases_results_mean[0,1], cases_results_mean[0,2],
                    cases_results_mean[1,0]+cases_results_mean[1,1], cases_results_mean[1,2]]

    y_errormin = [cases_results_mean[0,0]+cases_results_mean[0,1] - (cases_results_min[0,0]+cases_results_min[0,1]), cases_results_mean[0,1] - cases_results_min[0,0],
                    cases_results_mean[1,0]+cases_results_mean[1,1]- (cases_results_min[1,0]+cases_results_min[1,1]), cases_results_mean[1,1] - cases_results_min[0,0]]
    y_errormax = [(cases_results_max[0,0]+cases_results_max[0,1]) - (cases_results_mean[0,0]+cases_results_mean[0,1]),  cases_results_max[0,0] - cases_results_mean[0,1],
                  (cases_results_max[1,0]+cases_results_max[1,1]) - (cases_results_mean[1,0]+cases_results_mean[1,1]),  cases_results_max[1,0] - cases_results_mean[1,1]]
    fig, ax = plt.subplots()
    ax.bar(x_pos, cases_results, align="center", alpha=0.5, ecolor="black", capsize=10)
    # ax.bar(x_pos, cases_results, yerr = [y_errormin, y_errormax], align="center", alpha=0.5, ecolor="black", capsize=10)
    ax.set_ylabel("Correlation Probability")
    ax.set_xticks(x_pos)
    ax.set_xticklabels(cases)
    ax.set_title("Correlation Probability")
    ax.yaxis.grid(True)

    # Save the figure and show
    plt.tight_layout()
    plt.savefig("CorrelationProbability.png")
    # plt.show()