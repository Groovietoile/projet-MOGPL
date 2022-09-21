#!/usr/bin/python

# Copyright 2013, Gurobi Optimization, Inc.


from gurobipy import *
import csv
with open('villes.csv', newline='') as csvfile:
    ville = list(csv.reader(csvfile , delimiter = '\t'))
    v = []
    nom_v = []
    d = []
    ville.pop(0)
    for elem in ville:
        l = elem[0].split(";")
        v.append(int(l[0]))
        nom_v.append(str(l[1]))
        d.append(list(map(int,[0 if x == '' else x for x in l[2:]])))
#print(d)

n=15 
k=3
alpha = 0.1
nbcont=n+k
nbvar=n*k
sect = [0,1,2]

# Range of plants and warehouses
#lignes = range(nbcont)
colonnes = range(nbvar)

# Matrice des contraintes
a1 = []
for j in sect:
    l = []
    for i in range(n):
        for s in sect:
            if s == j :
                l.append(v[i])
            else:
                l.append(0)
    a1.append(l)
			
		
a2 = []
for m in range (n):
	a2.append(m*k*[0]+k*[1]+(n-m-1)*k*[0])
	

# Second membre
b1 = k*[((1+alpha)/k) * sum(v)] 
b2 = n*[1]

# Coefficients de la fonction objectif
c =[]
for i in range(n):
	for j in sect:
		c.append(d[max(i,j)][min(i,j)] * v[i] )
		

m = Model("mogplex")     
        
# declaration variables de decision
x = []
for i in range (n):
    for j in sect:
            x.append(m.addVar(vtype=GRB.BINARY, lb=0, name="x%d,%d" % (i+1,j+1)))

# maj du modele pour integrer les nouvelles variables
m.update()

obj = LinExpr();
obj =0
for j in colonnes:
    obj += c[j] * x[j]
        
# definition de l'objectif
m.setObjective(obj,GRB.MINIMIZE)

# Definition des contraintes
for i in range (k):
    m.addConstr(quicksum(a1[i][j]*x[j] for j in colonnes) <= b1[i], "Contrainte%d" % i)

for i in range (n):
    m.addConstr(quicksum(a2[i][j]*x[j] for j in colonnes) == b2[i], "Contrainte%d" % (i+k))


# Resolution
m.optimize()


print("")                
print('Solution optimale:')
lessecteurs = "Secteurs :"
for i in sect:
    lessecteurs += " "+nom_v[i].rstrip()
print(lessecteurs)

# Résultat
for var in m.getVars():
    if var.x > 0:
        print('%s %g' % (var.varName, var.x))         
print("")
print('Valeur de la fonction objectif :', m.objVal/sum(v))
print("")

# Pour lire le résultat
for i in range(n):
    print(i+1, nom_v[i])
    

   
