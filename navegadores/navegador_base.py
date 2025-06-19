from abc import ABC, abstractmethod
from selenium.webdriver.remote.webdriver import WebDriver
from typing import Tuple, Union
from utils.config import Config


class NavegadorBase(ABC):

    def __init__(self, config: Config, anchura: int, altura: int):
        """
        Inicializa as variables de clase e chama á función init_navegador, implementada polas clases fillas.
        """
        try:
            self.config = config
            self.repository = config.repository
            self.anchura = anchura
            self.altura = altura
            self.id_navegador_db, self.browser = self.init_navegador()
        except:
            raise ValueError("Erro de configuración do navegador. Non se atopa o repository")

    @abstractmethod
    def init_navegador(self) -> Tuple[int, WebDriver]:
        """
        Inicializa o navegador.
        """
        pass

    def captura_pantalla(self, nom: str) -> None:
        """
        Realiza unha captura de pantalla.

        Args:
        - nome: Nome do ficheiro onde se gardará a captura.
        """
        self.browser.save_screenshot(nom)

    def pecha_navegador(self):
        """
        Pecha o navegador.
        """
        self.browser.quit()
