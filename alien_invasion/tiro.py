import pygame
from pygame.sprite import Sprite


class Tiro(Sprite):
    """Administra os projéteis disparados pela espaçonave"""

    def __init__(self, ai_configs, tela, nave):
        """Cria um objeto para o projétil na posição da espaçonave"""

        super().__init__()
        self.tela = tela

        # Cria um retângulo para o projétil em (0, 0) e, em seguida, define a posição correta
        self.rect = pygame.Rect(0, 0, ai_configs.largura_tiro, ai_configs.altura_tiro)
        self.rect.centerx = nave.rect.centerx
        self.rect.top = nave.rect.top

        # Armazena a posição do projétil como um valor decimal
        self.y = float(self.rect.y)

        # Armazena a cor e a velocidade do projétil
        self.cor = ai_configs.cor_tiro
        self.fator_velocidade = ai_configs.fator_velocidade_tiro

    def update(self):
        """Move o projétil para cima na tela"""

        # Atualiza a posição decimal do projétil
        self.y -= self.fator_velocidade

        # Atualiza a posição de rect
        self.rect.y = self.y

    def desenhar_tiro(self):
        """Desenha o projétil na tela"""

        pygame.draw.rect(self.tela, self.cor, self.rect)
