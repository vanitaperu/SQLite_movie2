
from faulthandler import cancel_dump_traceback_later
from re import M
import db
from objects import Movie

def display_welcome():
    print("The Movie List Program")
    print()
    display_menu()

def display_menu():
    print("Command Menu")
    print("cat  - View movies by category")
    print("year - View movies by year")
    print("add  - Add a Movie")
    print("del  - Delete a Movie")
    print("exit - Exit program")
    print()

def display_categories():
    print("CATEGORIES")
    categories = db.get_categories()
    for category in categories:
        print(f"{category.id}. {category.name}")
    print()

def display_movies(movies, title_term):
    print(f"MOVIES - {title_term}")
    print(f"{'ID':<4}{'Name':<38}{'Year':<6}{'Mins':<6}{'Category':<10}{'Description':<25}")
    print("-" * 88)
    for movie in movies:
        print(f"{movie.id:<4d}{movie.name:<38}{movie.year:<6d}{movie.minutes:<6d}{movie.category.name if movie.category else 'N/A':<10}{movie.desc if movie.desc else 'N/A':<25}")

    print()

def get_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid whole number. Please try again.\n")

def display_movies_by_category():
    category_id = get_int("Category ID: ")
    category = db.get_category(category_id)
    if category is None:
        print("There is no category with that ID.\n")
    else:
        print()
        movies = db.get_movies_by_category(category_id)
        display_movies(movies, category.name.upper())

def display_movies_by_year():
    year = get_int("Year: ")
    print()
    movies = db.get_movies_by_year(year)
    display_movies(movies, str(year))

def add_movie():
    name = input("Name: ")
    year = get_int("Year: ")
    minutes = get_int("Minutes: ")
    desc = input("Description: ")
    category_id = get_int("Category ID: ")
    
    category = db.get_category(category_id)
    if category is None:
        print("There is no category with that ID. Movie not added.\n")
    else:
        movie = Movie(name=name, year=year, minutes=minutes, desc=desc, category=category)
        db.add_movie(movie)
        print(f"{name} was added to the database.\n")

def delete_movie():
    movie_id = get_int("Movie ID: ")
    db.delete_movie(movie_id)
    print(f"Movie ID {movie_id} was deleted from the database.\n")

def main():
    db.connect()
    display_welcome()
    display_categories()

    while True:
        command = input("Command: ").lower()
        if command == "cat":
            display_movies_by_category()
        elif command == "year":
            display_movies_by_year()
        elif command == "add":
            add_movie()
        elif command == "del":
            delete_movie()
        elif command == "exit":
            break
        else:
            print("Not a valid command. Please try again.\n")
            display_menu()

    db.close()
    print("Bye!")

if __name__ == "__main__":
    main()
