import random
from ucs import UniformCostSearch

class GeneticAlgorithm:
    def __init__(self, graph, population_size=100, generations=200, mutation_rate=0.1):
        self.graph = graph
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.ucs = UniformCostSearch(graph)

    def fitness(self, route):
        total_distance = 0
        for i in range(len(route) - 1):
            _, distance = self.ucs.find_path(route[i], route[i + 1])
            if distance == float('infinity'):
                return float('infinity')
            total_distance += distance
        return total_distance

    def initialize_population(self, stops, start, end=None):
        population = []
        base_route = [start] + stops + ([end] if end else [])
        for _ in range(self.population_size):
            if end:
                # Không xáo trộn start và end
                middle = stops.copy()
                random.shuffle(middle)
                individual = [start] + middle + [end]
            else:
                # Xáo trộn toàn bộ, giữ start ở đầu
                middle = stops.copy()
                random.shuffle(middle)
                individual = [start] + middle
            population.append(individual)
        return population

    def select_parent(self, population, fitnesses):
        total_fitness = sum(1 / (f + 1e-6) for f in fitnesses)  # Nghịch đảo fitness
        pick = random.uniform(0, total_fitness)
        current = 0
        for i, fitness in enumerate(fitnesses):
            current += 1 / (fitness + 1e-6)
            if current > pick:
                return population[i]
        return population[-1]

    def crossover(self, parent1, parent2):
        size = len(parent1)
        start, end = sorted(random.sample(range(1, size - 1), 2))
        child = [None] * size
        child[0] = parent1[0]  # Giữ start
        if parent1[-1] == parent2[-1]:  # Nếu có end
            child[-1] = parent1[-1]
        child[start:end] = parent1[start:end]

        ptr = 1
        for gene in parent2[1:]:
            if gene not in child:
                while ptr < size and child[ptr] is not None:
                    ptr += 1
                if ptr < size:
                    child[ptr] = gene
        return child

    def mutate(self, individual):
        if random.random() < self.mutation_rate:
            # Đảm bảo có ít nhất 2 trạm trung gian để hoán đổi
            end_offset = 2 if individual[-1] else 1
            if len(individual) > 2 + end_offset:  # Cần ít nhất 3 điểm (start + 2 trạm) hoặc 4 (nếu có end)
                i, j = random.sample(range(1, len(individual) - end_offset), 2)
                individual[i], individual[j] = individual[j], individual[i]
        return individual

    def find_path(self, start, stops, end=None):
        population = self.initialize_population(stops, start, end)
        best_route = None
        best_distance = float('infinity')

        for _ in range(self.generations):
            fitnesses = [self.fitness(individual) for individual in population]
            new_population = []

            # Giữ cá thể tốt nhất
            min_fitness_idx = fitnesses.index(min(fitnesses))
            if fitnesses[min_fitness_idx] < best_distance:
                best_distance = fitnesses[min_fitness_idx]
                best_route = population[min_fitness_idx].copy()

            for _ in range(self.population_size):
                parent1 = self.select_parent(population, fitnesses)
                parent2 = self.select_parent(population, fitnesses)
                child = self.crossover(parent1, parent2)
                child = self.mutate(child)
                new_population.append(child)

            population = new_population

        # Tạo đường đi chi tiết
        detailed_path = []
        total_distance = 0
        for i in range(len(best_route) - 1):
            segment_path, segment_distance = self.ucs.find_path(best_route[i], best_route[i + 1])
            if i > 0:
                segment_path = segment_path[1:]  # Tránh lặp điểm
            detailed_path += segment_path
            total_distance += segment_distance

        return detailed_path, total_distance