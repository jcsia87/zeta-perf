from locust import HttpLocust, TaskSet, task
from lxml import html


class UserBehavior(TaskSet):
    SIGN_IN_PAGE_CSS = '[class^="Header__HeaderItem-]'
    def on_start(self):
        """ on_start is called when a Locust start before
            any task is scheduled
        """
        self.login()

    def login(self):
        data = 'utf8=%E2%9C%93&user%5Bemail%5D=usersu.bme1%40gmail.com&user%5Bpassword%5D=b00mtrain&user%5Bremember_me%5D=1&commit=Log+In'
        self.client.get("/signin")
        r = self.client.post("/signin", data=data)
        tree = html.fromstring(r.text)
        assert tree.cssselect(self.SIGN_IN_PAGE_CSS)[0].text == "Dashboard", \
            "Expected title has not been found!"

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
