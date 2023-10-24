
import sqlite3
from contextlib import closing
from sqlite3 import connect, Error

class Category:
    def __init__(self, category_id, name):
        self.id = category_id
        self.name = name

class Movie:
    def __init__(self, movie_id, name, year, minutes, desc, category):
        self.id = movie_id
        self.name = name
        self.year = year
        self.minutes = minutes
        self.desc = desc
        self.category = category

conn = None

def connect():
    global conn
    if not conn:
        DB_FILE = "movies.sqlite"
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row

def close():
    if conn:
        conn.close()

def make_category(row):
    return Category(row["categoryID"], row["categoryName"])

def make_movie(row):
    return Movie(
        row["movieID"],
        row["name"],
        row["year"],
        row["minutes"],
        row["desc"],
        make_category(row)
    )

def make_movie_list(results):
    movies = []
    for row in results:
        movies.append(make_movie(row))
    return movies

def get_categories():
    query = '''SELECT categoryID, name as categoryName
               FROM Category'''
    with closing(conn.cursor()) as c:
        c.execute(query)
        results = c.fetchall()

    categories = []
    for row in results:
        categories.append(make_category(row))
    return categories

def get_category(category_id):
    query = '''SELECT categoryID, name as categoryName
               FROM Category WHERE categoryID = ?'''
    with closing(conn.cursor()) as c:
        c.execute(query, (category_id,))
        row = c.fetchone()
        if row:
            return make_category(row)
        else:
            return None

def get_movies_by_category(category_id):
    query = '''SELECT movieID, Movie.name, year, minutes, desc,
                    Movie.categoryID,
                    Category.name as categoryName
               FROM Movie JOIN Category
                    ON Movie.categoryID = Category.categoryID
               WHERE Movie.categoryID = ?'''
    with closing(conn.cursor()) as c:
        c.execute(query, (category_id,))
        results = c.fetchall()

    return make_movie_list(results)

def get_movies_by_year(year):
    query = '''SELECT movieID, Movie.name, year, minutes, desc,
                    Movie.categoryID,
                    Category.name as categoryName
               FROM Movie JOIN Category
                    ON Movie.categoryID = Category.categoryID
               WHERE year = ?'''
    with closing(conn.cursor()) as c:
        c.execute(query, (year,))
        results = c.fetchall()

    return make_movie_list(results)

def add_movie(movie):
    sql = '''INSERT INTO Movie(categoryID, name, year, minutes, desc)
             VALUES (?,?,?,?,?)'''
    with closing(conn.cursor()) as c:
        try:
            conn.execute('BEGIN TRANSACTION')  # Start a transaction
            c.execute(sql, (movie.category.id, movie.name, movie.year, movie.minutes, movie.desc))
            conn.commit()  # Commit the transaction
        except sqlite3.Error as e:
            print("Error while adding the movie:", e)
            conn.rollback()  # Roll back the transaction in case of an error

def delete_movie(movie_id):
    try:
        conn = sqlite3.connect("movies.sqlite")  # Replace with the actual path to your SQLite database file
        sql = '''DELETE FROM Movie WHERE movieID = ?'''
        with conn:
            conn.execute(sql, (movie_id,))
            conn.commit()
            print("Movie with ID {} deleted.".format(movie_id))
    except sqlite3.Error as e:
        print("An error occurred:", e)





