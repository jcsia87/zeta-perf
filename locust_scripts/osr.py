from locust import HttpLocust, TaskSet, task
import json
import random
from datetime import datetime


class UserBehavior(TaskSet):

    def on_start(self):
        self.ids = ['20', '7', '22', '37', '14', '11', '17', '13', '28', '12']
        self.update_campaign_body = json.load(open("osr_data/update_campaign.json"))
    
    @task
    def get_all_osr_campaigns(self):
        r = self.client.get("/api/v1/campaigns?site_id=test-demo-site")
        assert r.status_code is 200, "Unexpected response code: " + str(r.status_code)

    @task
    def get_osr_campaign(self):
        r = self.client.get("/api/v1/campaigns/{}".format(random.choice(self.ids)))
        assert r.status_code is 200, "Unexpected response code: " + str(r.status_code)

    @task
    def update_osr_campaign(self):
        self.update_campaign_body['name'] = "Update: OSR Campaign - " + str(datetime.now())
        r = self.client.put("/api/v1/campaigns/{}".format(random.choice(self.ids)), json=self.update_campaign_body)
        assert r.status_code is 204, "Unexpected response code: " + str(r.status_code)

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 2000
    max_wait = 5000
    host = 'https://onsiterecs.api.phoenix.boomtrain.com'
