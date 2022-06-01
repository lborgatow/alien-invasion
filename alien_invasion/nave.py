import pygame.image
from pygame.sprite import Sprite


class Nave(Sprite):
    """Representa uma nave"""

    def __init__(self, ai_configs, tela):
        """Inicializa a espaçonave e define sua posição inicial"""

        super(Nave, self).__init__()
        self.tela = tela
        self.ai_configs = ai_configs

        # Carrega a imagem da espaçonave e obtém seu rect
        self.image = pygame.image.load('images/nave.bmp')
        self.rect = self.image.get_rect()
        self.tela_rect = tela.get_rect()

        # Inicia cada nova espaçonave na parte inferior central da tela
        self.rect.centerx = self.tela_rect.centerx
        self.rect.bottom = self.tela_rect.bottom

        # Armazena um valor decimal para o centro da espaçonave
        self.center = float(self.rect.centerx)

        # Flag de movimento
        self.mover_para_direita = False
        self.mover_para_esquerda = False

    def centralizar_nave(self):
        """Centraliza a espaçonave na tela"""

        self.center = self.tela_rect.centerx

    def atualizar(self):
        """Atualiza a posição da espaçonave conforme as flags de movimento"""

        # Atualiza o valor do centro da espaçonave, e não o retângulo
        if self.mover_para_direita and self.rect.right < self.tela_rect.right:
            self.center += self.ai_configs.fator_velocidade_nave
        if self.mover_para_esquerda and self.rect.left > 0:
            self.center -= self.ai_configs.fator_velocidade_nave

        # Atualiza o objeto rect de acordo com self.center
        self.rect.centerx = self.center

    def blitme(self):
        """Desenha a espaçonave em sua posição atual"""

        self.tela.blit(self.image, self.rect)
