from flask import Flask, jsonify, request, render_template
import requests
import logging
from logging.handlers import RotatingFileHandler

# Logowanie
logging.basicConfig(level=logging.INFO)
handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=3)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

app = Flask(__name__)
app.logger.addHandler(handler)
def valid_limit(limit):
    try:
        return int(limit) >= 0
    except ValueError:
        return False


def fetch_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # wyjątek dla kodów 400 i 500
        return response.json()
    except requests.RequestException as e:
        app.logger.error(f"Błąd przy pobieraniu danych z {url}: {e}")
        return None

@app.route("/posts")
def aggregate_data():
    try:
        min_length = request.args.get('min_length', default=0, type=int)
        max_length = request.args.get('max_length', default=float('inf'), type=int)
        limit = request.args.get('limit')

        if limit is not None and not valid_limit(limit):
            return jsonify({'error': 'Invalid limit value'}), 400
        limit = int(limit) if limit is not None else None

        if limit == 0:
            return jsonify({'error': 'Limit is set to null'}), 400

        posts = fetch_data('https://jsonplaceholder.typicode.com/posts')
        users = fetch_data('https://jsonplaceholder.typicode.com/users')
        comments = fetch_data('https://jsonplaceholder.typicode.com/comments')

        if not posts or not users or not comments:
            raise ValueError("Nie udało się pobrać danych")

        users_dict = {user['id']: user for user in users}
        aggregated_data = []

        for post in posts:
            if min_length <= len(post['body']) <= max_length:
                user = users_dict.get(post['userId'])
                post_comments = [{
                    'name': c['name'],
                    'body': c['body'],
                    'email': c['email']
                } for c in comments if c['postId'] == post['id']]

                aggregated_data.append({
                    'name': user['name'] if user else 'No name',
                    'username': user['username'] if user else 'No username',
                    'post_body': post['body'],
                    'comments': post_comments
                })

        if limit is not None:
            aggregated_data = aggregated_data[:limit]

        return render_template('posts.html', posts=aggregated_data)
    except Exception as e:
        app.logger.error(f"Błąd przy agregowaniu danych postów: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500


@app.route("/photos")
def photos():
    try:
        limit = request.args.get('limit')
        if limit is not None and not valid_limit(limit):
            return jsonify({'error': 'Invalid limit value'}), 400
        limit = int(limit) if limit is not None else None

        if limit == 0:
            return jsonify({'error': 'Limit is set to null'}), 400

        photos = fetch_data('https://jsonplaceholder.typicode.com/photos')
        if photos is None:
            raise ValueError("Nie udało się pobrać danych zdjęć.")

        if limit is not None:
            photos = photos[:limit]

        return render_template('photos.html', photos=photos)
    except Exception as e:
        app.logger.error(f"Błąd przy ładowaniu zdjęć: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route("/albums/<int:album_id>")
def album_photos(album_id):
    try:
        photos = fetch_data(f'https://jsonplaceholder.typicode.com/albums/{album_id}/photos')
        album_info = fetch_data(f'https://jsonplaceholder.typicode.com/albums/{album_id}')
        if photos is None or album_info is None:
            raise ValueError("Nie udało się pobrać danych albumu lub zdjęć.")

        return render_template('album_photos.html', photos=photos, album_title=album_info['title'] if album_info else 'No album title')
    except Exception as e:
        app.logger.error(f"Błąd przy ładowaniu zdjęć dla albumu {album_id}: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route("/albums")
def albums():
    try:
        limit = request.args.get('limit')
        if limit is not None and not valid_limit(limit):
            return jsonify({'error': 'Invalid limit value'}), 400
        limit = int(limit) if limit is not None else None
        if limit == 0:
            return jsonify({'error': 'Limit is set to null'}), 400

        albums = fetch_data('https://jsonplaceholder.typicode.com/albums')
        photos = fetch_data('https://jsonplaceholder.typicode.com/photos')
        if albums is None or photos is None:
            raise ValueError("Nie udało się pobrać danych albumów lub zdjęć.")

        if limit is not None:
            albums = albums[:limit]

        return render_template('albums.html', albums=albums, photos=photos)
    except Exception as e:
        app.logger.error(f"Błąd przy ładowaniu albumów: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
