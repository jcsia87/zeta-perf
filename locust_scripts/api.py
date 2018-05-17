from locust import HttpLocust, TaskSet, task
import json


class UserBehavior(TaskSet):
    headers = json.load(open("headers/standardheader.json"))
    create_user_data = json.load(open("api_data/createuser.json"))
    create_activity_data = json.load(open("api_data/createactivity.json"))
    create_campaign_data = json.load(open("api_data/createcampaign.json"))

    @task
    def get_user(self):
        r = self.client.get("/201507/subscribers?uid=frodo.baggins",
                            headers=self.headers)
        print r.content
        assert r.status_code is 200, "Unexpected response code: " + str(r.status_code)

    @task
    def create_user(self):
        r = self.client.post("/201507/subscribers/identify",
                             json=self.create_user_data,
                             headers=self.headers)
        print r.content
        assert r.status_code is 200, "Unexpected response code: " + str(r.status_code)

    @task
    def create_activity(self):
        r = self.client.post("/201507/activities",
                             json=self.create_activity_data,
                             headers=self.headers)
        print r.content
        assert r.status_code is 202, "Unexpected response code: " + str(r.status_code)

    @task
    def create_campaign(self):
        r = self.client.post("/201507/campaigns",
                             json=self.create_campaign_data,
                             headers=self.headers)
        print r.content
        assert r.status_code is 200, "Unexpected response code: " + str(r.status_code)


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 2000
    max_wait = 5000
    host = 'https://phoenix.boomtrain.net'
