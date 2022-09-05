from genetic_algorithm import *

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
population = travelling_salesman_GA(population, 50, 0.01, 6, 100000)
population.sort(key=fitness, reverse=True)
print(len(population))
for individual in population:
    print(individual, fitness(individual))