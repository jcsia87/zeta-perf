from locust import HttpLocust, TaskSet, task

class UserBehavior(TaskSet):
    def on_start(self):
        """ on_start is called when a Locust start before
            any task is scheduled
        """
        self.login()

    def login(self):
        self.client.post("/login",
                         {"username":"ellen_key",
                          "password":"education"})

    @task(1)
    def index(self):
        self.client.get("/")

    @task()
    def profile(self):
        self.client.get("/profile")

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = e