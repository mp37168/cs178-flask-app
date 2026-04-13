# author: T. Urness and M. Moore
# description: Flask example using redirect, url_for, and flash
# credit: the template html files were constructed with the help of ChatGPT

from flask import Flask
from flask import render_template
from flask import Flask, render_template, request, redirect, url_for, flash
from dbCode import *
from dynamoCode import *

app = Flask(__name__)
app.secret_key = 'your_secret_key' # this is an artifact for using flash displays; 
                                   # it is required, but you can leave this alone

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/add-user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        genre = request.form['genre']

        execute_query("""
            INSERT INTO user (name, genre)
            VALUES (%s, %s)
        """, (name, genre))

        flash('User added successfully!', 'success')
        return redirect(url_for('display_users'))

    return render_template('add_user.html')
@app.route('/delete-user/<int:user_id>')
def delete_user(user_id):
    execute_query("DELETE FROM user WHERE user_id=%s", (user_id,))
    flash("User deleted successfully!", "warning")
    return redirect(url_for('display_users'))

@app.route('/display-users')
def display_users():
    users_list = execute_query("""
        SELECT user_id, name, genre
        FROM user
    """)
    return render_template('display_users.html', users=users_list)

@app.route('/update-user/<int:user_id>', methods=['GET', 'POST'])
def update_user(user_id):
    if request.method == 'POST':
        name = request.form['name']
        genre = request.form['genre']

        execute_query("""
            UPDATE user
            SET name=%s, genre=%s
            WHERE user_id=%s
        """, (name, genre, user_id))

        flash("User updated successfully!", "success")
        return redirect(url_for('display_users'))

    user = execute_query(
        "SELECT * FROM user WHERE user_id=%s",
        (user_id,)
    )

    return render_template('update_user.html', user=user[0])

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

@app.route('/add-favorite/<int:movie_id>/<title>')
def add_favorite_route(movie_id, title):
    username = "guest"

    add_favorite(username, movie_id, title)

    flash("Added to favorites!", "success")
    return redirect(url_for('display_movies'))

@app.route('/favorites')
def favorites():
    username = "guest"

    favs = get_favorites(username)
    return render_template('favorites.html', favorites=favs)

@app.route('/delete-favorite/<movie_id>')
def delete_favorite_route(movie_id):
    username = "guest"

    delete_favorite(username, movie_id)

    flash("Removed from favorites!", "warning")
    return redirect(url_for('favorites'))

# these two lines of code should always be the last in the file
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
