import boto3

REGION = "us-east-2"
TABLE_NAME = "FavoriteMovies"


def get_table():
    dynamodb = boto3.resource("dynamodb", region_name=REGION)
    return dynamodb.Table(TABLE_NAME)

# -------------------------
# CREATE (add favorite)
# -------------------------
def add_favorite(username, movie_id, Title):
    table.put_item(
        Item={
            "username": username,
            "movie_id": str(movie_id),
            "Title": Title
        }
    )


# -------------------------
# READ (get favorites)
# -------------------------

def get_favorites(username):
    table = get_table()

    response = table.scan()  

    items = response.get("Items", [])

    return [item for item in items if item.get("username") == username]

# -------------------------
# DELETE (remove favorite)
# -------------------------
def delete_favorite(username, movie_id):
    table.delete_item(
        Key={
            "username": username,
            "movie_id": str(movie_id)
        }
    )