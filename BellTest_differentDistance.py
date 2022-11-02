#!/usr/bin/env python3

import numpy as np
# %matplotlib inline
import matplotlib.pyplot as plt
from utils import withinRotatingRange, writeToCsvFile

PI=180 # np.pi
ParticleNum = 1000
RepeatitionNum = 100
Theta_A = 0
Theta_B = 60
Theta_C = 120

"""# A B !C + !A B C + A !B C >= 1"""

def getOneStateMeasurements(leftSideAngle, rightSideAngle):
  "Returns A B !C, !A B C, A !B C"
  stats = np.array([0,0,0])
  if withinRotatingRange(leftSideAngle, Theta_A-PI/2, Theta_A+PI/2): # A
    if withinRotatingRange(rightSideAngle, Theta_B-PI/2, Theta_B+PI/2): # B
      stats[0]+=1
    if withinRotatingRange(rightSideAngle, Theta_C-PI/2, Theta_C+PI/2): # C
      stats[2]+=1
  if withinRotatingRange(leftSideAngle, Theta_B-PI/2, Theta_B+PI/2): # B
    if withinRotatingRange(rightSideAngle, Theta_C-PI/2, Theta_C+PI/2): # C
      stats[1]+=1
  return stats

# define statistic variables in a numpy array

theta_a=0
results=[]
for i in range(RepeatitionNum):
  particles = np.random.uniform(0,2*PI+1,ParticleNum)
  distanceAngleShift = np.random.normal(0, 45, ParticleNum)
  stats = np.array([0, 0, 0]) # Psame(A,B), Psame(B,C), Psame(A,C), 
  for particleAngle in range(ParticleNum):
    oneStat = getOneStateMeasurements(particles[i], (particles[i] + PI + distanceAngleShift[i]) % (2*PI))
    stats = stats + oneStat
  stats = stats/ParticleNum
  # print(stats, np.sum(stats))
  results.append(stats)
  # pyplot.plot(result)

results = np.array(results)
results_mean = np.mean(results, axis=0)
print("Results (A B !C, !A B C, A !B C):", results_mean)
results_sum = np.sum(results_mean)
print(f"Results sum: {results_sum}") #, " not " if results_sum>= 1 else "", " violate Bell's inequality.")
y_error =[np.std(results, axis=0)] 

# Build the plot
cases = ["A B !C", "!A B C", "A !B C"]
x_pos = np.arange(len(cases))
fig, ax = plt.subplots()
ax.bar(x_pos, results_mean, yerr=y_error, align='center', alpha=0.5, ecolor='black', capsize=10)
ax.set_ylabel('A B !C + !A B C + A !B C >= 1')
ax.set_xticks(x_pos)
ax.set_xticklabels(cases)
ax.set_title('A B !C + !A B C + A !B C')
ax.yaxis.grid(True)

# Save the figure and show
plt.tight_layout()
plt.savefig('bar_plot_with_error_bars.png')
plt.show()

# write results into CSV file
# writeToCsvFile('A B !C_!A B C_A !B C.csv', range(1, int(0.5*PI)), results_mean, y_errormin, y_errormax)
