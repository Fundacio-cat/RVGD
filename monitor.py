# -*- coding: utf-8 -*-

import logging
import sys
import argparse
from utils.config import Config
from utils.utils import nom_sensor
from navegadors.navegador_chrome import ChromeNavegador
from navegadors.navegador_firefox import FirefoxNavegador
from cercadors.cercador_google import GoogleCercador
from cercadors.cercador_bing import BingCercador
from repository.repository import Repository

def parseja_arguments():
    parser = argparse.ArgumentParser(description='Colle os parámetros do ficheiro json')
    parser.add_argument('-c', '--config', default='config.json', help='Ruta ao ficheiro de configuración. Por defecto é "config.json".')
    return parser.parse_args()

def inicia_base_dades(config: Config) -> Repository:
    try:
        repo = Repository(config)
        repo.connecta_bd()
        return repo
    except Exception as e:
        config.write_log(f"Erro na conexión a PostgreSQL: {e}", level=logging.ERROR)
        sys.exit(503)

def obtenir_sensor() -> str:
    sensor = nom_sensor()
    if not sensor:
        config.write_log("Non se puido obter o nome do sensor", level=logging.ERROR)
        sys.exit(1)
    return sensor

def crea_navegador(navegador: int, navegador_text: str, config: Config):

    # Retorna o navegador Chrome se 1
    if navegador == 1:
        return ChromeNavegador(config)

    # Retorna o navegador Firefox se 2
    elif navegador == 2:
        return FirefoxNavegador(config)

    # Se non está previsto, retorna un erro
    else:
        config.write_log(f"Erro: Non existe o navegador {navegador_text}", level=logging.ERROR)
        sys.exit(1)

def crea_cercador(cercador: int, cercador_text: str, config: Config):

    # Retorna Google se 1
    if cercador == 1:
        return GoogleCercador(config)

    # Retorna Bing se 2
    elif cercador == 2:
        return BingCercador(config)

    # Se non está previsto, retorna un erro
    else:
        config.write_log(f"Erro: Non existe o buscador {cercador_text}", level=logging.ERROR)
        sys.exit(1)

def executa_crawler(config: Config, cerca: str, id_cerca: int):
    try:
        resultats = config.cercador.guarda_resultats(cerca)
        logging.info(f"Gardando na base de datos os resultados para a busca {cerca}")
        for posicio, dades in resultats.items():
            logging.info(f"Gardando na base de datos a posición {posicio}, co sensor {config.sensor}")
            repo.guarda_bd(
                id_cerca,
                posicio,
                dades.get('titol', ''),
                dades.get('url', ''),
                dades.get('description', ''),
                False
            )
    except Exception as e:
        config.write_log(f"Erro na execución do crawler para a busca {cerca}: {e}", level=logging.ERROR)


if __name__ == "__main__":
    args = parseja_arguments()
    # Carga a configuración utilizando o ficheiro especificado ou o ficheiro por defecto
    config = Config.carrega_config(args.config)
    repo = inicia_base_dades(config)
    try:

        # Inicio do sensor
        sensor = obtenir_sensor()
        config.set_repository(repo) # BD
        config.set_sensor(sensor)
        config.write_log(f"Sensor {sensor} iniciado correctamente", level=logging.INFO)

        # Selecciona o navegador
        int_navegador = repo.selecciona_navegador()
        navegador_text = "Chrome" if int_navegador == 1 else "Firefox" if int_navegador == 2 else "Navegador desconegut"
        # Créao
        config.write_log(f"Creando o navegador {navegador_text} ...", level=logging.INFO)
        navegador = crea_navegador(int_navegador, navegador_text, config)
        config.set_navegador(navegador)
        config.write_log(f"Navegador {navegador_text} creado correctamente", level=logging.INFO)

        # Selecciona o buscador
        int_cercador = repo.selecciona_cercador()
        cercador_text = "Google" if int_cercador == 1 else "Bing" if int_cercador == 2 else "Navegador desconegut"
        # Crea'l
        config.write_log(f"Creando o buscador {cercador_text} ...", level=logging.INFO)
        cercador = crea_cercador(int_cercador, cercador_text, config)
        config.set_cercador(cercador)
        config.write_log(f"Buscador {cercador_text} creado correctamente", level=logging.INFO)

        id_cerca, cerca = repo.seguent_cerca(sensor)
        if cerca:
            config.write_log(f"Busca a executar: {cerca}", level=logging.INFO)
            executa_crawler(config, cerca, id_cerca)
        else:
            config.write_log("Non se obtivo ningunha busca", level=logging.WARNING)

    except Exception as e:
        config.write_log(f"Erro durante a execución: {e}", level=logging.ERROR)
        sys.exit(1)

    finally:
        # Intenta pechar o navegador e a conexión coa base de datos, independentemente de se houbo erros ou non.
        try:
            navegador.tanca_navegador()
        except Exception as e:
            config.write_log(f"Erro pechando o navegador: {e}", level=logging.ERROR)

        try:
            repo.close_connection()
        except Exception as e:
            config.write_log(f"Erro pechando a conexión coa BD: {e}", level=logging.ERROR)

        config.write_log("Crawler finalizado", level=logging.INFO)
        sys.exit(0)
