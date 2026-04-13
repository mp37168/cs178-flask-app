# Movie Browser

**CS178: Cloud and Database Systems — Project #1**
**Author:** Maddie Phillips
**GitHub:** mp37168

---

## Overview

<!-- Describe your project in 2-4 sentences. What does it do? Who is it for? What problem does it solve? -->
Movie Browser is a full-stack web application built with Flask that allows users to browse and manage a movie database. Users can perform full CRUD operations on movies and users, view relational data using SQL JOIN queries, and save favorite movies using a DynamoDB NoSQL database.

The project demonstrates integration between AWS services including EC2 (deployment), RDS (MySQL relational database), and DynamoDB (NoSQL storage). It is designed as a simple but complete cloud-based database application.

---

## Technologies Used

- **Flask** — Python web framework
- **AWS EC2** — hosts the running Flask application
- **AWS RDS (MySQL)** — relational database for storing movies, users, genres, and relationships
- **AWS DynamoDB** — non-relational database for storing user favorite movies
- **GitHub Actions** — auto-deploys code from GitHub to EC2 on push

---

## Project Structure

```
ProjectOne/
├── flaskapp.py # Main Flask application — all routes and app logic (MySQL + DynamoDB integration)
├── dbCode.py # MySQL helper functions (connection + queries)
├── dynamoCode.py # DynamoDB helper functions (favorites system)
├── creds.py # AWS/RDS credentials (NOT pushed to GitHub)
├── creds_sample.py # Example credentials file (safe version)

├── templates/
│ ├── home.html # Landing page / navigation dashboard
│ ├── add_user.html # Create new user
│ ├── display_users.html # View all users
│ ├── update_user.html # Update user information
│ ├── delete_user.html # (if used) user deletion page

│ ├── add_movie.html # Create movie (SQL CREATE)
│ ├── display_movies.html # View movies (SQL READ + DynamoDB links)
│ ├── update_movie.html # Update movie (SQL UPDATE)
│ ├── movies_genres.html # JOIN query results (movies + genres)
│ ├── favorites.html # DynamoDB favorites page (NoSQL READ)

└── README.md
```

---

## How to Run Locally

1. Clone the repository:

   ```bash
   git clone https://github.com/mp37168/cs178-flask-app.git
   cd cs178-flask-app
   ```

2. Install dependencies:

   ```bash
   pip3 install flask pymysql boto3
   ```

3. Set up your credentials (see Credential Setup below)

4. Run the app:

   ```bash
   python3 flaskapp.py
   ```

5. Open your browser and go to `http://127.0.0.1:8080`

---

## How to Access in the Cloud

The app is deployed on an AWS EC2 instance. To view the live version:

```
http://ec2-23-22-172-115.compute-1.amazonaws.com:8080/
```

_(Note: the EC2 instance may not be running after project submission.)_

---

## Credential Setup

This project requires a `creds.py` file that is **not included in this repository** for security reasons.

Create a file called `creds.py` in the project root with the following format (see `creds_sample.py` for reference):

```python
# creds.py — do not commit this file
host = "your-rds-endpoint"
user = "admin"
password = "your-password"
db = "your-database-name"
```

---

## Database Design

### SQL (MySQL on RDS)

The relational database stores movies, users, genres, and relationships between them.

- `movie` — stores movie_id, title, and release_date
- `user` — stores user_id, name, and genre preference
- `genre` — stores genre names
- `movie_genres` — join table connecting movies and genres
- `movie_cast` — stores cast information for movies


The JOIN query used in this project:
- Movies are joined with the `movie_genres` table
- Then joined with `genre` to display genre names alongside movies
This allows the application to display enriched movie information on the `/movies-genres` page.

### DynamoDB

- **Table name:** FavoriteMovies
- **Partition key:** username
- **Sort key:** movie_id

Each item stores:
- username (string)
- movie_id (number/string)
- title (string)

### Used for:
Storing a user's favorite movies. Users can add movies from the movie browser, view their saved favorites, and remove them.

---

## CRUD Operations

| Operation | Type | Route | Description |
|----------|------|--------|-------------|
| Create | SQL | `/add-movie`, `/add-user` | Adds movies and users to MySQL database |
| Read | SQL | `/display-movies`, `/display-users` | Displays stored data |
| Update | SQL | `/update-movie/<id>`, `/update-user/<id>` | Updates existing records |
| Delete | SQL | `/delete-movie/<id>`, `/delete-user/<id>` | Removes records |
| Create | NoSQL | `/add-favorite` | Adds favorite movie to DynamoDB |
| Read | NoSQL | `/favorites` | Displays saved favorites |
| Delete | NoSQL | `/delete-favorite/<id>` | Removes favorite movie |
---

## Challenges and Insights

<!-- What was the hardest part? What did you learn? Any interesting design decisions? -->
One of the biggest challenges in this project was correctly integrating both SQL (MySQL) and NoSQL (DynamoDB) databases into a single Flask application. Initially, I struggled with correctly structuring JOIN queries due to inconsistencies in table names.

Another challenge was debugging AWS permissions for DynamoDB, specifically IAM access errors when attempting to use PutItem. This helped me understand the importance of IAM roles and permissions in cloud applications.

I also learned the importance of proper spacing and indentation in Python and HTML. Since both languages rely heavily on structure and formatting, small mistakes can lead to errors or unexpected behavior. This reinforced the importance of writing clean, well-organized code for both functionality and readability.

On the frontend side, I learned the importance of spacing, indentation, and consistent styling using Bootstrap. Without consistent formatting, pages looked unorganized and were harder to use, so improving UI structure made the application much more professional.

Overall, I learned how full-stack applications connect frontend templates, backend Flask routes, and cloud-based databases into a single working system.



## AI Assistance

ChatGPT was used to assist with:
- Help debug Flask routing issues (including 404 errors and incorrect route parameters)
- Assist with integrating AWS DynamoDB (PutItem, GetItem, and permission errors)
- Improve SQL queries and JOIN logic for displaying movie and genre data
- Format HTML templates using Bootstrap for a more consistent and professional UI
- Improve code organization and readability across Flask routes and database helper files