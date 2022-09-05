import random
from math import inf

class Graph:
    def __init__(self, size):
        self.graph = []
        for i in range(size+1):
            self.graph.append([])
    
    def add_edge(self, vertex1, vertex2, distance):
        for vertex in self.graph[vertex1]:
            if vertex[0] == vertex2:
                return
        for vertex in self.graph[vertex2]:
            if vertex[0] == vertex1:
                return
        self.graph[vertex1].append((vertex2, distance))
        self.graph[vertex2].append((vertex1, distance))

    def get_vertex(self, index):
        return self.graph[index]
    
    def get_graph(self):
        return self.graph
    
    def distance(self, vertex1, vertex2):
        for vertex in self.graph[vertex1]:
            if vertex[0] == vertex2:
                return vertex[1]
        return inf

def fitness(individual):
    total_distance = 0
    for i in range(1, len(individual)):
        total_distance += graph.distance(individual[i-1], individual[i])
    return 1/total_distance


def population_generator(size, graph):
    population = []
    for i in range(size):
        individual = list(range(1, len(graph.get_graph())))
        random.shuffle(individual)
        population.append(individual)
    return population

def natural_selection(population, size_of_selection, tournament_size):
    selected = []
    for i in range(size_of_selection):
        tounament = random.sample(population, tournament_size)
        selected.append(max(tounament, key=fitness))
    return selected

def crossover(parent1, parent2):
    child = []
    childP1 = []
    childP2 = []
    
    geneA = int(random.random() * len(parent1))
    geneB = int(random.random() * len(parent1))
    
    startGene = min(geneA, geneB)
    endGene = max(geneA, geneB)

    for i in range(startGene, endGene):
        childP1.append(parent1[i])
        
    childP2 = [item for item in parent2 if item not in childP1]

    child = childP1 + childP2
    return child


def mutation(individual, mutation_rate):
    for swapped in range(len(individual)):
        if(random.random() < mutation_rate):
            swapWith = int(random.random() * len(individual))
            
            city1 = individual[swapped]
            city2 = individual[swapWith]
            
            individual[swapped] = city2
            individual[swapWith] = city1
    return individual


def generate_new_population(population, selection_size, mutation_rate, elite_size):
    selected_pop = natural_selection(population, selection_size, 5)
    new_population = []
    population.sort(key=fitness, reverse=True)
    for i in range(elite_size):
        new_population.append(population[i])
    while len(new_population) < len(population):
        parent1 = random.choice(selected_pop)
        parent2 = random.choice(selected_pop)
        child = crossover(parent1, parent2)
        child = mutation(child, mutation_rate)
        new_population.append(child)
    return new_population


def genetic_algorithm(population, selection_size, mutation_rate, elite_size, generations):
    for i in range(generations):
        # print(i)
        population = generate_new_population(population, selection_size, mutation_rate, elite_size)
        pop = population.copy()
        pop.sort(key=fitness, reverse=True)
        best_fitness = fitness(population[0])
        best_pops = 1
        for individual in pop:
            if fitness(individual) == best_fitness:
                best_pops += 1
        if best_pops == 0.65*len(pop):
            print(i)
            break
    return population


if __name__ == "__main__":
    graph = Graph(6)
    graph.add_edge(1, 2, 10)
    graph.add_edge(1, 3, 12)
    graph.add_edge(1, 5, 11)
    graph.add_edge(2, 4, 5)
    graph.add_edge(2, 6, 45)
    graph.add_edge(3, 4, 90)
    graph.add_edge(3, 5, 26)
    graph.add_edge(3, 6, 5)
    graph.add_edge(4, 5, 4)
    graph.add_edge(4, 6, 25)
    graph.add_edge(5, 6, 8)
    
    population = population_generator(100, graph)
    population = genetic_algorithm(population, 50, 0.01, 6, 100000)
    population.sort(key=fitness, reverse=True)
    print(len(population))
    for individual in population:
        print(individual, fitness(individual))
