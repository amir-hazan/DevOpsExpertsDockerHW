import itertools
import time
import pymysql
import names
import socket
from pypika import Column, Query, Table, Schema
from prettytable import PrettyTable


def wait_for_db(host, port):
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((host, port))
            return True
        except socket.error:
            time.sleep(1)


def get_date_time():
    dt_for_db = time.strftime('%Y-%m-%d %H:%M:%S')
    return dt_for_db


def db_connector():
    if wait_for_db('database', 3306) is True:
        try:
            schema_name = "DevOpsExpertsDB"

            conn = pymysql.connect(
                host='database',
                port=3306,
                user='amir',
                passwd='e%RP9331',
                db=schema_name
            )

        except pymysql.err.OperationalError as operationalErr:
            print(operationalErr)
        finally:
            # Getting a cursor from Database
            cursor = conn.cursor()
            return cursor, conn


def check_if_table_exist():
    cursor, conn = db_connector()

    cursor = conn.cursor()
    statement_to_exec = "SHOW TABLES"

    try:
        cursor.execute(statement_to_exec)

        table_list = []
        for tables in cursor.fetchall():
            table_list.append(tables)

        if not table_list and 'users' not in table_list:
            print('no table was found')
            return False

    except pymysql.OperationalError as err:
        print(err)

    finally:
        conn.close()
        cursor.close()

    return True


def create_users_table():
    if check_if_table_exist() is False:
        cursor, conn = db_connector()

        # PyPika CREATE
        create_users_tbl = Query \
            .create_table('users') \
            .columns(
                Column('user_id', "integer auto_increment", nullable=False),
                Column('user_name', "VARCHAR(50)", nullable=False),
                Column('date_created', "DATETIME", nullable=False)) \
            .primary_key('user_id')

        create_users_tbl = create_users_tbl.get_sql()
        create_users_tbl = create_users_tbl.replace('"', '')

        try:
            cursor.execute(create_users_tbl)
            conn.commit()
            print("table: users created successfully\n")
        except pymysql.err.OperationalError as pyExistErr:
            print("Error:", pyExistErr)
        finally:
            cursor.close()
            conn.close()

    return True


def get_next_available_user_id():
    if create_users_table() is True:
        cursor, conn = db_connector()

        # PyPika SELECT
        schema = Schema('DevOpsExpertsDB')
        users = Table('users')
        get_all_users_ids = Query.from_(schema.users).select(
            users.user_id
        )

        get_all_users_ids = get_all_users_ids.get_sql()
        get_all_users_ids = get_all_users_ids.replace('"', '')  # Removing apostrophes from relevant strings

        cursor.execute(get_all_users_ids)
        conn.commit()

        users_ids = []

        for ids in cursor:
            users_ids.append(ids)

        users_ids = list(itertools.chain(*users_ids))
        # print(users_ids)

        try:
            if not users_ids:
                next_user_id = 1
            else:
                next_user_id = sorted(set(range(1, users_ids[-1])) - set(users_ids))
                # print(missing_user_id)
                if not next_user_id:
                    next_user_id = max(users_ids) + 1
                    # print(next_user_id)
                else:
                    next_user_id = min(next_user_id)

        except ValueError as val:
            print(val)
        except UnboundLocalError as localErr:
            print(localErr)
        finally:
            cursor.close()
            conn.close()

        return next_user_id


def create_random_users():
    # print(get_next_available_user_id())
    max_users_to_create = get_next_available_user_id() + 10

    cursor, conn = db_connector()

    for i in range(get_next_available_user_id(), max_users_to_create):
        user_id = get_next_available_user_id()
        user_name = names.get_first_name()
        datetime = get_date_time()

        schema = Schema('DevOpsExpertsDB')
        insert_random_user = Query.into(schema.users).insert(
            user_id,
            user_name,
            datetime
        )

        insert_random_user = insert_random_user.get_sql()  # get Query as SQL
        insert_random_user = insert_random_user.replace('"', '')  # Removing apostrophes from relevant strings

        try:
            cursor.execute(insert_random_user)
            conn.commit()
        except pymysql.err.InternalError as inErr:
            print(inErr)

    conn.close()
    cursor.close()

    return True


def print_users_table():
    if create_random_users() is True:
        cursor, conn = db_connector()

        schem = Schema('DevOpsExpertsDB')
        select_all_from_db = Query.from_(schem.users).select('*')

        select_all_from_db = select_all_from_db.get_sql()
        select_all_from_db = select_all_from_db.replace('"', '')

        cursor.execute(select_all_from_db)

        result = cursor.fetchall()
        users_tbl = PrettyTable(
            [
                'user id',
                'username',
                'creation date'
            ]
        )

        users_tbl.hrules = 1
        users_tbl.vrules = 1

        for row in result:
            r = (row[0], row[1], row[2])
            users_tbl.add_row(r)

        print("\n", users_tbl, "\n")


print_users_table()
