import pygame.image
from pygame.sprite import Sprite


class Alien(Sprite):
    """Representa um único alienígena da frota"""

    def __init__(self, ai_configs, tela):
        """Inicializa o alienígena e define sua posição inicial"""

        super().__init__()
        self.tela = tela
        self.ai_configs = ai_configs

        # Carrega a imagem do alienígena e define seu atributo rect
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # Inicia cada novo alienígena próximo à parte superior esquerda da tela
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Armazena a posição exata do alienígena
        self.x = float(self.rect.x)

    def verificar_bordas(self):
        """Devolve True se o alienígena estiver na borda da tela"""

        tela_rect = self.tela.get_rect()
        if self.rect.right >= tela_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """Move o alienígena para a direita ou para a esquerda"""

        self.x += (self.ai_configs.fator_velocidade_alien * self.ai_configs.direcao_frota)
        self.rect.x = self.x

    def blitme(self):
        """Desenha o alienígena em sua posição atual"""

        self.tela.blit(self.image, self.rect)
