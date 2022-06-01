import sys
from time import sleep
import pygame
from tiro import Tiro
from alien import Alien


def verificar_eventos_keydown(event, ai_configs, tela, estatisticas, pts, nave, aliens, tiros):
    """Responde a pressionamentos de tecla"""

    if event.key == pygame.K_RIGHT:
        nave.mover_para_direita = True
    elif event.key == pygame.K_LEFT:
        nave.mover_para_esquerda = True
    elif event.key == pygame.K_SPACE:
        atirar(ai_configs, tela, nave, tiros)
    elif event.key == pygame.K_p:
        comecar_jogo(ai_configs, tela, estatisticas, pts, nave, aliens, tiros)
    elif event.key == pygame.K_q:
        sys.exit()


def verificar_eventos_keyup(event, ai_configs, nave):
    """Responde a solturas de tecla"""

    if event.key == pygame.K_RIGHT:
        nave.mover_para_direita = False
    elif event.key == pygame.K_LEFT:
        nave.mover_para_esquerda = False
    elif event.key == pygame.K_SPACE:
        ai_configs.shoot = False


def verificar_eventos(ai_configs, tela, estatisticas, pts, botao_play, nave, aliens, tiros):
    """Responde a eventos de pressionamento de teclas e de mouse"""

    # Observa eventos de teclado e mouse
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            verificar_eventos_keydown(event, ai_configs, tela, estatisticas, pts, nave, aliens, tiros)
        elif event.type == pygame.KEYUP:
            verificar_eventos_keyup(event, ai_configs, nave)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            verificar_botao_play(ai_configs, tela, estatisticas, pts, botao_play, nave,
                                 aliens, tiros, mouse_x, mouse_y)


def comecar_jogo(ai_configs, tela, estatisticas, pts, nave, aliens, tiros):
    """Inicia um novo jogo"""

    # Reinicia as configurações do jogo
    ai_configs.inicializar_configs_dinamicas()

    # Oculta o cursor do mouse
    pygame.mouse.set_visible(False)

    # Reinicia os dados estatísticos do jogo
    estatisticas.redefinir_estatisticas()
    estatisticas.jogo_ativo = True

    # Reinicia as imagens do painel de pontuação
    pts.preparar_pontuacao()
    pts.preparar_pontuacao_maxima()
    pts.preparar_nivel()
    pts.preparar_naves()

    # Esvazia a lista de alienígenas e de projéteis
    aliens.empty()
    tiros.empty()

    # Cria uma nova frota e centraliza a espaçonave
    criar_frota(ai_configs, tela, nave, aliens)
    nave.centralizar_nave()


def verificar_botao_play(ai_configs, tela, estatisticas, pts, botao_play, nave, aliens,
                         tiros, mouse_x, mouse_y):
    """"Inicia um novo jogo quando o jogador clicar em Play"""

    botao_clicado = botao_play.rect.collidepoint(mouse_x, mouse_y)
    if botao_clicado and not estatisticas.jogo_ativo:
        comecar_jogo(ai_configs, tela, estatisticas, pts, nave, aliens, tiros)


def atirar(ai_configs, tela, nave, tiros):
    """Dispara um tiro se o limite não foi atingido"""

    # Cria um novo projétil e o adiciona ao grupo de projéteis
    if len(tiros) < ai_configs.tiros_permitidos:
        novo_tiro = Tiro(ai_configs, tela, nave)
        tiros.add(novo_tiro)

        # Som do tiro
        som_tiro = pygame.mixer.Sound('som_tiro.wav')
        som_tiro.set_volume(0.05)
        som_tiro.play()


def atualizar_tela(ai_configs, tela, estatisticas, pts, nave, aliens, tiros, botao_play):
    """Atualiza as imagens na tela e alterna para a nova tela"""

    # Redesenha a tela a cada passagem pelo laço
    tela.fill(ai_configs.cor_fundo)

    # Redesenha todos os projéteis atrás da espaçonave e dos alienígenas
    for tiro in tiros.sprites():
        tiro.desenhar_tiro()
    nave.blitme()
    aliens.draw(tela)

    # Desenha a informação sobre pontuação
    pts.mostrar_pontuacao()

    # Desenha o botão Play se o jogo estiver inativo
    if not estatisticas.jogo_ativo:
        botao_play.desenhar_botao()

    # Deixa a tela mais recente visível
    pygame.display.flip()


def atualizar_tiros(ai_configs, tela, estatisticas, pts, nave, aliens, tiros):
    """Atualiza a posição dos projéteis e remove os projéteis antigos"""

    # Atualiza as posições dos projéteis
    tiros.update()

    # Livra-se dos projéteis que desapareceram
    for tiro in tiros.copy():
        if tiro.rect.bottom <= 0:
            tiros.remove(tiro)
    verificar_colisoes_tiro_alien(ai_configs, tela, estatisticas, pts, nave, aliens, tiros)


def verificar_pontuacao_maxima(estatisticas, pts):
    """Verifica se há uma nova pontuação máxima"""

    if estatisticas.pontuacao > estatisticas.pontuacao_maxima:
        estatisticas.pontuacao_maxima = estatisticas.pontuacao
        pts.preparar_pontuacao_maxima()


