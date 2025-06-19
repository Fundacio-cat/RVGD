import os
import logging
from buscadores.buscador_base import BuscadorBase
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from datetime import datetime
import logging
from utils.selenium_helpers import busca_datos
from utils.utils import asegura_directorio_existe
from time import sleep

from os.path import sep
from datetime import datetime
from os import remove


class GoogleBuscador(BuscadorBase):

    def inicia_buscador(self):
        id_buscador_db = 1
        try:
            aceptado = False
            self.browser.get('https://www.google.com')
            buttons = self.browser.find_elements(By.XPATH, '//button')
            for button in buttons:
                try:
                    # Google Cookies
                    if button.find_element(By.XPATH, './/div[contains(text(), "Aceptar todo")]'):
                        button.click()
                        aceptado = True
                        break
                except NoSuchElementException:
                    pass
            if not aceptado:
                self.config.write_log("Non se puideron aceptar as cookies de Google", level=logging.ERROR)
                raise ValueError("Non se puideron aceptar as cookies de Google")
        except Exception as e:
            try:
                browser_version = self.browser.capabilities['browserVersion']
                driver_version = self.browser.capabilities['chrome']['chromedriverVersion'].split(' ')[0]
                error_message = f"Erro iniciando o buscador: " \
                                f"Versión do navegador Chrome: {browser_version}\n" \
                                f"Versión do ChromeDriver: {driver_version}"
            except WebDriverException:
                error_message = f"Erro iniciando o buscador: {e}\n" \
                                "Non se puido obter a información da versión do navegador ou do controlador."

            self.config.write_log(error_message, level=logging.ERROR)
            raise ValueError(error_message) from e

        return id_buscador_db

    def compon_nome_captura(self, busca, navegador_text, suffix=None):
        current_directory = self.config.current_directory
        busca_sen_espazos = busca.replace(' ', '_')
        data_hora_actual = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        nome_base = f"{current_directory}{sep}{self.config.directorio_Imaxes}{sep}{self.config.sensor}_{navegador_text}_Google_{busca_sen_espazos}_{data_hora_actual}"
        if suffix:
            nome_captura = f"{nome_base}_{suffix}.png"
        else:
            nome_captura = f"{nome_base}.png"

        asegura_directorio_existe(os.path.dirname(nome_captura))
        return nome_captura

    def garda_resultados(self, busca, navegador_text):
        navegador = self.config.navegador
        browser = self.browser

        resultados = {}
        resultados_gardados = 1
        intents = 0
        max_intents = 3

        sleep(self.config.tempo_espera_procesos)
        try:
            textarea = self.browser.find_element(By.TAG_NAME, value='textarea')
            # Selecciona todo o texto do textarea
            # En Mac, usa Keys.COMMAND en vez de Keys.CONTROL
            textarea.send_keys(Keys.CONTROL, 'a')
            # Elimina o posible contido e introduce a busca
            textarea.send_keys(Keys.DELETE)
            textarea.send_keys(busca + Keys.ENTER)
        except:
            raise ValueError("Non se puido realizar a busca")

        while resultados_gardados <= 10:
            sleep(self.config.tempo_espera_procesos)

            nome_captura_1 = self.compon_nome_captura(busca, navegador_text)
            nome_captura_2 = self.compon_nome_captura(busca, navegador_text, suffix="2a")

            navegador.captura_pantalla(nome_captura_1)
            resultados_busca = browser.find_elements(By.XPATH, '//a[h3]')

            for resultado in resultados_busca:
                if resultados_gardados < 11:
                    link, titulo, description = busca_datos(resultado)

                    if titulo == "Máis resultados":
                        logging.info(f"Obtemos a segunda páxina de {busca}...")
                        browser.get(link)
                        sleep(self.config.tempo_espera_procesos)
                        navegador.captura_pantalla(nome_captura_2)
                        a_elements_with_h3 = browser.find_elements(By.XPATH, '//a[h3]')

                        for a in a_elements_with_h3:
                            if resultados_gardados < 11:
                                link, titulo, description = busca_datos(a)

                                if link is not None:
                                    resultados[resultados_gardados] = {
                                        'titulo': titulo, 'url': link, 'description': description}
                                    resultados_gardados += 1

                            else:
                                logging.info(f"Colleitéronse os 10 resultados da segunda páxina de {busca}...")
                                browser.execute_script("window.history.go(-1)")
                                sleep(self.config.tempo_espera_procesos)
                                break

                    else:
                        if link is not None:
                            resultados[resultados_gardados] = {
                                'titulo': titulo, 'url': link, 'description': description}
                            resultados_gardados += 1

            if resultados_gardados < 11:
                try:
                    browser.find_elements(By.XPATH, '//a[@aria-label=\'Page 2\']')[0].click()
                    sleep(self.config.tempo_espera_procesos)
                    navegador.captura_pantalla(nome_captura_2)
                    a_elements_with_h3 = browser.find_elements(By.XPATH, '//a[h3]')

                    for a in a_elements_with_h3:
                        if resultados_gardados < 11:
                            link, titulo, description = busca_datos(a)

                            if link is not None:
                                resultados[resultados_gardados] = {
                                    'titulo': titulo, 'url': link, 'description': description}
                                resultados_gardados += 1
                        else:
                            browser.execute_script("window.history.go(-1)")
                            sleep(self.config.tempo_espera_procesos)
                            break
                except:
                    sleep(self.config.tempo_espera_buscadores)
                    logging.error(f"Non se puido realizar a petición da segunda páxina de {busca}")

            logging.info(f"Valorando os resultados de {busca}...")

            if resultados_gardados < 11:
                intents += 1
                logging.info(f"Non se obtiveron os 10 resultados de {busca}... (Intent {intents}/{max_intents})")
                remove(nome_captura_1)

                try:
                    remove(nome_captura_2)
                except:
                    pass

                if intents >= max_intents:
                    error_msg = f"Non se puideron obter os 10 resultados de {busca} després de {max_intents} intents. Tancando o programa."
                    logging.error(error_msg)
                    self.config.write_log(error_msg, level=logging.ERROR)
                    raise ValueError(error_msg)

                resultados_gardados = 1
                resultados = {}
                browser.get('https://google.com')
                sleep(self.config.tempo_espera_buscadores)
                textarea = browser.find_element(By.TAG_NAME, value='textarea')
                textarea.send_keys(busca + Keys.ENTER)
                sleep(self.config.tempo_espera_procesos)
                logging.info(f"Volve a realizar a busca (Intent {intents + 1})")

            else:
                return resultados
