import numpy as np
import CaseStudy1Data_cpart
import pandas as pd
import pyomo.environ as pyo
from pyomo.opt import SolverFactory
import sys
sys.stdout = open('C:/Users/Bartu/Desktop/Results_Cpart.txt', 'w')
#Construct the model
mdl = pyo.ConcreteModel('CaseStudy1')
#Define sets
mdl.I = pyo.Set(initialize=CaseStudy1Data_cpart.entrynode, doc='entrynode' )
mdl.J = pyo.Set(initialize=CaseStudy1Data_cpart.exitnode, doc='exitnode')

#Define parameters
mdl.c = pyo.Param(mdl.I, mdl.J, initialize=CaseStudy1Data_cpart.CostMatrix, doc='Cost of each arc' )
mdl.u=  pyo.Param(mdl.J, initialize=CaseStudy1Data_cpart.Upper, doc='Upper Bound for each process')

#Define variables
mdl.vX = pyo.Var (mdl.I, mdl.J, doc='amount transported from node i to node j', within=pyo.NonNegativeReals)

#Define constraints

def Upper_Bound (mdl,j):
    if j not in (1,24,25,26,27,44,45,46) :
        return sum(mdl.vX[j,i] for i in mdl.J) <= mdl.u[j]
    else:
        return pyo.Constraint.Skip
mdl.Upper_Bound=pyo.Constraint(mdl.J,rule=Upper_Bound,doc='Upper Bound for each process constraint')

def Supply (mdl,j):
    if j  in (1,27) :
        return sum(mdl.vX[j,i] for i in mdl.J) <= mdl.u[j]
    else:
        return pyo.Constraint.Skip
mdl.Supply=pyo.Constraint(mdl.J,rule=Supply,doc='Upper Bound for supply constraint ')
def Demand (mdl,j):
    if j  in (24,25,26,44,45,46) :
        return sum(mdl.vX[i,j] for i in mdl.I) == mdl.u[j]
    else:
        return pyo.Constraint.Skip
mdl.Demand=pyo.Constraint(mdl.J,rule=Demand,doc='Demand should met')

def Zero_Outflow(mdl, j):
    if j not in (1,27,24,25,26,44,45,46):
        return sum(mdl.vX[i,j] for i in mdl.I) - sum(mdl.vX[j,i] for i in mdl.J) == 0
    else:
        return pyo.Constraint.Skip

mdl.Zero_Outflow = pyo.Constraint(mdl.J, rule=Zero_Outflow, doc='Net Flow = 0 for non-source and non-sink node')


#Define objective
def oTotal_Cost(mdl):
    return sum(mdl.c[i,j]*mdl.vX[i,j] for i in mdl.I for j in mdl.J)
mdl.oTotal_Cost = pyo.Objective(rule=oTotal_Cost, sense=pyo.minimize, doc='Total Transportation Cost')

Solver = SolverFactory('glpk')
SolverResults = Solver.solve(mdl, tee=True)
SolverResults.write()
mdl.pprint()
mdl.vX.display()
mdl.oTotal_Cost.display()