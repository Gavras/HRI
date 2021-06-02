import Utility.DBConnector as Connector

from Utility.Exceptions import DatabaseException
from Utility.DBConnector import ResultSet
from psycopg2 import sql


def dropTable() -> None:
    conn = None
    try:
        conn = Connector.DBConnector()
        conn.execute("DROP TABLE IF EXISTS Users CASCADE")
        conn.commit()
    except DatabaseException.ConnectionInvalid as e:

        print(e)
    except DatabaseException.NOT_NULL_VIOLATION as e:

        print(e)
    except DatabaseException.CHECK_VIOLATION as e:

        print(e)
    except DatabaseException.UNIQUE_VIOLATION as e:

        print(e)
    except DatabaseException.FOREIGN_KEY_VIOLATION as e:

        print(e)
    except Exception as e:
        print(e)
    finally:

        conn.close()


def createTable() -> None:
    conn = None
    conn = Connector.DBConnector()
    try:
        conn = Connector.DBConnector()
        action ="CREATE TABLE Users(id INTEGER , name TEXT NOT NULL,question_number INTEGER NOT NULL,answer TEXT NOT NULL,date_time TIMESTAMPTZ DEFAULT Now() ); " \

        conn.execute(action)
        conn.commit()
    except DatabaseException.ConnectionInvalid as e:
        print(e)
    except DatabaseException.NOT_NULL_VIOLATION as e:
        print(e)
    except DatabaseException.CHECK_VIOLATION as e:
        print(e)
    except DatabaseException.UNIQUE_VIOLATION as e:
        print(e)
    except DatabaseException.FOREIGN_KEY_VIOLATION as e:
        print(e)
    except Exception as e:
        print(e)
    finally:

        conn.close()


def getUsers(ID) -> ResultSet:
    conn = None
    rows_effected, result = 0, ResultSet()
    try:
        conn = Connector.DBConnector()
        rows_effected, result = conn.execute("SELECT * FROM Users WHERE id={I_D}", I_D=sql.Literal(ID))
        conn.commit()
        # rows_effected is the number of rows received by the SELECT
    except DatabaseException.ConnectionInvalid as e:
        print(e)
    except DatabaseException.NOT_NULL_VIOLATION as e:
        print(e)
    except DatabaseException.CHECK_VIOLATION as e:
        print(e)
    except DatabaseException.UNIQUE_VIOLATION as e:
        print(e)
    except DatabaseException.FOREIGN_KEY_VIOLATION as e:
        print(e)
    except Exception as e:
        print(e)
    finally:
        conn.close()
        return result


def insert_user_action( ID = 0 , name = 'test_user',question=-1 , Clickanswer='test_click' ) :
    conn = None
    try:
        conn = Connector.DBConnector()
        query = sql.SQL("INSERT INTO Users(id, name, question_number,answer) VALUES({id}, {username},{question_num},{answer_click})").format(id=sql.Literal(ID),
                                                                                       username=sql.Literal(name),
                                                                                       question_num = sql.Literal(question),
                                                                                       answer_click = sql.Literal(Clickanswer))
        rows_effected, _ = conn.execute(query)
        conn.commit()
    except DatabaseException.ConnectionInvalid as e:
        print(e)
    except DatabaseException.NOT_NULL_VIOLATION as e:
        print(e)
    except DatabaseException.CHECK_VIOLATION as e:
        print(e)
    except DatabaseException.UNIQUE_VIOLATION as e:
        print(e)
    except DatabaseException.FOREIGN_KEY_VIOLATION as e:
        print(e)
    except Exception as e:
        print(e)
    finally:
        conn.close()



def deleteUser(ID: int) -> bool:
    conn = None
    rows_effected = 0
    try:
        conn = Connector.DBConnector()
        query = sql.SQL("DELETE FROM Users WHERE id={I_D}").format(I_D=sql.Literal(ID))
        rows_effected, _ = conn.execute(query)
        conn.commit()
    except DatabaseException.ConnectionInvalid as e:
        print(e)
    except DatabaseException.NOT_NULL_VIOLATION as e:
        print(e)
    except DatabaseException.CHECK_VIOLATION as e:
        print(e)
    except DatabaseException.UNIQUE_VIOLATION as e:
        print(e)
    except DatabaseException.FOREIGN_KEY_VIOLATION as e:
        print(e)
    except Exception as e:
        print(e)
    finally:
        conn.close()
        return rows_effected > 0


if __name__ == '__main__':

    print("0. Creating all tables")
    createTable()
    insert_user_action(3,'gal',4,'correct')
    deleteUser(3)
    print("rr")
    dropTable()
    '''
    print("1. Add user with ID 1 and name Roei")
    addUser(1, 'Roei')

    print("2. Add user with ID 2 and name Noa")
    addUser(2, 'Noa')
    print('3. Can reinsert the same row since no commit was done')
    addUser(2, 'Noa')
    print("4. Printing all users")
    users = getUsers(printSchema=True)  # will cause printing the users, because printSchema=true in getUsers()
    print('5. Printing user in the second row')
    print(users[1]['id'], users[1]['name'])
    print("6. Printing all IDs")
    for index in range(users.size()):
        print(users[index]['ID'])
    print("7. Delete user with ID 1")
    deleteUser(1)
    print("8. Printing all users")
    users = getUsers(printSchema=False)  # will not cause printing the users, because printSchema=false in getUsers()
    # print users
    for index in range(users.size()):  # for each user
        current_row = users[index]  # get the row
        for col in current_row:  # iterate over the columns
            print(str(col) + "=" + str(current_row[col]))
    print("9. Delete user with ID 2, but do not commit, hence it is valid only within the connection")
    deleteUser(2, False)
    print("10. Printing all users - no change")
    users = getUsers(printSchema=False)  # will not cause printing the users, because printSchema=false in getUsers()
    # print users
    for index in range(users.size()):  # for each user
        current_row = users[index]  # get the row
        for col in current_row:  # iterate over the columns
            print(str(col) + "=" + str(current_row[col]))
    print("11. Dropping all tables - empty database")
    dropTable()
    '''
