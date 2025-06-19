from abc import ABC, abstractmethod
from utils.config import Config


class BuscadorBase(ABC):
    def __init__(self, config: Config):
        try:
            self.config = config
            self.navegador = config.navegador
            self.browser = config.navegador.browser
            self.id_buscador_db = self.inicia_buscador()
        except:
            raise ValueError("Erro de configuración do navegador. Non se atopa o navegador. Quizais fallou antes")

    """
    Crea un buscador a partir da configuración e do navegador.
    Chámase directamente ao constructor da clase buscador.
    Dispara un erro se non se pode crear o buscador.
    Retorna o identificador do buscador da base de datos.
    """
    @abstractmethod
    def inicia_buscador(self) -> int:
        pass

    @abstractmethod
    def garda_resultados(self, cerca):
        pass
