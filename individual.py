import random
import numpy as np


class Individual:
    """
    Classe que representa um indivíduo em um algoritmo genético.

    Atributos:
        actions (list): Lista de ações (índice da ação e duração) que o indivíduo executa.
        fitness (float): Valor de fitness do indivíduo.

    Métodos:
        __init__(self):
            Inicializa um novo indivíduo com ações aleatórias, incluindo pulos longos para obstáculos maiores.
        generate_actions(self, environment):
            Gera ações para o indivíduo, incluindo pulos adaptativos para obstáculos grandes.
        evaluate(self, environment):
            Avalia o indivíduo no ambiente fornecido e calcula seu fitness.
    """

    def __init__(self):
        """
        Inicializa um novo indivíduo com ações aleatórias, incluindo pulos longos para obstáculos maiores.
        """
        self.actions = self.generate_actions()
        self.fitness = 0

    def generate_actions(self, environment=None):
        """
        Gera ações para o indivíduo, incluindo pulos adaptativos para obstáculos grandes.

        Args:
            environment (Environment, optional): Instância do ambiente do jogo. Default é None.

        Returns:
            list: Lista de ações geradas (índice da ação e duração).
        """
        actions = []
        for _ in range(5000):
            action = random.choices([0, 1, 2], weights=[1, 2, 1])[0]
            duration = random.randint(1, 10)

            if action == 2:
                if environment and self.detect_large_obstacle(environment):
                    if random.random() < 0.5:
                        duration = random.randint(5, 15)
                else:
                    if random.random() < 0.2:
                        duration = random.randint(5, 15)

            actions.append((action, duration))
        return actions

    def evaluate(self, environment):
        """
        Avalia o indivíduo no ambiente fornecido e calcula seu fitness.

        Args:
            environment (Environment): Instância do ambiente do jogo.

        Returns:
            float: Valor de fitness calculado.
        """
        state = environment.reset()
        total_fitness = 0
        max_time = 0
        right_moves = 0
        game_ended = False

        for action, duration in self.actions:
            if game_ended == "Fim de Jogo":
                break
            new_state, fitness, time_left, game_ended = environment.step(action, duration)
            total_fitness += fitness
            max_time = max(max_time, time_left)
            right_moves += 1 if action == 1 else 0
            state = new_state

        time_points = 500 if max_time > 0 else 0
        self.fitness = total_fitness + time_points + right_moves * 5
        return self.fitness

    def detect_large_obstacle(self, environment):
        """
        Função para detectar a presença de obstáculos grandes no ambiente.

        Args:
            environment (Environment): Instância do ambiente do jogo.

        Returns:
            bool: True se houver um obstáculo grande, False caso contrário.
        """
        # Exemplo simplificado: Detecta obstáculos grandes baseados em lógica do ambiente
        return environment.detect_large_obstacle()

    def set_actions(self, actions):
        """
        Define as ações para o indivíduo.

        Args:
            actions (list): Lista de ações (índice da ação e duração).

        """
        self.actions = actions

    def get_fitness(self):
        """
        Retorna o fitness do indivíduo.

        Returns:
            float: Valor de fitness do indivíduo.

        """
        return self.fitness


def evaluate_fitness(individual, environment):
    """
    Avalia o fitness de um indivíduo no ambiente fornecido.

    Args:
        individual (Individual): Instância do indivíduo a ser avaliado.
        environment (Environment): Instância do ambiente do jogo.

    Returns:
        float: Valor de fitness normalizado.
    """
    fitness = individual.evaluate(environment)
    normalized_fitness = fitness / 10000
    return normalized_fitness


def initialize_individuals(population_size):
    """
    Inicializa uma população de indivíduos.

    Args:
        population_size (int): Tamanho da população a ser criada.

    Returns:
        list: Lista de instâncias de indivíduos.
    """
    return [Individual() for _ in range(population_size)]
