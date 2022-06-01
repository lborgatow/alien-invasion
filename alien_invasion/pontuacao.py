import pygame.font
from pygame.sprite import Group
from nave import Nave


class Pontuacao:
    """Uma classe para mostrar informações sobre a pontuação"""

    def __init__(self, ai_configs, tela, estatisticas):
        """Inicializa os atributos de pontuação"""

        self.naves = None
        self.nivel_rect = None
        self.imagem_nivel = None
        self.pontuacao_maxima_rect = None
        self.imagem_pontuacao_maxima = None
        self.pontuacao_rect = None
        self.imagem_pontuacao = None

        self.tela = tela
        self.tela_rect = tela.get_rect()
        self.ai_configs = ai_configs
        self.estatisticas = estatisticas

        # Configurações de fonte para as informações de pontuação
        self.cor_texto = (255, 255, 255)
        self.fonte = pygame.font.SysFont(None, 48)

        # Prepara a imagem da pontuação inicial
        self.preparar_pontuacao()
        self.preparar_pontuacao_maxima()
        self.preparar_nivel()
        self.preparar_naves()

    def preparar_pontuacao(self):
        """Transforma a pontuação em uma imagem renderizada"""

        pontuacao_arredondada = int(round(self.estatisticas.pontuacao, -1))
        pontuacao_str = str(f"{pontuacao_arredondada:,}")
        self.imagem_pontuacao = self.fonte.render(pontuacao_str, True, self.cor_texto,
                                                  self.ai_configs.cor_fundo)

        # Exibe a pontuação na parte superior direita da tela
        self.pontuacao_rect = self.imagem_pontuacao.get_rect()
        self.pontuacao_rect.right = self.tela_rect.right - 20
        self.pontuacao_rect.top = 20

    def preparar_pontuacao_maxima(self):
        """Transforma a pontuação máxima em uma imagem renderizada"""

        pontuacao_maxima = int(round(self.estatisticas.pontuacao_maxima, -1))
        pontuacao_maxima_str = str(f"{pontuacao_maxima:,}")
        self.imagem_pontuacao_maxima = self.fonte.render(pontuacao_maxima_str, True,
                                                         self.cor_texto, self.ai_configs.cor_fundo)

        # Exibe a pontuação máxima na parte superior da tela
        self.pontuacao_maxima_rect = self.imagem_pontuacao_maxima.get_rect()
        self.pontuacao_maxima_rect.centerx = self.tela_rect.centerx
        self.pontuacao_maxima_rect.top = self.pontuacao_rect.top

    def preparar_nivel(self):
        """Transforma o nível em uma imagem renderizada"""

        self.imagem_nivel = self.fonte.render(str(self.estatisticas.nivel), True,
                                              self.cor_texto, self.ai_configs.cor_fundo)

        # Posiciona o nível abaixo da pontuação
        self.nivel_rect = self.imagem_nivel.get_rect()
        self.nivel_rect.right = self.pontuacao_rect.right
        self.nivel_rect.top = self.pontuacao_rect.bottom + 10

    def preparar_naves(self):
        """Mostra quantas espaçonaves restam"""

        self.naves = Group()
        for numero_de_naves in range(self.estatisticas.naves_restantes):
            nave = Nave(self.ai_configs, self.tela)
            nave.rect.x = 10 + numero_de_naves * nave.rect.width
            nave.rect.y = 10
            self.naves.add(nave)

    def mostrar_pontuacao(self):
        """Desenha a pontuação na tela"""
        # Desenha a imagem da pontuação na tela no local especificado por pontuacao_rect
        self.tela.blit(self.imagem_pontuacao, self.pontuacao_rect)
        self.tela.blit(self.imagem_pontuacao_maxima, self.pontuacao_maxima_rect)
        self.tela.blit(self.imagem_nivel, self.nivel_rect)

        # Desenha as espaçonaves
        self.naves.draw(self.tela)
