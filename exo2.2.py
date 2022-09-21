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
print(d)


n=15 
k=5
alpha = 0.5
#nbcont=n+n+(n*n)
#nbconty = n*k
nbvar=n*n
nbvary=n
nbvarz = 1
#sect = [0,1,2]

# Range of plants and warehouses
#lignes = range(nbcont)
colonnes = range(nbvar)

#lignesy = range(nbconty)
colonnesy = range(nbvary)

# Matrice des contraintes
a1 = []
for j in range(n):
    l = []
    for i in range(n):
        for s in range(n):
            if s == j :
                l.append(v[i])
            else:
                l.append(0)
    a1.append(l)
			
		
a2 = []
for m in range (n):
	a2.append(m*n*[0]+n*[1]+(n-m-1)*n*[0])

a3 = []	
for m in range (n):
	a3.append(1)
    
a4 = []
for i in range(n):
    for j in range(k):
        a4.append([1,-1])

a5 = []
for i in range(n):
    l = []
    for j in range(n*n):
        if i*n <= j <= i*n+n-1:
            l.append(1)
        else:
            l.append(0)
    a5.append(l)

# Second membre
b1 = n*[((1+alpha)/k) * sum(v)] 
b2 = n*[1]
b3 = k
b4 = 0
#b5 = 0

# Coefficients de la fonction objectif
c =[1]
		
m = Model("mogplex")     
        
# declaration variables de decision
x = []
for i in range (n):
    for j in range(n):
            x.append(m.addVar(vtype=GRB.BINARY, lb=0, name="x%d,%d" % (i+1,j+1)))
y = []
for i in range (n):
    y.append(m.addVar(vtype=GRB.CONTINUOUS, lb=0, name='y%d'%(i+1)))

z = m.addVar(vtype=GRB.CONTINUOUS, lb=0, name='z')

# maj du modele pour integrer les nouvelles variables
m.update()

obj = LinExpr();
obj = z
        
# definition de l'objectif
m.setObjective(obj,GRB.MINIMIZE)

# Definition des contraintes
for i in range (n):
    m.addConstr(quicksum(a1[i][j]*x[j] for j in colonnes) <= b1[i], "Contrainte%d" % i)


for i in range (n):
    m.addConstr(quicksum(a2[i][j]*x[j] for j in colonnes) == b2[i], "Contrainte%d" % (i+k))


m.addConstr(quicksum(a3[j]*y[j] for j in colonnesy) == b3, "Contrainte%d" % (k))

for i in range(n*n):
    m.addConstr(x[i] - y[i%n] <= b4, "Contrainte%d" % (k))


for i in range (n):
    m.addConstr(quicksum(a5[i][j]*max(d[i][j%n],d[j%n][i])*x[j] for j in colonnes) <= z, "Contrainte z %d" % (i))

# Resolution
m.optimize()

print("")                
print('Solution optimale:')


if m.status == GRB.OPTIMAL :
    # Résultat
    for var in m.getVars():
        if var.x > 0:
            print('%s %g' % (var.varName, var.x))         
    print("")
    print('Valeur de la fonction objectif :', m.objVal)
    print("")
    # Pour lire le résultat       
    for i in range(n):
        print(i+1, nom_v[i])
    

   
