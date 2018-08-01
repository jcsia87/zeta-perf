from locust import HttpLocust, TaskSet, task
import json
import random


class UserBehavior(TaskSet):

    def on_start(self):
        self.sites = ['qa-osr-site1', 'qa-osr-site-2', 'qa-osr-site3']
        self.bsins = json.load(open("osr_data/bsins.json"))

    @task
    def get_onsite_recommendations(self):
        r = self.client.get("/api/v1/osrs?site_id={}&bsin={}&selectors=%23selector1".format(random.choice(self.sites), random.choice(self.bsins)))
        assert r.status_code is 200, "Unexpected response code: " + str(r.status_code)


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 2000
    max_wait = 5000
    host = 'https://onsiterecs.api.boomtrain.com'
