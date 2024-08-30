# -*- coding: utf-8 -*-

import psycopg2
import logging
from datetime import datetime
from utils.config import Config


class Repository:
    def __init__(self, config: Config):
        self.config = config
        self.conn = None
        self.cursor = None

    def conecta_bd(self):
        try:
            # Obter as credenciais da configuración
            host = self.config.host
            port = self.config.port
            database = self.config.database
            user = self.config.user
            password = self.config.password

            configuracion = {
                'host': host,
                'port': port,
                'database': database,
                'user': user,
                'password': password,
            }

            # Conectar á BD
            self.conn = psycopg2.connect(**configuracion)
            self.cursor = self.conn.cursor()

        except Exception as e:
            self.config.write_log(f"Erro na conexión a PostgreSQL: {e}", level=logging.ERROR)
            raise ValueError(f"Erro na conexión a PostgreSQL: {e}")

    def garda_bd(self, int_busca, posicion, titulo, url, description, noticia):
        try:
            now = datetime.now()
            if titulo is not None:
                titulo = titulo.replace("'", "''")

            if description is not None:
                description = description.replace("'", "''")

            insert_query = "INSERT INTO resultats (sensor, hora, navegador, cercador, cerca, posicio, titol, url, descripcio, noticia) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            values = (self.config.sensor, now, self.config.navegador.id_navegador_db, self.config.buscador.id_buscador_db, int_busca, posicion, titulo, url, description, noticia)

            self.cursor.execute(insert_query, values)
            self.conn.commit()
        except psycopg2.Error as db_error:
            self.config.write_log(f"Erro na conexión a PostgreSQL: {db_error}", level=logging.ERROR)

    def mock_garda_bd(self, int_busca, posicion, titulo, url, description, noticia):
        try:
            now = datetime.now()
            if titulo is not None:
                titulo = titulo.replace("'", "''")

            if description is not None:
                description = description.replace("'", "''")

            insert_query = "INSERT INTO resultats (sensor, hora, navegador, cercador, cerca, posicio, titol, url, descripcio, noticia) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            values = (self.config.sensor, now, self.config.navegador.id_navegador_db, self.config.buscador.id_buscador_db, int_busca, posicion, titulo, url, description, noticia)

            # self.cursor.execute(insert_query, values)
            # self.conn.commit()
            print(insert_query % values)

        except psycopg2.Error as db_error:
            self.config.write_log(f"Erro na conexión a PostgreSQL: {db_error}", level=logging.ERROR)

    def busca_userAgent(self, navegador):
        try:
            select_query = f"SELECT useragent FROM navegadors WHERE navId = {navegador};"
            self.cursor.execute(select_query)
            resultado = self.cursor.fetchone()
            if resultado:
                useragent = str(resultado[0])
                return useragent
            else:
                return None
        except psycopg2.Error as db_error:
            self.config.write_log(f"Erro na conexión a PostgreSQL: {db_error}", level=logging.ERROR)
            return None

    def seguinte_busca(self, sensor):
        try:
            # Executar a instrución SQL para obter o ID da seguinte busca
            select_integral = "SELECT seguent_cerca_filtrada('{}');".format(sensor)
            self.cursor.execute(select_integral)
            int_busca = self.cursor.fetchone()[0]

            # Executar a instrución SQL para obter a consulta str da busca
            select_busca = "SELECT consulta FROM cerques WHERE cerqId = {};".format(int_busca)
            self.cursor.execute(select_busca)
            busca = self.cursor.fetchone()[0]
            return int_busca, busca
        except psycopg2.Error as db_error:
            self.config.write_log(f"Erro na conexión a PostgreSQL: {db_error}", level=logging.ERROR)
            return None, None
        
    def selecciona_medidas(self):
        try:
            # Executar a instrución SQL para obter o ID da seguinte busca
            select_medidas = "SELECT selecciona_mides();"
            self.cursor.execute(select_medidas)
            int_medida = self.cursor.fetchone()[0]

            select_anchura = f"SELECT amplada FROM mides WHERE midaid = {int_medida};"
            self.cursor.execute(select_anchura)
            anchura = self.cursor.fetchone()[0]

            select_altura = f"SELECT altura FROM mides WHERE midaid = {int_medida};"
            self.cursor.execute(select_altura)
            altura = self.cursor.fetchone()[0]

            return int_medida, anchura, altura

        except psycopg2.Error as db_error:
            self.config.write_log(f"Erro na conexión a PostgreSQL: {db_error}", level=logging.ERROR)
            return None, None

    def selecciona_navegador(self):
        try:
            # Executar a instrución SQL para obter o ID da seguinte busca
            select_navegador = "SELECT selecciona_navegador();"
            self.cursor.execute(select_navegador)
            int_navegador = self.cursor.fetchone()[0]

            return int_navegador

        except psycopg2.Error as db_error:
            self.config.write_log(f"Erro na conexión a PostgreSQL: {db_error}", level=logging.ERROR)
            return None, None
        
    def selecciona_buscador(self):
        try:
            # Executar a instrución SQL para obter o ID da seguinte busca
            select_buscador = "SELECT selecciona_cercador();"
            self.cursor.execute(select_buscador)
            int_buscador = self.cursor.fetchone()[0]

            return int_buscador

        except psycopg2.Error as db_error:
            self.config.write_log(f"Erro na conexión a PostgreSQL: {db_error}", level=logging.ERROR)
            return None, None

    def close_connection(self):
        if self.conn is not None:
            self.conn.close()
