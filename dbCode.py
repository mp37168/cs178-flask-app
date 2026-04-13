# dbCode.py
# Author: Maddie Phillips
# Helper functions for database connection and queries

import pymysql
import creds

def get_conn():
    """Returns a connection to the MySQL RDS instance."""
    conn = pymysql.connect(
        host=creds.host,
        user=creds.user,
        password=creds.password,
        db=creds.db,
    )
    return conn

def execute_query(query, args=()):
    conn = get_conn()
    cur = conn.cursor(pymysql.cursors.DictCursor)

    cur.execute(query, args)
    conn.commit()   

    try:
        rows = cur.fetchall()
    except:
        rows = []

    cur.close()
    conn.close()
    return rows

def get_movies():
    """Returns a list of 15 movies in the database."""
    query = """
    SELECT movie_id, title, release_date
    FROM movie
    ORDER BY RAND()
    LIMIT 15;
    """
    return execute_query(query)


def get_movies_with_genres():
    """Returns a list of movies in the database that match the given genre."""
    query = """
SELECT m.title, m.release_date, g.genre_name
FROM movie m
JOIN movie_genres mg ON m.movie_id = mg.movie_id
JOIN genre g ON mg.genre_id = g.genre_id
ORDER BY RAND()
LIMIT 15;
    """
    return execute_query(query)