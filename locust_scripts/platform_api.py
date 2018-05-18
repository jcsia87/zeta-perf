from locust import HttpLocust, TaskSet, task
import json


class UserBehavior(TaskSet):
    oauth_data = json.load(open("platform_data/oauthdata.json"))
    headers = json.load(open("headers/standardheader.json"))
    headers_with_bearer = headers
    recommendations_advance_data = json.load(open("platform_data/recommendations.json"))

    def on_start(self):
        self.get_auth_token()

    def get_auth_token(self):
        r = self.client.post("https://boomtrain.auth0.com/oauth/ro",
                             json=self.oauth_data)
        print r.content
        assert r.status_code is 200, "Unexpected response code: " + str(r.status_code)
        r_dict = r.json()
        self.id_token = r_dict['id_token']
        print self.id_token
        self.headers_with_bearer['Authorization'] = 'Bearer ' + self.id_token

    @task
    def recommendations_basic(self):
        r = self.client.get("/{}/email/{}?test=true".format('zt2bt-qa', 'david+zt2bt-qa@boomtrain.com'),
                            headers=self.headers)
        print r.content
        assert r.status_code is 200, "Unexpected response code: " + str(r.status_code)

    @task
    def recommendations_advanced(self):
        r = self.client.post("/{}/email/{}?test=true".format('zt2bt-qa', 'david+zt2bt-qa@boomtrain.com'),
                             json=self.recommendations_advance_data,
                             headers=self.headers)
        print r.content
        assert r.status_code is 200, "Unexpected response code: " + str(r.status_code)


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 2000
    max_wait = 5000
    host = 'https://recommendations.api.boomtrain.com/v1'
