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


# Calcula o fitness de um indivíduo
def fitness(individual):
    total_distance = 0
    # A distancia total é a soma das distâncias entre todas as cidades da rota
    # O calculo não leva em consideração a volta para a cidade inicial
    for i in range(1, len(individual)):
        total_distance += graph.distance(individual[i-1], individual[i])
    # total_distance += graph.distance(individual[-1], individual[0])
    return 1/total_distance


# Gera uma população inicial aleatória
def population_generator(size, graph):
    population = []
    for i in range(size):
        individual = list(range(1, len(graph.get_graph())))
        random.shuffle(individual)
        population.append(individual)
    return population


# Seleciona os indivíduos que vão gerar a nova população através do método de seleção por torneio
def tournament_selection(population, selection_size, tournament_size):
    selected = []
    for i in range(selection_size):
        tounament = random.sample(population, tournament_size)
        selected.append(max(tounament, key=fitness))
    return selected


# Realiza o crossover de dois indivíduos
def crossover(parent1, parent2):
    child = []
    child_p1 = []
    child_p2 = []
    # Gera um ponto de corte aleatório, ou seja, dois genes aleatórios que serão
    # utilizados para pegar uma fatia do indivíduo 1
    gene1 = int(random.random() * len(parent1))
    gene2 = int(random.random() * len(parent1))
    # Garante que o ponto de corte 1 é menor que o ponto de corte 2
    startGene = min(gene1, gene2)
    endGene = max(gene1, gene2)
    # Pega a fatia gerada pelos pontos de corte do indivíduo 1 e adiciona a primeira parte do filho
    for i in range(startGene, endGene):
        child_p1.append(parent1[i])
    # Gera uma fatia com os genes do indivíduo 2 que não estão presentes na fatia do indivíduo 1
    child_p2 = [item for item in parent2 if item not in child_p1]
    # Pega os genes do indivíduo 2 que não estão na fatia do indivíduo 1 e adiciona ao filho
    # Como é o problema do caixeiro viajante é possível garantir que todos os genes estarão presentes no filho
    child = child_p1 + child_p2
    return child


# Realiza a mutação de um indivíduo
def mutation(individual, mutation_rate):
    # Percorre o indivíduo gene a gene, verificando se o gene em questão sofrerá mutação,
    # ou seja, se o valor aleatório gerado é menor que a taxa de mutação
    for swapped in range(len(individual)):
        if(random.random() < mutation_rate):
            # A mutação é feita trocando o gene em questão por outro aleatório (trocando duas cidades de lugar)
            swap_with = int(random.random() * len(individual))    
            gene1 = individual[swapped]
            gene2 = individual[swap_with]
            individual[swapped] = gene2
            individual[swap_with] = gene1
    return individual


# Gera uma nova população a partir da população atual
def generate_new_population(population, selection_size, mutation_rate, elite_size, tournament_size):
    # Utiliza o método de seleção por torneio para escolher os indivíduos que serão selecionados gerar a nova população
    selected_pop = tournament_selection(population, selection_size, tournament_size)
    new_population = []
    population.sort(key=fitness, reverse=True)
    # Passa os melhores indivíduos (elite) para a próxima geração
    for i in range(elite_size):
        new_population.append(population[i])
    # Cria os novos indivíduos que vão fazer parte da próxima geração através do crossover e mutação
    while len(new_population) < len(population):
        # Seleciona dois indivíduos aleatórios da população selecionada
        parent1 = random.choice(selected_pop)
        parent2 = random.choice(selected_pop)
        child = crossover(parent1, parent2)
        child = mutation(child, mutation_rate)
        new_population.append(child)
    return new_population


# Verifica se a população atingiu a estagnação
def check_stagnation(population, stagnation_percentage, generation):
    pop = population.copy()
    pop.sort(key=fitness, reverse=True)
    best_fitness = fitness(population[0])
    best_pops = 1
    for individual in pop:
        if fitness(individual) == best_fitness:
            best_pops += 1
    # Verifica se a porcentagem de indivíduos com a melhor aptidão é maior que a porcentagem de estagnação
    # Caso seja, o algoritmo é encerrado
    if best_pops/len(pop) >= stagnation_percentage:
        print("\nGerações: ", generation)
        return True
    return False


# Executa o algoritmo genético para o problema do caixeiro viajante
def travelling_salesman_GA(population, selection_size, mutation_rate, elite_size, tournament_size, generations, stagnation_percentage=0.65):
    resume_execution = True
    for i in range(generations):
        if resume_execution:
            tecla = input("Pressione R para resumir a execução, Enter para continuar a visualização: ")
            if tecla == 'r' or tecla == 'R':
                resume_execution = False
                continue
            pop = population.copy()
            pop.sort(key=fitness, reverse=True)
            print("Geração: ", i)
            print("Melhor indivíduo: ", pop[0])
            print("Melhor aptidão: ", fitness(pop[0]))
            print("Média de aptidão: ", sum([fitness(individual) for individual in pop])/len(pop))
            print("Pior indivíduo: ", pop[-1])
            print("Pior aptidão: ", fitness(pop[-1]))
            print("------------------------------------------------")
        # Gera uma nova população a cada geração do algoritmo genético
        population = generate_new_population(population, selection_size, mutation_rate, elite_size, tournament_size)
        if check_stagnation(population, stagnation_percentage, i):
            return population
    print("\nGerações: ", generations)
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
    population = travelling_salesman_GA(population, 50, 0.01, 6, 10, 10000, 0.65)
    population.sort(key=fitness, reverse=True)
    print("Resultado final:")
    print("Melhor indivíduo: ", population[0])
    print("Melhor aptidão: ", fitness(population[0]))
    print("Média de aptidão: ", sum([fitness(individual) for individual in population])/len(population))
    print("Pior indivíduo: ", population[-1])
    print("Pior aptidão: ", fitness(population[-1]))
    print("------------------------------------------------")
    print("População final: ")
    for individual in population:
        print("Individuo: ", individual, "\tAptidao:", fitness(individual))
    with open('saida.txt', 'w') as file:
        file.write(f"Resultado final:\n")
        file.write(f"Melhor individuo:  {population[0]}\n")
        file.write(f"Melhor aptidao:    {fitness(population[0])}\n")
        file.write(f"Media de aptidao:  {sum([fitness(individual) for individual in population])/len(population)}\n")
        file.write(f"Pior individuo:    {population[-1]}\n")
        file.write(f"Pior aptidao:      {fitness(population[-1])}\n")
        file.write(f"------------------------------------------------\n")
        file.write(f"Populacao final: \n")
        for individual in population:
            file.write("Individuo: %s\tAptidao: %s\n" % (individual, fitness(individual)))
