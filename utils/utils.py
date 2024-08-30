import socket
import os


def nome_sensor():
    """
    Devolve o nome do host do sistema operativo.
    Esta función foi modificada para ser compatible tanto con Linux como con Windows.

    Returns:
    - string: Os primeiros 5 caracteres do nome do host. Se hai un erro, devolve None.
    """
    try:
        # Obtén o nome completo do host utilizando a biblioteca socket.
        # Este método é multiplataforma e funciona tanto en Linux como en Windows.
        hostname = socket.gethostname()

        # Colle os primeiros 5 caracteres do nome do host.
        sensor = hostname[:5]
        return sensor
    except Exception as e:
        # Registra o erro se se produce algún problema ao obter o nome do host.
        print(f"Erro obtendo o nome do sensor: {e}")
        return None


def asegura_directorio_existe(directorio):
    """
    Crea un directorio se non existe.

    Argumentos:
    - directorio (str): O directorio que se quere crear.
    """
    if not os.path.exists(directorio):
        os.makedirs(directorio)
