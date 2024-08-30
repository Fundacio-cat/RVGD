# -*- coding: utf-8 -*-

from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup


# Define se un título h3 está dentro dun módulo de "Máis preguntas"
def h3_modulo_preguntas(h3):

    try:
        div_preguntas = h3.find_element(By.XPATH, './parent::span/parent::div/parent::div/parent::div/parent::div/parent::div/parent::div/parent::div/parent::div/parent::div/parent::div/parent::div/parent::div/parent::div/parent::div/parent::div/parent::div')
        div_mais_preguntas = div_preguntas.find_element(By.XPATH, './div/div[1]/div/div')
        mais_preguntas = div_mais_preguntas.find_element(By.XPATH, './/span')
        if "preguntas" in mais_preguntas.text.lower():
            e_pregunta = True
        else:
            e_pregunta = False

    # Non está dentro dun contedor de Máis preguntas
    except:
        mais_preguntas = None
        e_pregunta = False

    return mais_preguntas, e_pregunta

# Colle os datos das respostas e devolveos en formato diccionario
def busca_datos(elemento_buscar):

    link = None
    titulo = None
    description = None

    mais_preguntas, e_pregunta = h3_modulo_preguntas(elemento_buscar)

    if not e_pregunta:

        # Gardamos as URL e os títulos
        link = elemento_buscar.get_attribute('href')
        html = elemento_buscar.get_attribute("innerHTML")
        soup = BeautifulSoup(html, 'html.parser')
        titulo = soup.find('h3').text

        # Description
        try:

            # Accede tres veces ao elemento pai
            div_pai = elemento_buscar.find_element(By.XPATH, './parent::span/parent::div/parent::div/parent::div/parent::div/parent::div')

            # A ligazón non ten imaxe. A descrición está no 2º div
            try:
                div_description = div_pai.find_element(By.XPATH, './div/div[2]')
                spans = div_description.find_elements(By.XPATH, './/span')
                description = spans[len(spans)-1].text

            # A ligazón ten unha imaxe. A descrición está no 3º div
            except:
                div_description = div_pai.find_element(By.XPATH, './div/div[3]')
                spans = div_description.find_elements(By.XPATH, './/span')
                description = spans[len(spans)-1].text

        except:
            try:
                # Outro acceso ás descricións
                div_pai = elemento_buscar.find_element(By.XPATH, './parent::span/parent::div/parent::div/parent::div/parent::div')
                div_description = div_pai.find_element(By.XPATH, './div[3]')
                description = div_description.text

                if description == '':
                    div_description = div_pai.find_element(By.XPATH, './div[2]')
                    description = div_description.text

            except:
                if mais_preguntas is not None:
                    description = mais_preguntas.text
                else:
                    description = None


    return [link, titulo, description]
