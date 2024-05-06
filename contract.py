import requests
import pytest
import json

BASE_URL = 'https://jsonplaceholder.typicode.com/'

@pytest.mark.contract
def test_get_user_contract():
    user_id = 1

    response = requests.get(f"{BASE_URL}/users/{user_id}")

    assert response.status_code == 200
    assert response.headers["Content-Type"].startswith("application/json")

    user_data = response.json()
    assert user_data["id"] == user_id

@pytest.mark.contract
def test_create_post_contract():
    user_id = 1
    post_data = {
        "userId": user_id,
        "title": "My New Post",
        "body": "This is the content of my new post."
    }

    response = requests.post(f"{BASE_URL}/posts", json=post_data)

    assert response.status_code == 201
    assert response.headers["Content-Type"].startswith("application/json")

    created_post = response.json()
    assert created_post["userId"] == user_id
    assert created_post["title"] == post_data["title"]
    assert created_post["body"] == post_data["body"]

    response = requests.get(f"{BASE_URL}/posts/{created_post['id']}")
    fetched_post = response.json()
    assert fetched_post == created_post

@pytest.mark.contract
def test_delete_post_contract():
    post_id = 101

    response = requests.delete(f"{BASE_URL}/posts/{post_id}")

    assert response.status_code == 200

    response = requests.get(f"{BASE_URL}/posts/{post_id}")
    assert response.status_code == 404