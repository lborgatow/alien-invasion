import pygame.font


class Botao:
    """Representa um botão"""

    def __init__(self, tela, mensagem):
        """Inicializa os atributos do botão"""

        self.imagem_mensagem_rect = None
        self.imagem_mensagem = None

        self.tela = tela
        self.tela_rect = tela.get_rect()

        # Define as dimensões e as propriedades do botão
        self.largura, self.altura = 200, 50
        self.cor_botao = (0, 255, 0)
        self.cor_texto = (255, 255, 255)
        self.fonte = pygame.font.SysFont(None, 48)

        # Constrói o objeto rect do botão e o centraliza
        self.rect = pygame.Rect(0, 0, self.largura, self.altura)
        self.rect.center = self.tela_rect.center

        # A mensagem do botão deve ser preparada apenas uma vez
        self.preparar_mensagem(mensagem)

    def preparar_mensagem(self, mensagem):
        """Transforma mensagem em uma imagem renderizada e centraliza o texto no botão"""

        self.imagem_mensagem = self.fonte.render(mensagem, True, self.cor_texto, self.cor_botao)
        self.imagem_mensagem_rect = self.imagem_mensagem.get_rect()
        self.imagem_mensagem_rect.center = self.rect.center

    def desenhar_botao(self):
        """Desenha um botão em branco e, em seguida, desenha a mensagem"""

        self.tela.fill(self.cor_botao, self.rect)
        self.tela.blit(self.imagem_mensagem, self.imagem_mensagem_rect)
