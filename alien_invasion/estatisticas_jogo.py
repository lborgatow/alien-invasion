class EstatisticasJogo:
    """Armazena dados estatísticos de Alien Invasion"""

    def __init__(self, ai_configs):
        """Inicializa os dados estatísticos"""

        self.nivel = None
        self.pontuacao = None
        self.naves_restantes = None

        self.ai_configs = ai_configs
        self.redefinir_estatisticas()

        # Inicia a Invasão Alienígena em um estado inativo
        self.jogo_ativo = False

        # A pontuação máxima jamais deverá ser reiniciada
        self.pontuacao_maxima = 0

    def redefinir_estatisticas(self):
        """Inicializa os dados estatísticos que podem mudar durante o jogo"""

        self.naves_restantes = self.ai_configs.limite_naves
        self.pontuacao = 0
        self.nivel = 1
