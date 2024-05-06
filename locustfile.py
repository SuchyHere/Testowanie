from locust import HttpUser, task, between


class UserBehavior(HttpUser):
    wait_time = between(1, 5)

    @task(3)
    def view_posts(self):
        self.client.get("/posts")

    @task(2)
    def view_albums(self):
        self.client.get("/albums")

    @task(1)
    def view_photos(self):
        self.client.get("/photos")