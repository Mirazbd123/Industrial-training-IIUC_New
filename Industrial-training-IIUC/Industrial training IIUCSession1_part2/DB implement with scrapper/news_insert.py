import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
from database_connection import create_db_connection


def execute_query(connection, query, id_query , data=None):
    """
    Execute a given SQL query on the provided database connection.

    Parameters
    ----------
    connection : mysql.connector.connection.MySQLConnection
        The connection object to the database.
    query : str
        The SQL query to execute.
    data : tuple, optional
        The data tuple to pass to the query, for parameterized queries.

    Returns
    -------
    None
    """
    cursor = connection.cursor()
    try:
        if data:
            cursor.execute(query, data)
        else:
            cursor.execute(query)
        connection.commit()
        print("Query successful")

        cursor.execute(id_query)
        row = cursor.fetchall()
        x = row[-1][0]
        return x

    except Error as e:
        print(f"The error '{e}' occurred")

def insert_category(connection, name, description):
    """
    Inserts a new category into the categories table.

    Parameters
    ----------
    connection : mysql.connector.connection.MySQLConnection
        The connection object to the database.
    name : str
        The name of the category.
    description : str
        The description of the category.

    Returns
    -------
    None
    """
    query = """
    INSERT INTO categories (name, description)
    VALUES (%s, %s)
    """
    data = (name, description)
    id_query = """SELECT id FROM categories"""
    return execute_query(connection, query,id_query, data)

def insert_reporter(connection, name, email):
    """
    Inserts a new author into the authors table.

    Parameters
    ----------
    connection : mysql.connector.connection.MySQLConnection
        The connection object to the database.
    name : str
        The name of the author.
    email : str
        The email of the author.

    Returns
    -------
    None
    """
    query = """
    INSERT INTO reporter (name, email)
    VALUES (%s, %s)
    """
    data = (name, email)
    id_query = """SELECT id FROM reporter"""
    return execute_query(connection, query, id_query,data)

def insert_publisher(connection, name, email,phone_number , head_office_address,website,facbook,twitter,linkedin,instagram):
    """
    Inserts a new editor into the editors table.

    Parameters
    ----------
    connection : mysql.connector.connection.MySQLConnection
        The connection object to the database.
    name : str
        The name of the editor.
    email : str
        The email of the editor.

    Returns
    -------
    None
    """
    query = """
    INSERT INTO publisher (name, email,phone_number , head_office_address,website,facbook,twitter,linkedin,instagram)
    VALUES (%s, %s,%s, %s,%s, %s,%s, %s,%s)
    """
    data = (name, email,phone_number , head_office_address,website,facbook,twitter,linkedin,instagram)
    id_query = """SELECT id FROM publisher"""
    return execute_query(connection, query,id_query ,data)

def insert_news(connection, category_id, author_id, editor_id, datetime, title, body, link):
    """
    Inserts a new news article into the news table.

    Parameters
    ----------
    connection : mysql.connector.connection.MySQLConnection
        The connection object to the database.
    category_id : int
        The ID of the category.
    author_id : int
        The ID of the author.
    editor_id : int
        The ID of the editor.
    datetime : datetime
        The publication date and time of the news article.
    title : str
        The title of the news article.
    body : str
        The body text of the news article.
    link : str
        The URL link to the full news article.

    Returns
    -------
    None
    """
    query = """
    INSERT INTO news (category_id, author_id, editor_id, datetime, title, body, link)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    data = (category_id, author_id, editor_id, datetime, title, body, link)
    id_query = """SELECT id FROM news"""
    return execute_query(connection, query, id_query ,data)

def insert_image(connection, news_id, image_url):
    """
    Inserts a new image into the images table.

    Parameters
    ----------
    connection : mysql.connector.connection.MySQLConnection
        The connection object to the database.
    news_id : int
        The ID of the news article associated with the image.
    image_url : str
        The URL of the image.

    Returns
    -------
    None
    """
    query = """
    INSERT INTO images (news_id, image_url)
    VALUES (%s, %s)
    """
    data = (news_id, image_url)
    id_query = """SELECT id FROM images"""
    return execute_query(connection, query,id_query,data )

def insert_summary(connection, news_id, summary_text):
    """
    Inserts a new summary into the summaries table.

    Parameters
    ----------
    connection : mysql.connector.connection.MySQLConnection
        The connection object to the database.
    news_id : int
        The ID of the news article associated with the summary.
    summary_text : str
        The text of the summary.

    Returns
    -------
    None
    """
    query = """
    INSERT INTO summaries (news_id, summary_text)
    VALUES (%s, %s)
    """
    data = (news_id, summary_text)
    id_query = """SELECT id FROM summaries"""
    return execute_query(connection, query, id_query,data)

# Example usage
if __name__ == "__main__":
    conn = create_db_connection()
    # if conn is not None:
    #     d = insert_category(conn, "Politics", "All news related to politics")
    #     e = insert_reporter(conn, "John Doe", "test@example.com")
    #     f = insert_publisher(conn , "Miraz" , "miraz@gmail.com" , "01701002818","oxygen/pathan para" , "WWW.mirazbd123.com" , "Miraz Alam",
    #                      "Mirazbd123" , "Miraz_Alam" , "Mirazul")
    #     print(d)
    #     print(e)
    #     print(f)
