import numpy as np
import random
import matplotlib.pyplot as plt

c1 = 0.8  # coef cognifivo 
c2 = 0.8  # coef social
w = 0.7   # inercia

def particle():
    while True:
        particle = []
        pos1 = []
        pos2 = []
        for i in range(6):
            rand = random.randint(0, 3) + random.random()
            rand2 = random.randint(0, 3) + random.random()
            pos1.append(rand)
            pos2.append(rand2)
        vel = [0, 0, 0, 0, 0, 0]
        particle.append(pos1)
        particle.append(pos2)
        particle.append(vel)
        if sum(particle[0]) <= 13 and sum(particle[1]) <= 13:
            return particle

def population(qnt):
    particles = []
    for i in range(qnt):
        particles.append(particle())
    return particles

def fitness(particle, index):
    prof1 = [3.5, 1, 1, 2, 5, 2.5]
    prof2 = [2, 2, 1.5, 1, 4.5, 3]
    prof3 = [2.5, 3.5, 1, 2.5, 4, 1.5]
    professores = [prof1, prof2, prof3]
    if sum(particle[index]) <= 13:
        s = 0
        for professor in professores:
            cont = 0
            while cont < len(particle[index]):
                double = [particle[index][cont], professor[cont]]
                minimum = min(double)
                s = s + minimum 
                cont = cont + 1
        return s/39
    else:
        return 0.01

def fitness_simple(particle):
    prof1 = [3.5, 2.5, 1, 2, 5, 2.5]
    prof2 = [2, 2, 1.5, 1, 4.5, 3]
    prof3 = [2.5, 3.5, 1, 2.5, 4, 1.5]
    professores = [prof1, prof2, prof3]
    sum = 0
    for professor in professores:
        cont = 0
        while cont < len(particle):
            double = [particle[cont], professor[cont]]
            minimum = min(double)
            sum = sum + minimum
            cont = cont + 1
    return sum/39

def pbest(particle):
    values = []
    cont = 0
    while cont < 2:
        if cont == 0:
            pbest = particle[0]
        elif cont == 1:
            if fitness(particle, cont) > fitness(particle, 0):
                pbest = particle[1]
        cont += 1
    return pbest

def gbest(pop_gerenated):
    pbests = []
    for i in pop_gerenated:
        pbests.append(list(pbest(i)))
    
    for indx in pbests:
        if pbests.index(indx) == 0:
            gbest = pbests[0]
        else:
            if fitness_simple(indx) > fitness_simple(gbest):
                gbest = indx
    return gbest

def new_velocity(part, pop):
    r1 = random.random()
    r2 = random.random()
    vel = part[2]
    new_v = w*np.array(vel) + c1*r1*(np.array(pbest(part)) - np.array(part[1])) + c2*r2*(np.array(gbest(pop)) - np.array(part[1]))
    return new_v

def new_pos(p, pop):
    nvel = new_velocity(p, pop)
    new = p[1] + nvel
    return new

def new_particle(p, pop):
    new_p = [np.array(p[0]), new_pos(p, pop), new_velocity(p, pop)]
    return new_p

pop = population(20)
values = []

graph = []

for i in range(100):
    best = gbest(pop)
    new_pop = []
    for j in pop:
        new_part = new_particle(j, pop)
        new_pop.append(new_part)
    pop = new_pop
    graph.append(fitness_simple(best))
    print(best)
    print(fitness_simple(best))
    print(sum(best))
    print()

plt.plot(graph)
plt.title('Aproveitamento dos Professores (%)')
plt.savefig("Aproveitamento.png")