from locust import HttpUser, task, between


class UserBehavior(HttpUser):
    wait_time = between(1, 5)

    @task(1)
    def view_posts(self):
        self.client.get("/posts")

    @task(2)
    def view_albums(self):
        self.client.get("/albums")

    @task(3)
    def view_photos(self):
        self.client.get("/photos")

    @task(4)
    def view_limit_albums(self):
        self.client.get("/albums?limit=3")

    @task(5)
    def view_limit_posts(self):
        self.client.get("/posts?limit=7")