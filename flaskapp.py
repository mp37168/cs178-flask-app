# author: T. Urness and M. Moore
# description: Flask example using redirect, url_for, and flash
# credit: the template html files were constructed with the help of ChatGPT

from flask import Flask
from flask import render_template
from flask import Flask, render_template, request, redirect, url_for, flash
from dbCode import *

app = Flask(__name__)
app.secret_key = 'your_secret_key' # this is an artifact for using flash displays; 
                                   # it is required, but you can leave this alone

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/add-user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        # Extract form data
        name = request.form['name']
        genre = request.form['genre']
        
        # Process the data (e.g., add it to a database)
        # For now, let's just print it to the console
        print("Name:", name, ":", "Favorite Genre:", genre)
        
        flash('User added successfully! Huzzah!', 'success')  # 'success' is a category; makes a green banner at the top
        # Redirect to home page or another page upon successful submission
        return redirect(url_for('home'))
    else:
        # Render the form page if the request method is GET
        return render_template('add_user.html')

@app.route('/delete-user',methods=['GET', 'POST'])
def delete_user():
    if request.method == 'POST':
        # Extract form data
        name = request.form['name']
        
        # Process the data (e.g., add it to a database)
        # For now, let's just print it to the console
        print("Name to delete:", name)
        
        flash('User deleted successfully! Hoorah!', 'warning') 
        # Redirect to home page or another page upon successful submission
        return redirect(url_for('home'))
    else:
        # Render the form page if the request method is GET
        return render_template('delete_user.html')


@app.route('/display-users')
def display_users():
    # hard code a value to the users_list;
    # note that this could have been a result from an SQL query :) 
    users_list = (('John','Doe','Comedy'),('Jane', 'Doe','Drama'))
    return render_template('display_users.html', users = users_list)


@app.route('/movies-genres')
def movies_genres():
    movies = get_movies_with_genres()
    return render_template('movies_genres.html', movies = movies)

# Following function was genreated with the help of ChatGPT for C in CRUD
# it adds a movie to the database using a form and then redirects to the display movies page with a flash message confirming the addition.
@app.route('/add-movie', methods=['GET', 'POST'])
def add_movie():
    if request.method == 'POST':
        title = request.form['title']
        release_date = request.form['release_date']

        query = """
        INSERT INTO movie (title, release_date)
        VALUES (%s, %s)
        """
        execute_query(query, (title, release_date))

        flash("Movie added successfully!", "success")
        return redirect(url_for('display_movies'))

    return render_template('add_movie.html')

# following function was generated with the help of ChatGPT for R in CRUD
# it reads the movies from the database and displays them on a page using a template.
@app.route('/display-movies')
def display_movies():
    movies_list = get_movies()
    return render_template('display_movies.html', movies=movies_list)

# following function was generated with the help of ChatGPT for U in CRUD
# it updates a movie in the database using a form and then redirects to the display movies page
@app.route('/update-movie/<int:movie_id>', methods=['GET', 'POST'])
def update_movie(movie_id):
    if request.method == 'POST':
        title = request.form['title']
        release_date = request.form['release_date']

        query = """
        UPDATE movie
        SET title=%s, release_date=%s
        WHERE movie_id=%s
        """
        execute_query(query, (title, release_date, movie_id))

        flash("Movie updated!", "success")
        return redirect(url_for('display_movies'))

    movie = execute_query(
        "SELECT * FROM movie WHERE movie_id=%s",
        (movie_id,)
    )
    return render_template('update_movie.html', movie=movie[0])

# following function was generated with the help of ChatGPT for D in CRUD
# it deletes a movie from the database and then redirects to the display movies page with a flash
@app.route('/delete-movie/<int:movie_id>')
def delete_movie(movie_id):
    execute_query("DELETE FROM movie_cast WHERE movie_id=%s", (movie_id,))
    execute_query("DELETE FROM movie WHERE movie_id=%s", (movie_id,))


    flash("Movie deleted!", "warning")
    return redirect(url_for('display_movies'))


# these two lines of code should always be the last in the file
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
