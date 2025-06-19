import json
import os
import logging
import inspect
from dataclasses import dataclass, fields


@dataclass
class Config:
    CHROME_DRIVER_PATH: str
    FIREFOX_DRIVER_PATH: str
    tempo_espera_procesos: int
    tempo_espera_buscadores: int
    numero_de_buscas_por_execucion: int
    ficheiro_logs: str
    directorio_Imaxes: str
    nivel_logging: str
    host: str = None
    port: str = None
    database: str = None
    user: str = None
    password: str = None
    repository = None
    sensor = None
    navegador = None
    buscador = None

    def __post_init__(self):
        self.configure_logging()
        self.current_directory = os.getcwd()

    def configure_logging(self):
        """Configura o logging cos parámetros desexados."""
        level = getattr(logging, self.nivel_logging.upper(), None)
        if not isinstance(level, int):
            raise ValueError(f'Nivel de logging inválido: {self.nivel_logging}')
        logging.basicConfig(filename=self.ficheiro_logs, level=level, format=self.define_format(), encoding='utf-8')

    @staticmethod
    def define_format():
        """Define e devolve o formato de log desexado."""
        return "%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)d] - %(message)s"

    def write_log(self, message, level=logging.ERROR):
        """
        Escribe un mensaxe de log cun determinado nivel.

        Argumentos:
        - message (str): O mensaxe que se quere escribir no log.
        - level (int): O nivel de log (por exemplo: logging.ERROR, logging.INFO, ...). Por defecto é logging.ERROR.
        """
        caller_frame = inspect.currentframe().f_back
        caller_file = caller_frame.f_code.co_filename
        caller_line = caller_frame.f_lineno
        caller_function = caller_frame.f_code.co_name

        detailed_message = f"{message} (Chamada desde {caller_file} liña {caller_line} función {caller_function})"
        logger = logging.getLogger()
        getattr(logger, logging.getLevelName(level).lower())(detailed_message)

    @classmethod
    def carrega_config(cls, config_json):
        """Carga a configuración desde un ficheiro JSON."""
        config_path = os.path.join(os.getcwd(), config_json)
        try:
            with open(config_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            cls.validate_keys(data)
            return cls(**data)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            raise ValueError(f"Erro co ficheiro '{config_json}': {e}")

    @classmethod
    def validate_keys(cls, data):
        """Valida que todas as chaves requiridas estean presentes."""
        required_keys = {field.name for field in fields(cls)}
        missing_keys = required_keys - set(data.keys())
        if missing_keys:
            raise ValueError(f"Ficheiro de configuración incompleto. Faltan as seguintes chaves: {', '.join(missing_keys)}")

    def set_repository(self, repository):
        """Establece o repositorio para a configuración."""
        self.repository = repository

    def set_sensor(self, sensor):
        """Establece o sensor para a configuración."""
        self.sensor = sensor

    def set_navegador(self, navegador):
        """Establece o navegador para a configuración."""
        self.navegador = navegador

    def set_buscador(self, buscador):
        """Establece o buscador para a configuración."""
        self.buscador = buscador