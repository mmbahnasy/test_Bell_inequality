#!/usr/bin/env python3

import numpy as np
# %matplotlib inline
import matplotlib.pyplot as pyplot
from utils import withinRotatingRange, writeToCsvFile

PI=180 # np.pi
ParticleNum = 1000
RepeatitionNum = 100

"""# AsameB + BsameC + AsameC >= 1"""

def getStats(p_angle):
  "Returns AsameB, BsameC, AsameC"
  stats = np.array([0,0,0])
  if withinRotatingRange(p_angle, *theta_a_range): # A
    if withinRotatingRange(p_angle, *theta_b_range): # B
      stats[0]+=1
    if withinRotatingRange(p_angle, *theta_c_range): # C
      stats[2]+=1
  if withinRotatingRange(p_angle, *theta_b_range): # B
    if withinRotatingRange(p_angle, *theta_c_range): # C
      stats[1]+=1
  return stats

# define statistic variables in a numpy array
stats = np.array([0, 0, 0]) # Psame(A,B), Psame(B,C), Psame(A,C), 

particles = np.random.uniform(0,2*PI+1,ParticleNum)
theta_a=0
results_all = []
for i in range(RepeatitionNum):
  result=[]
  for theta_b in range(1,int(0.5*PI)):
    theta_c=2*theta_b
    theta_a_range = (theta_a - 0.5*PI , theta_a + 0.5*PI)
    theta_b_range = (theta_b - 0.5*PI , theta_b + 0.5*PI)
    theta_c_range = (theta_c - 0.5*PI , theta_c + 0.5*PI)
    # start monitoring the particles
    for i in range(ParticleNum):
      s = getStats(particles[i])
      stats = stats + s
    stats = stats/ParticleNum
    # print(stats, np.sum(stats))
    result.append(np.sum(stats))
  results_all.append(result)
  # pyplot.plot(result)

results_all = np.array(results_all)
results_mean = np.mean(results_all, axis=0)
y_errormin = np.round(results_mean - np.min(results_all, axis=0), 5)
y_errormax = np.round(results_mean - np.max(results_all, axis=0), 5)
y_error =[y_errormin, y_errormax] 

pyplot.errorbar(range(1, int(0.5*PI)), results_mean, yerr = y_error, fmt ='r') # must be >= 0s
# pyplot.plot(results_mean)
pyplot.grid()
pyplot.title("AsameB + BsameC + AsameC >= 1")
pyplot.savefig("AsameB_BsameC_AsameC")

# write results into CSV file
writeToCsvFile('AsameB_BsameC_AsameC.csv', range(1, int(0.5*PI)), results_mean, y_errormin, y_errormax)
