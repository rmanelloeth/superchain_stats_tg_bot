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

def get_wallet_stat(wallet: str):
    try:
        connection = psycopg2.connect(
            host=config.host,
            user=config.user_name,
            password=config.password,
            database=config.database_name)
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM stats WHERE wallet = '{wallet}';")
            rows = cursor.fetchall()
            # print(rows)
            return rows
    except Exception as e:
        print(f'Error to connect DB: {e}')
    finally:
        if connection:
            connection.close()
            # print(f'connection closed')

def update_stat(user_id: str, wallet: str, results: dict):
    try:
        connection = psycopg2.connect(
            host=config.host,
            user=config.user_name,
            password=config.password,
            database=config.database_name
        )
        connection.autocommit = True

        with connection.cursor() as cursor:
            # Жестко заданный порядок колонок
            known_columns = ['optimism', 'base', 'ink', 'soneium', 'lisk', 'unichain']
            valid_items = {}

            for chain in known_columns:
                value = results.get(chain.upper())
                try:
                    if isinstance(value, (int, float)):
                        valid_items[chain] = value
                    elif isinstance(value, str):
                        # Пробуем привести строку к числу
                        num = float(value)
                        valid_items[chain] = int(num) if num.is_integer() else num
                except (ValueError, TypeError):
                    continue  # Пропускаем невалидное

            # Проверим, есть ли запись по этому кошельку
            cursor.execute("SELECT * FROM stats WHERE wallet = %s AND user_id = %s", (wallet, user_id))
            existing = cursor.fetchone()

            columns = ['user_id', 'wallet']
            values = [user_id, wallet]
            # print(values)

            for col in known_columns:
                if col in valid_items:
                    columns.append(col)
                    values.append(valid_items[col])
                else:
                    if existing:
                        continue  # Не обновляем — оставим как было
                    else:
                        columns.append(col)
                        values.append('-')  # Новый кошелек — ставим прочерк

            if len(columns) == 2:
                print("Нет новых данных для обновления.")
                return

            placeholders = ', '.join(['%s'] * len(values))
            columns_str = ', '.join(columns)
            update_str = ', '.join([f"{col} = EXCLUDED.{col}" for col in columns[2:]])

            sql = f"""
                INSERT INTO stats ({columns_str})
                VALUES ({placeholders})
                ON CONFLICT (wallet) DO UPDATE SET {update_str};
            """

            cursor.execute(sql, values)

    except Exception as e:
        print(f"Ошибка при обновлении статистики: {e}")
    finally:
        if connection:
            connection.close()

def delete_wallet(wallet: str, id: str):
    try:
        connection = psycopg2.connect(
            host=config.host,
            user=config.user_name,
            password=config.password,
            database=config.database_name)
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM stats WHERE wallet = %s AND user_id = %s;",
                (wallet, id)
            )
            cursor.execute(
                "DELETE FROM wallets WHERE wallet = %s AND user_id = %s;",
                (wallet, id)
            )
    except Exception as e:
        print(f'Error to connect DB: {e}')
    finally:
        if connection:
            connection.close()
            # print(f'connection closed')

def delete_wallet(wallet: str, id: str):
    try:
        connection = psycopg2.connect(
            host=config.host,
            user=config.user_name,
            password=config.password,
            database=config.database_name)
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM stats WHERE wallet = %s AND user_id = %s;",
                (wallet, id)
            )
            cursor.execute(
                "DELETE FROM wallets WHERE wallet = %s AND user_id = %s;",
                (wallet, id)
            )
    except Exception as e:
        print(f'Error to connect DB: {e}')
    finally:
        if connection:
            connection.close()

