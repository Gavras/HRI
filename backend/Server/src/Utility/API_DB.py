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


def getUser(ID) -> ResultSet:
    conn = None
    rows_effected, result = 0, ResultSet()
    try:
        conn = Connector.DBConnector()
        query = sql.SQL("SELECT * FROM Users WHERE id ={i_d}").format(i_d=sql.Literal(ID))
        rows_effected, result = conn.execute(query) 
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



