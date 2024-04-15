from flask import Flask, jsonify, request, render_template
import requests

app = Flask(__name__)

def fetch_data(url):
    response = requests.get(url)
    return response.json() if response.status_code == 200 else None

@app.route("/posts")
def aggregate_data():
    min_length = request.args.get('min_length', default=0, type=int)
    max_length = request.args.get('max_length', default=float('inf'), type=int)
    posts = fetch_data('https://jsonplaceholder.typicode.com/posts')
    users = fetch_data('https://jsonplaceholder.typicode.com/users')
    comments = fetch_data('https://jsonplaceholder.typicode.com/comments')

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

    return render_template('posts.html', posts=aggregated_data)

@app.route("/photos")
def photos():
    photos = fetch_data('https://jsonplaceholder.typicode.com/photos')
    albums = fetch_data('https://jsonplaceholder.typicode.com/albums')
    albums_dict = {album['id']: album for album in albums}
    
    photos_data = [{
        'title': photo['title'],
        'url': photo['url'],
        'album_id': photo['albumId'],
        'album_title': albums_dict[photo['albumId']]['title'] if photo['albumId'] in albums_dict else 'No album title'
    } for photo in photos]

    return render_template('photos.html', photos=photos_data)

@app.route("/albums/<int:album_id>")
def album_photos(album_id):
    photos = fetch_data(f'https://jsonplaceholder.typicode.com/albums/{album_id}/photos')
    album_info = fetch_data(f'https://jsonplaceholder.typicode.com/albums/{album_id}')

    return render_template('album_photos.html', photos=photos, album_title=album_info['title'] if album_info else 'No album title')

@app.route("/albums")
def albums():
    albums = fetch_data('https://jsonplaceholder.typicode.com/albums')
    photos = fetch_data('https://jsonplaceholder.typicode.com/photos')

    album_first_photo = {}
    for photo in photos:
        if photo['albumId'] not in album_first_photo:
            album_first_photo[photo['albumId']] = photo['url']

    albums_data = [{
        'id': album['id'],
        'title': album['title'],
        'first_photo_url': album_first_photo.get(album['id'], '')
    } for album in albums]

    return render_template('albums.html', albums=albums_data)


@app.route('/')
def home():
    return render_template('home.html')
if __name__ == '__main__':
    app.run(debug=True, port=5000)
