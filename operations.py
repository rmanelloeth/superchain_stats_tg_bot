import config
import psycopg2

def get_user_ids():
    try:
        connection = psycopg2.connect(
            host=config.host,
            user=config.user_name,
            password=config.password,
            database=config.database_name)
        connection.autocommit = True

        with connection.cursor() as cursor:
            cursor.execute(
                """SELECT user_id FROM all_users;"""
            )
            rows = cursor.fetchall()
            user_ids = [row[0] for row in rows]
            # print(user_ids)
            return user_ids
    except Exception as e:
        print(f'Error to connect DB: {e}')
    finally:
        if connection:
            connection.close()
            # print(f'connection closed')

def add_new_user(id: str, username: str):
    try:
        connection = psycopg2.connect(
            host=config.host,
            user=config.user_name,
            password=config.password,
            database=config.database_name)
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute("""INSERT INTO all_users VALUES (%s, %s)""", (id, username))
            print(f'Добавил {username} в all_users  ')
    except Exception as e:
        print(f'Error to connect DB: {e}')
    finally:
        if connection:
            connection.close()
            # print(f'connection closed')

def get_user_wallets(id: str):
    try:
        connection = psycopg2.connect(
            host=config.host,
            user=config.user_name,
            password=config.password,
            database=config.database_name)
        connection.autocommit = True

        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM wallets WHERE user_id = '{id}';")
            rows = cursor.fetchall()
            wallets = [row[1] for row in rows]
            labels = [row[2] for row in rows]
            # print(wallets)
            return wallets, labels
    except Exception as e:
        print(f'Error to connect DB: {e}')
    finally:
        if connection:
            connection.close()
            # print(f'connection closed')

def add_new_wallet(id: str, wallet: str, label: str):
    try:
        connection = psycopg2.connect(
            host=config.host,
            user=config.user_name,
            password=config.password,
            database=config.database_name)
        connection.autocommit = True
        with connection.cursor() as cursor:
            wallets,_ = get_user_wallets(id)
            if wallet not in wallets:
                cursor.execute("""INSERT INTO wallets VALUES (%s, %s, %s)""", (id, wallet, f'wallet {label}'))
                return False
            else:
                return True
    except Exception as e:
        print(f'Error to connect DB: {e}')
    finally:
        if connection:
            connection.close()
            # print(f'connection closed')

# add_new_user('rmanello','dsadsd')
# get_user_wallets(str(2))
# add_new_wallet('2','0x75c6648796FE7fad760219816f4fBeC8065007ee','3')
