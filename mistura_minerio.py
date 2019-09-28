import sys
from mip import *

with open(sys.argv[1], "r") as file:
    file_content = file.readlines()

# Lista de nomes dos minérios
minerios = file_content[0].split(',')[:-2]

# Teor mínimo de cada tipo de minério por tonelada extraída
teor_min = list(map(float, file_content[1].split(',')))

# Teor mínimo de cada tipo de minério por tonelada extraída
teor_max = list(map(float, file_content[2].split(',')))

# Lista de concentração de minério por pilha
a = [list(map(float, line.split(',')[:-2])) for line in file_content[3:]]

# Lista de disponibilidade de minério por pilha
disp = [float(d) for d in [line.split(',')[-2] for line in file_content[3:]]]

# Lista de custos por tonelada de minério extraído em cada pilha
custo = [float(c) for c in [line.split(',')[-1] for line in file_content[3:]]]

# Quantidade de toneladas de minério a serem exportadas
d = float(sys.argv[2])

model = Model("Mistura de minério", MINIMIZE)

# ====================================================================================

# Quantidade de toneladas de minério a serem extraídas de cada pilha
x = [model.add_var("Pilha %2d" % (i + 1)) for i in range(len(a))]

# ====================================================================================

# Minimizar o custo
model += xsum(x[i] * custo[i] for i in range(len(a)))

# Sujeito à:

# A quantidade de toneladas de minério extraídas deve ser igual à fornecida
model += xsum(x[i] for i in range(len(minerios))) == d

# Garante que não ultrapasse a capacidade da pilha
for i in range(len(a)):
    model += x[i] <= disp[i]

# Garante a quantidade mínima de concentração de minério
model += xsum((a[i][j] - teor_min[j]) * x[i] for i in range(len(a)) for j in range(len(minerios))) >= 0

# Garante a quantidade máxima de concentração de minério não seja ultrapassada
model += xsum((a[i][j] - teor_max[j]) * x[i] for i in range(len(a)) for j in range(len(minerios))) <= 0

# ====================================================================================
model.optimize()

for v in x:
    print("%s: %f" % (v.name, v.x))
