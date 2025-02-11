from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from navegadores.navegador_base import NavegadorBase
import os
import logging


class FirefoxNavegador(NavegadorBase):

    def init_navegador(self):
        browser = None
        id_navegador_db = 2
        user_agent = self.repository.busca_userAgent(id_navegador_db)

        if user_agent:
            options = Options()
            options.add_argument(f"user-agent={user_agent}")
            options.set_preference('intl.accept_languages', 'gl')
            driver_path = os.path.join(self.config.current_directory, "Controladores", self.config.FIREFOX_DRIVER_PATH)
            service = Service(driver_path)
            try:
                browser = webdriver.Firefox(service=service, options=options)
                browser.set_window_size(self.anchura, self.altura)
            except Exception as e:
                self.config.write_log(f"Erro iniciando o navegador Firefox: {e}", level=logging.ERROR)
                raise ValueError("Erro iniciando o navegador Firefox")
        else:
            self.config.write_log("Non hai user agent dispoñible.", level=logging.ERROR)
            raise ValueError("Non hai user agent dispoñible.")
        return id_navegador_db, browser
