import pygame
from pygame.sprite import Group
from configs import Configs
from estatisticas_jogo import EstatisticasJogo
from pontuacao import Pontuacao
from botao import Botao
from nave import Nave
import funcionalidades_jogo as fj


def executar_jogo():
    """Executa o jogo Alien Invasion"""

    # Inicializa o pygame, as configurações e a tela
    pygame.init()

    # instância da classe Configs()
    ai_configs = Configs()

    # Cria uma janela de exibição chamada tela com as dimensões escolhidas
    tela = pygame.display.set_mode((ai_configs.largura_tela, ai_configs.altura_tela))
    pygame.display.set_caption("Alien Invasion")

    # Cria o botão Play
    botao_play = Botao(tela, "Play")

    # Cria uma instância para armazenar dados estatísticos do jogo e cria painel de pontuação
    estatisticas = EstatisticasJogo(ai_configs)
    pts = Pontuacao(ai_configs, tela, estatisticas)

    # Cria uma espaçonave, um grupo de projéteis e um grupo de alienígenas
    nave = Nave(ai_configs, tela)
    tiros = Group()
    aliens = Group()

    # Cria a frota de alienígenas
    fj.criar_frota(ai_configs, tela, nave, aliens)

    # Inicia o laço principal do jogo
    while True:
        fj.verificar_eventos(ai_configs, tela, estatisticas, pts, botao_play, nave, aliens, tiros)

        if estatisticas.jogo_ativo:
            nave.atualizar()
            fj.atualizar_tiros(ai_configs, tela, estatisticas, pts, nave, aliens, tiros)
            fj.atualizar_aliens(ai_configs, tela, estatisticas, pts, nave, aliens, tiros)

        fj.atualizar_tela(ai_configs, tela, estatisticas, pts, nave, aliens, tiros, botao_play)


executar_jogo()
