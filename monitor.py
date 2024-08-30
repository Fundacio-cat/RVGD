# -*- coding: utf-8 -*-

import logging
import sys
import argparse
from utils.config import Config
from utils.utils import nome_sensor
from navegadores.navegador_chrome import ChromeNavegador
from navegadores.navegador_firefox import FirefoxNavegador
from buscadores.buscador_google import GoogleBuscador
from repository.repository import Repository

def valora_os_argumentos():
    parser = argparse.ArgumentParser(description='Colle os parámetros do ficheiro json')
    parser.add_argument('-c', '--config', default='config.json', help='Ruta ao ficheiro de configuración. Por defecto é "config.json".')
    return parser.parse_args()

def inicia_base_datos(config: Config) -> Repository:
    try:
        repo = Repository(config)
        repo.conecta_bd()
        return repo
    except Exception as e:
        config.write_log(f"Erro na conexión a PostgreSQL: {e}", level=logging.ERROR)
        sys.exit(503)

def obter_sensor() -> str:
    sensor = nome_sensor()
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

def crea_buscador(buscador: int, buscador_text: str, config: Config):

    # Retorna Google se 1
    if buscador == 1:
        return GoogleBuscador(config)

    # Se non está previsto, retorna un erro
    else:
        config.write_log(f"Erro: Non existe o buscador {buscador_text}", level=logging.ERROR)
        sys.exit(1)

def executa_crawler(config: Config, busca: str, id_busca: int):
    try:
        resultats = config.buscador.garda_resultados(busca)
        logging.info(f"Gardando na base de datos os resultados para a busca {busca}")
        for posicion, datos in resultats.items():
            logging.info(f"Gardando na base de datos a posición {posicion}, co sensor {config.sensor}")
            repo.garda_bd(
                id_busca,
                posicion,
                datos.get('titol', ''),
                datos.get('url', ''),
                datos.get('description', ''),
                False
            )
    except Exception as e:
        config.write_log(f"Erro na execución do crawler para a busca {busca}: {e}", level=logging.ERROR)


if __name__ == "__main__":
    args = valora_os_argumentos()
    # Carga a configuración utilizando o ficheiro especificado ou o ficheiro por defecto
    config = Config.carrega_config(args.config)
    repo = inicia_base_datos(config)
    try:

        # Inicio do sensor
        sensor = obter_sensor()
        config.set_repository(repo) # BD
        config.set_sensor(sensor)
        config.write_log(f"Sensor {sensor} iniciado correctamente", level=logging.INFO)

        # Selecciona o navegador
        int_navegador = repo.selecciona_navegador()
        navegador_text = "Chrome" if int_navegador == 1 else "Firefox" if int_navegador == 2 else "Navegador descoñecido"
        # Créao
        config.write_log(f"Creando o navegador {navegador_text} ...", level=logging.INFO)
        navegador = crea_navegador(int_navegador, navegador_text, config)
        config.set_navegador(navegador)
        config.write_log(f"Navegador {navegador_text} creado correctamente", level=logging.INFO)

        # Selecciona o buscador
        int_buscador = repo.selecciona_buscador()
        buscador_text = "Google" if int_buscador == 1 else "Bing" if int_buscador == 2 else "Buscador descoñecido"
        # Créao
        config.write_log(f"Creando o buscador {buscador_text} ...", level=logging.INFO)
        buscador = crea_buscador(int_buscador, buscador_text, config)
        config.set_buscador(buscador)
        config.write_log(f"Buscador {buscador_text} creado correctamente", level=logging.INFO)

        id_busca, busca = repo.seguinte_busca(sensor)
        if busca:
            config.write_log(f"Busca a executar: {busca}", level=logging.INFO)
            executa_crawler(config, busca, id_busca)
        else:
            config.write_log("Non se obtivo ningunha busca", level=logging.WARNING)

    except Exception as e:
        config.write_log(f"Erro durante a execución: {e}", level=logging.ERROR)
        sys.exit(1)

    finally:
        # Intenta pechar o navegador e a conexión coa base de datos, independentemente de se houbo erros ou non.
        try:
            navegador.pecha_navegador()
        except Exception as e:
            config.write_log(f"Erro pechando o navegador: {e}", level=logging.ERROR)

        try:
            repo.close_connection()
        except Exception as e:
            config.write_log(f"Erro pechando a conexión coa BD: {e}", level=logging.ERROR)

        config.write_log("Crawler finalizado", level=logging.INFO)
        sys.exit(0)