def verificar_colisoes_tiro_alien(ai_configs, tela, estatisticas, pts, nave, aliens, tiros):
    """Responde a colisões entre projéteis e alienígenas"""

    # Remove qualquer projétil e alienígena que tenham colidido
    colisoes = pygame.sprite.groupcollide(tiros, aliens, True, True)
    # (..., False, True) se quiser que o projétil suba até a borda superior eliminando todos os alien no caminho

    if colisoes:
        for _ in colisoes.values():
            estatisticas.pontuacao += ai_configs.pontos_alien * len(aliens)
            pts.preparar_pontuacao()
        verificar_pontuacao_maxima(estatisticas, pts)

    # Destrói os projéteis existentes, aumenta a velocidade e cria uma nova frota
    if len(aliens) == 0:  # Se a frota toda for destruída, inicia um novo nível
        tiros.empty()  # Remove todos os sprites restantes em um grupo
        ai_configs.aumentar_velocidade()

        # Aumenta o nível
        estatisticas.nivel += 1
        pts.preparar_nivel()

        criar_frota(ai_configs, tela, nave, aliens)


def verificar_bordas_frota(ai_configs, aliens):
    """Responde apropriadamente se algum alienígena alcançou uma borda"""

    for alien in aliens.sprites():
        if alien.verificar_bordas():
            mudar_direcao_tropa(ai_configs, aliens)
            break


def mudar_direcao_tropa(ai_configs, aliens):
    """Faz toda a frota descer e muda a sua direção"""

    for alien in aliens.sprites():
        alien.rect.y += ai_configs.velocidade_queda_frota
    ai_configs.direcao_frota *= -1


def colisao_nave(ai_configs, tela, estatisticas, pts, nave, aliens, tiros):
    """Responde ao fato da espaçonave ter sido atingida por um alienígena"""

    if estatisticas.naves_restantes > 0:
        # Decrementa naves_restantes
        estatisticas.naves_restantes -= 1

        # Atualiza o painel de pontuações
        pts.preparar_naves()

    else:
        estatisticas.jogo_ativo = False
        pygame.mouse.set_visible(True)

    # Esvazia a lista de alienígenas e de projéteis
    aliens.empty()
    tiros.empty()

    # Cria uma nova frota e centraliza a espaçonave
    criar_frota(ai_configs, tela, nave, aliens)
    nave.centralizar_nave()

    # Faz uma pausa
    sleep(0.5)


def verificar_aliens_inferior(ai_configs, tela, estatisticas, pts, nave, aliens, tiros):
    """Verifica se algum alienígena alcançou a parte inferior da tela"""

    tela_rect = tela.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= tela_rect.bottom:
            # Trata esse caso do mesmo modo feito quando a espaçonave é atingida
            colisao_nave(ai_configs, tela, estatisticas, pts, nave, aliens, tiros)
            break


def atualizar_aliens(ai_configs, tela, estatisticas, pts, nave, aliens, tiros):
    """Verifica se a frota está em uma das bordas e então
    atualiza as posições de todos os alienígenas da frota"""

    verificar_bordas_frota(ai_configs, aliens)
    aliens.update()

    # Verifica se houve colisões entre alienígenas e a espaçonave
    if pygame.sprite.spritecollideany(nave, aliens):
        colisao_nave(ai_configs, tela, estatisticas, pts, nave, aliens, tiros)

    # Verifica se há algum alienígena que atingiu a parte inferior da tela
    verificar_aliens_inferior(ai_configs, tela, estatisticas, pts, nave, aliens, tiros)


def obter_numero_aliens_x(ai_configs, largura_alien):
    """Determina o número de alienígenas que cabem em uma linha"""

    area_livre_x = ai_configs.largura_tela - 2 * largura_alien
    numero_aliens_x = int(area_livre_x / (2.3 * largura_alien))
    return numero_aliens_x


def obter_numero_linhas(ai_configs, altura_nave, altura_alien):
    """Determina o número de linhas com alienígenas que cabem na tela"""

    area_livre_y = (ai_configs.altura_tela - (3 * altura_alien) - altura_nave)
    numero_de_linhas = int(area_livre_y / (2.5 * altura_alien))
    return numero_de_linhas


def criar_alien(ai_configs, tela, aliens, numero_alien, numero_da_linha):
    """Cria um alienígena e o posiciona na linha"""

    # O espaçamento entre os alienígenas é igual à largura de um alienígena
    alien = Alien(ai_configs, tela)
    largura_alien = alien.rect.width
    alien.x = largura_alien + 2 * alien.rect.width * numero_alien
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * numero_da_linha
    aliens.add(alien)


def criar_frota(ai_configs, tela, nave, aliens):
    """Cria uma frota completa de alienígenas"""

    # Cria um alienígena e calcula o número de alienígenas em uma linha
    alien = Alien(ai_configs, tela)
    numero_aliens_x = obter_numero_aliens_x(ai_configs, alien.rect.width)
    numero_de_linhas = obter_numero_linhas(ai_configs, nave.rect.height, alien.rect.height)

    # Cria a frota de alienígenas
    for numero_da_linha in range(numero_de_linhas):
        for numero_alien in range(numero_aliens_x):
            criar_alien(ai_configs, tela, aliens, numero_alien, numero_da_linha)
