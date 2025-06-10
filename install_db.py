"""Перед установкой бота запускаем все эти функции по порядку, поменяв в конфиге данные пользователя"""
import config
import psycopg2

def create_table_all_users():
    try:
        connection = psycopg2.connect(
            host=config.host,
            user=config.user_name,
            password=config.password,
            database=config.database_name)
        connection.autocommit = True

        with connection.cursor() as cursor:
            cursor.execute(
                """CREATE TABLE all_users (
                  user_id varchar(20) PRIMARY KEY ,
                  nickname varchar(100)
                  );"""
            )
            print(f'Таблица Пользователей создана')
    except Exception as e:
        print(f'Error to connect DB: {e}')
    finally:
        if connection:
            connection.close()
            print(f'connection closed')


def create_stats_table():
    try:
        connection = psycopg2.connect(
            host=config.host,
            user=config.user_name,
            password=config.password,
            database=config.database_name)
        connection.autocommit = True

        with connection.cursor() as cursor:
            cursor.execute(
                """CREATE TABLE stats (
                  user_id varchar(25),
                  wallet varchar(50) PRIMARY KEY,
                  OPTIMISM varchar(100),
                  BASE varchar(100),
                  INK varchar(100),
                  SONEIUM varchar(100),
                  LISK varchar(100),
                  UNICHAIN varchar(100)
                  );"""
            )
            print(f'Таблица Пользователей создана')
    except Exception as e:
        print(f'Error to connect DB: {e}')
    finally:
        if connection:
            connection.close()
            print(f'connection closed')

def create_table_wallets():
    try:
        connection = psycopg2.connect(
            host=config.host,
            user=config.user_name,
            password=config.password,
            database=config.database_name)
        connection.autocommit = True

        with connection.cursor() as cursor:
            cursor.execute(
                """CREATE TABLE wallets (
                  user_id varchar(25),
                  wallet varchar(100),
                  label varchar(15)
                  );"""
            )
            print(f'Таблица Wallets')
    except Exception as e:
        print(f'Error to connect DB: {e}')
    finally:
        if connection:
            connection.close()
            print(f'connection closed')

def create_state_machine():
    try:
        connection = psycopg2.connect(
            host=config.host,
            user=config.user_name,
            password=config.password,
            database=config.database_name)
        connection.autocommit = True

        with connection.cursor() as cursor:
            cursor.execute(
                """CREATE TABLE state_machine (
                  user_id varchar(20) PRIMARY KEY ,
                  state varchar(200),
                  user_number integer
                  );"""
            )
            print(f'Таблица машины состояний создана')
    except Exception as e:
        print(f'Error to connect DB: {e}')
    finally:
        if connection:
            connection.close()
            print(f'connection closed')


create_stats_table()

