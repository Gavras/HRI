import Utility.DBConnector as Connector

from Utility.Exceptions import DatabaseException
from Utility.DBConnector import ResultSet
from psycopg2 import sql


def dropTable() -> None:
    conn = None
    conn_valid=True

    try:
        conn = Connector.DBConnector()
        conn.execute("DROP TABLE IF EXISTS Users CASCADE")
        conn.commit()
    except DatabaseException.ConnectionInvalid as e:
        print(e)
        con_valid=False
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

        if conn_valid:
           conn.close()


def createTable() -> None:
    conn = None
    conn_valid=True
    
    try:
	    
        conn = Connector.DBConnector()
        action ="CREATE TABLE Users(name TEXT NOT NULL,question_number INTEGER NOT NULL,answer_number INTEGER NOT NULL,answer TEXT NOT NULL,date_time TIMESTAMPTZ DEFAULT Now() ,with_robot TEXT NOT NULL); " \

        conn.execute(action)
        conn.commit()
    except DatabaseException.ConnectionInvalid as e:

        print(e)
        conn_valid=False
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
        if conn_valid:
             conn.close()


def getUser(N) -> ResultSet:
    conn = None
    conn_valid=True
    rows_effected, result = 0, ResultSet()
    try:
        conn = Connector.DBConnector()
        query = sql.SQL("SELECT * FROM Users WHERE name ={Name}").format(Name=sql.Literal(N))
        rows_effected, result = conn.execute(query) 
        conn.commit()
        # rows_effected is the number of rows received by the SELECT
    except DatabaseException.ConnectionInvalid as e:
        print(e)
        conn_valid=False
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
        if conn_valid:
             conn.close()
        return result


def insert_user_action(name = 'test_user',question=-1,a_number=-1 , Clickanswer='test_click' , _robot="false") :
    conn = None
    conn_valid=True

    try:
        conn = Connector.DBConnector()
        query = sql.SQL("INSERT INTO Users( name, question_number,answer_number,answer,with_robot) VALUES({username},{question_num},{a_num},{answer_click},{robot})").format(
                                                                                       username=sql.Literal(name),
                                                                                       a_num=sql.Literal(a_number),
                                                                                       question_num = sql.Literal(question),
                                                                                       answer_click = sql.Literal(Clickanswer),
                                                                                       robot = sql.Literal(_robot))

        rows_effected, _ = conn.execute(query)
        conn.commit()
    except DatabaseException.ConnectionInvalid as e:
        print("action: ( {0},{1},{2},{3}) FAILED to DataBase".format(name,question,a_number,Clickanswer))
        conn_valid=False

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
        if conn_valid:
            conn.close()
            print("action: ( {0},{1},{2},{3}) SUCCEEDED to DataBase".format( name, question,a_number, Clickanswer))


def deleteUser(N) -> bool:
    conn = None
    conn_valid=True
    rows_effected = 0
    try:
        conn = Connector.DBConnector()
        query = sql.SQL("DELETE FROM Users WHERE name={Name}").format(Name=sql.Literal(N))
        rows_effected, _ = conn.execute(query)
        conn.commit()
    except DatabaseException.ConnectionInvalid as e:
        print(e)
        conn_valid=False
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
        if conn_valid:
            conn.close()
        return rows_effected > 0



