import numpy as np
from pyboy import PyBoy
from pyboy.utils import WindowEvent


class Environment:
    """
    Classe que representa o ambiente do jogo Mario emulado pelo PyBoy.

    Atributos:
        pyboy (PyBoy): Instância do emulador PyBoy.
        mario (GameWrapper): Instância do jogo Mario.

    Métodos:
        __init__(self, filename='mario.gb', silent_mode=True):
            Inicializa o ambiente do jogo.
        calculate_fitness(self):
            Calcula o valor de fitness baseado no estado atual do jogo.
        is_game_over(self):
            Verifica se o jogo terminou.
        reset(self):
            Reinicia o jogo e retorna o estado inicial.
        step(self, action_index, duration):
            Executa uma ação no jogo por uma determinada duração.
        get_state(self):
            Retorna o estado atual do jogo como uma matriz NumPy.
        close(self):
            Encerra o emulador PyBoy.
    """

    def __init__(self, filename='mario.gb', modo_silencioso=True):
        """
        Inicializa o ambiente do jogo.

        Args:
            filename (str): Nome do arquivo ROM do jogo. Padrão é 'mario.gb'.
            silent_mode (bool): Se True, executa o emulador em modo silencioso. Padrão é True.
        """
        window_type = "headless" if modo_silencioso else "SDL2"
        self.pyboy = PyBoy(filename, window=window_type, debug=modo_silencioso)
        self.pyboy.set_emulation_speed(500)
        self.mario = self.pyboy.game_wrapper
        self.mario.start_game()

    def calculate_fitness(self):
        """
        Calcula o valor de fitness baseado no estado atual do jogo.

        Returns:
            int: Valor de fitness calculado.
        """
        return self.mario.score + 2 * self.mario.level_progress + self.mario.time_left

    def is_game_over(self):
        """
        Verifica se o jogo terminou.

        Returns:
            bool: True se o jogo terminou, False caso contrário.
        """
        return self.mario.lives_left == 1 or self.mario.score < 0

    def reset(self):
        """
        Reinicia o jogo e retorna o estado inicial.

        Returns:
            np.ndarray: Estado inicial do jogo como uma matriz NumPy.
        """
        self.mario.reset_game()
        self.pyboy.tick()
        return self.get_state()

    def step(self, action_index, duration):
        """
        Executa uma ação no jogo por uma determinada duração.

        Args:
            action_index (int): Índice da ação a ser executada.
            duration (int): Duração da ação em ticks.

        Returns:
            tuple: Estado atual do jogo, valor de fitness, tempo restante, progresso no nível.
        """
        if self.is_game_over():
            print("Fim de jogo detectado")
            return None, 0, 0, "Fim de Jogo"

        actions = {
            0: WindowEvent.PRESS_ARROW_LEFT,
            1: WindowEvent.PRESS_ARROW_RIGHT,
            2: WindowEvent.PRESS_BUTTON_A
        }
        release_actions = {
            0: WindowEvent.RELEASE_ARROW_LEFT,
            1: WindowEvent.RELEASE_ARROW_RIGHT,
            2: WindowEvent.RELEASE_BUTTON_A
        }

        action = actions.get(action_index, WindowEvent.PASS)
        self.pyboy.send_input(action)
        for _ in range(duration):
            self.pyboy.tick()

        release_action = release_actions.get(action_index, WindowEvent.PASS)
        self.pyboy.send_input(release_action)
        self.pyboy.tick()

        time_left = self.mario.time_left
        level_progress = self.mario.level_progress
        return self.get_state(), self.calculate_fitness(), time_left, level_progress

    def get_state(self):
        """
        Retorna o estado atual do jogo como uma matriz NumPy.

        Returns:
            np.ndarray: Estado atual do jogo.
        """
        return np.asarray(self.mario.game_area())

    def close(self):
        """
        Encerra o emulador PyBoy.
        """
        self.pyboy.stop()
