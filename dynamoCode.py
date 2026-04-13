import boto3
from boto3.dynamodb.conditions import Key

# Connect to DynamoDB (same region as your AWS table)
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')

# Your table name MUST match AWS exactly
table = dynamodb.Table('FavoriteMovies')


# -------------------------
# CREATE (add favorite)
# -------------------------
def add_favorite(username, movie_id, title):
    table.put_item(
        Item={
            "username": username,
            "movie_id": str(movie_id),
            "title": title
        }
    )


# -------------------------
# READ (get favorites)
# -------------------------
def get_favorites(username):
    response = table.query(
        KeyConditionExpression=Key('username').eq(username)
    )
    return response.get('Items', [])


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