import random
from individual import Individual


def selection(individuals):
    """
    Realiza a seleção de indivíduos por meio de um torneio.

    Args:
        individuals (list): Lista de indivíduos para seleção.

    Returns:
        list: Lista de indivíduos selecionados.
    """
    tournament_size = 3
    selected = []
    for _ in range(len(individuals)):
        tournament = random.sample(individuals, tournament_size)
        winner = max(tournament, key=lambda ind: ind.fitness)
        selected.append(winner)
    return selected


def crossover(parent1, parent2):
    """
    Realiza o cruzamento entre dois pais para gerar dois filhos.

    Args:
        parent1 (Individual): Primeiro pai para o cruzamento.
        parent2 (Individual): Segundo pai para o cruzamento.

    Returns:
        tuple: Dois novos indivíduos filhos gerados pelo cruzamento.
    """
    crossover_point = random.randint(1, len(parent1.actions) - 1)
    child1_actions = parent1.actions[:crossover_point] + parent2.actions[crossover_point:]
    child2_actions = parent2.actions[:crossover_point] + parent1.actions[crossover_point:]
    child1 = Individual()
    child2 = Individual()
    child1.actions = child1_actions
    child2.actions = child2_actions
    return child1, child2


def mutation(individual, mutation_rate=0.1):
    """
    Realiza a mutação em um indivíduo com uma certa taxa de mutação.

    Args:
        individual (Individual): Indivíduo a ser mutado.
        mutation_rate (float): Taxa de mutação, entre 0 e 1. Padrão é 0.1.
    """
    for i in range(len(individual.actions)):
        if random.random() < mutation_rate:
            individual.actions[i] = (random.randint(0, 2), random.randint(1, 10))


def print_individual_actions(individual):
    """
    Gera uma representação em texto das ações de um indivíduo.

    Args:
        individual (Individual): Indivíduo cujas ações serão impressas.

    Returns:
        list: Lista de strings representando cada ação do indivíduo.
    """
    action_names = ["left", "right", "A"]
    actions = [f"{action_names[action]} for {duration} ticks" for action, duration in individual.actions]
    return actions
