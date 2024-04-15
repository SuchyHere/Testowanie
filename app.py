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
@app.route('/')
def home():
    return render_template('home.html')
if __name__ == '__main__':
    app.run(debug=True, port=5000)
