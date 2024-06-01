import random
from individual import Individual, evaluate_fitness, initialize_individuals
from geneticOperators import selection, crossover, mutation, print_individual_actions


def genetic_algorithm(population_size, environment, generations=1000):
    """
    Executa um algoritmo genético para evolução de uma população de indivíduos.

    Args:
        population_size (int): Tamanho da população inicial.
        environment (Environment): Instância do ambiente do jogo.
        generations (int): Número de gerações a serem executadas. Padrão é 100.

    Returns:
        Individual: Melhor indivíduo encontrado durante a execução do algoritmo genético.
    """
    population = initialize_individuals(population_size)
    best_individual = None
    best_fitness = -float('inf')

    for generation in range(generations):
        # Avalia o fitness de cada indivíduo na população
        for individual in population:
            individual.fitness = evaluate_fitness(individual, environment)
            print(f"Fitness: {individual.fitness}")

        # Seleciona os indivíduos para a próxima geração
        selected = selection(population)

        # Realiza o cruzamento (crossover) para gerar descendentes
        descendants = []
        while len(descendants) < len(population) - len(selected):
            parent1, parent2 = random.sample(selected, 2)
            child1, child2 = crossover(parent1, parent2)
            descendants.extend([child1, child2])

        # Aplica mutação nos descendentes
        for descendant in descendants:
            mutation(descendant)

        # Nova população é formada pelos selecionados e seus descendentes
        population = selected + descendants

        # Atualiza o melhor indivíduo encontrado até agora
        current_fitness = max(individual.fitness for individual in population)
        current_best_individual = max(population, key=lambda ind: ind.fitness)
        if current_fitness > best_fitness:
            best_fitness = current_fitness
            best_individual = current_best_individual

        print(f"Geração {generation}: Melhor Fitness {best_fitness}")
        print(f"Melhores Ações: {print_individual_actions(best_individual)}")

    return best_individual


def run_best_model(environment, best_individual):
    """
    Executa o melhor modelo encontrado repetidamente no ambiente fornecido.

    Args:
        environment (Environment): Instância do ambiente do jogo.
        best_individual (Individual): Melhor indivíduo encontrado pelo algoritmo genético.
    """
    while True:
        state = environment.reset()
        for action, duration in best_individual.actions:
            state, fitness, time_left, level_progress = environment.step(action, duration)

        print("Loop completado, reiniciando...")


if __name__ == "__main__":
    from environment import Environment

    # Configuração do ambiente e do algoritmo genético
    environment = Environment(modo_silencioso=False)
    best_individual = genetic_algorithm(population_size=100, environment=environment)

    # Execução do melhor modelo encontrado
    run_best_model(environment, best_individual)
