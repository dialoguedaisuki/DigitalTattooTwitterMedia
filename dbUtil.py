import psycopg2
import configparser


def get_connection(db_envName):
    config = configparser.ConfigParser()
    config.read('db_setting.ini')
    DB_HOST = config.get(db_envName, 'DB_HOST')
    DB_PORT = config.get(db_envName, 'DB_PORT')
    DB_NAME = config.get(db_envName, 'DB_NAME')
    DB_USER = config.get(db_envName, 'DB_USER')
    DB_PASS = config.get(db_envName, 'DB_PASS')
    return psycopg2.connect('postgresql://{user}:{password}@{host}:{port}/{dbname}'
                            .format(
                                user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT, dbname=DB_NAME
                            ))
