from locust import HttpLocust, TaskSet, task


class UserBehavior(TaskSet):
    def on_start(self):
        """ on_start is called when a Locust start before
            any task is scheduled
        """
        self.login()

    def login(self):
        data = 'utf8=%E2%9C%93&user%5Bemail%5D=usersu.bme1%40gmail.com&user%5Bpassword%5D=b00mtrain&user%5Bremember_me%5D=1&commit=Log+In'
        self.client.get("/signin")
        self.client.post("/signin", data=data)

    @task
    def segments(self):
        self.client.get("/segments")

    @task
    def activities(self):
        self.client.get("/activities")

    @task
    def report(self):
        self.client.get("/report/summary")

    @task
    def subscribers(self):
        self.client.get("/subscribers")

    @task
    def content(self):
        self.client.get("/content")


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 15000
    host = 'https://phoenix.boomtrain.net'
