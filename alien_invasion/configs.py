from tkinter import *


class Configs:
    """Armazena todas as configurações de Alien Invasion"""

    def __init__(self):
        """Inicializa as configurações estáticas do jogo"""

        self.direcao_frota = None
        self.pontos_alien = None
        self.fator_velocidade_alien = None
        self.fator_velocidade_tiro = None
        self.fator_velocidade_nave = None

        # Configurações da tela
        root = Tk()
        largura_tela = root.winfo_screenwidth()  # Retorna a largura da tela em pixels
        altura_tela = root.winfo_screenheight()  # Retorna a altura da tela em pixels
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela
        self.cor_fundo = (0, 0, 0)

        # Configurações da espaçonave
        self.limite_naves = 3

        # Configurações dos projéteis
        self.largura_tiro = 6
        self.altura_tiro = 18
        self.cor_tiro = 255, 0, 0
        self.tiros_permitidos = 3

        # Configurações dos alienígenas
        self.velocidade_queda_frota = 10

        # A taxa com que a velocidade do jogo aumenta
        self.escala_aceleracao = 1.1

        # A taxa com que os pontos para cada alienígena aumentam
        self.escala_pontuacao = 1.5

        self.inicializar_configs_dinamicas()

    def inicializar_configs_dinamicas(self):
        """Inicializa as configurações que mudam ao decorrer do jogo"""

        # Velocidades
        self.fator_velocidade_nave = 1.8
        self.fator_velocidade_tiro = 3
        self.fator_velocidade_alien = 1.4

        # Pontuação
        self.pontos_alien = 50

        # direcao_frota = 1 representa a direita; -1 representa a esquerda
        self.direcao_frota = 1

    def aumentar_velocidade(self):
        """Aumenta as configurações de velocidade"""

        self.fator_velocidade_nave *= self.escala_aceleracao
        self.fator_velocidade_tiro *= self.escala_aceleracao
        self.fator_velocidade_alien *= self.escala_aceleracao

        self.pontos_alien = int(self.pontos_alien * self.escala_pontuacao)
