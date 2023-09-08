import sqlite3
import os


# Function to create the database and table
def create_database_table():
    conn = sqlite3.connect('stephen_king_adaptations.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stephen_king_adaptations_table (
            movieID INTEGER PRIMARY KEY AUTOINCREMENT,
            movieName TEXT,
            movieYear INTEGER,
            imdbRating REAL
        )
    ''')

    conn.commit()
    conn.close()


# Function to read the file and insert data into the table if the table is empty
def insert_data_from_file():
    conn = sqlite3.connect('stephen_king_adaptations.db')
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM stephen_king_adaptations_table")
    count = cursor.fetchone()[0]
    if count > 0:
        print("Database is not empty. Skipping data insertion.")
        return

    with open('stephen_king_adaptations.txt', 'r') as file:
        lines = file.readlines()

    for line in lines:
        movie_data = line.strip().split(',')
        cursor.execute('INSERT INTO stephen_king_adaptations_table (movieName, movieYear, imdbRating) VALUES (?, ?, ?)',
                       (movie_data[1], int(movie_data[2]), float(movie_data[3])))

    conn.commit()
    conn.close()


# Function to search for movies based on user input
def search_movies():
    conn = sqlite3.connect('stephen_king_adaptations.db')
    cursor = conn.cursor()

    while True:
        print("\nOptions:")
        print("1. Search by Movie Name")
        print("2. Search by Movie Year")
        print("3. Search by Movie Rating")
        print("4. STOP")
        option = input("Enter your choice: ")

        if option == '1':
            movie_name = input("Enter the name of the movie: ")
            cursor.execute('SELECT * FROM stephen_king_adaptations_table WHERE movieName LIKE ?',
                           ('%' + movie_name + '%',))
            result = cursor.fetchall()
            if result:
                for row in result:
                    print(f"Movie Name: {row[1]}, Year: {row[2]}, Rating: {row[3]}")
            else:
                print("No such movie exists in our database.")

        elif option == '2':
            movie_year = input("Enter the year: ")
            cursor.execute('SELECT * FROM stephen_king_adaptations_table WHERE movieYear = ?', (int(movie_year),))
            result = cursor.fetchall()
            if result:
                for row in result:
                    print(f"Movie Name: {row[1]}, Year: {row[2]}, Rating: {row[3]}")
            else:
                print("No movies were found for that year in our database.")

        elif option == '3':
            rating_limit = input("Enter the minimum rating: ")
            cursor.execute('SELECT * FROM stephen_king_adaptations_table WHERE imdbRating >= ?', (float(rating_limit),))
            result = cursor.fetchall()
            if result:
                for row in result:
                    print(f"Movie Name: {row[1]}, Year: {row[2]}, Rating: {row[3]}")
            else:
                print("No movies at or above that rating were found in the database.")

        elif option == '4':
            break

        else:
            print("Invalid option. Please choose a valid option.")

        print("Thank you for using.")

    conn.close()


# Main program
create_database_table()
insert_data_from_file()
search_movies()
