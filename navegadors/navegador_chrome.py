from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from repository.repository import Repository
from navegadors.navegador_base import NavegadorBase
from utils.config import Config
import os
import logging


class ChromeNavegador(NavegadorBase):

    def init_navegador(self):
        browser = None
        id_navegador_db = 1
        user_agent = self.repository.cerca_userAgent(id_navegador_db)

        if user_agent:
            options = Options()
            options.add_argument(f"user-agent={user_agent}")
            options.add_argument("--lang=gl")

            driver_path = os.path.join(self.config.current_directory, "Controladores", self.config.CHROME_DRIVER_PATH)

            service = Service(driver_path)

            try:
                browser = webdriver.Chrome(service=service, options=options)
            except Exception as e:
                self.config.write_log(f"Erro iniciando o navegador Chrome: {e}", level=logging.ERROR)
                raise ValueError("Erro iniciando o navegador Chrome")
        else:
            self.config.write_log("Non hai user agent dispoñible.", level=logging.ERROR)
            raise ValueError("Non hai user agent dispoñible.")
        return id_navegador_db, browser
