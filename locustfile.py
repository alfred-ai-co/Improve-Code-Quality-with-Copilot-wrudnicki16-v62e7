from locust import HttpUser, task, between
import logging

logging.basicConfig(level=logging.INFO)

class HelloWorldUser(HttpUser):
    wait_time = between(1, 5)
    entity_type = "project"
    user_id = 1

    def on_start(self):
        # Setup code here
        pass

    def on_stop(self):
        # Teardown code here
        pass

    @task
    def get_history(self):
        self.client.post("/api/history/", json={
            "entity_type": self.entity_type,
            "entity_id": 1,
            "change_type": "create",
            "user_id": self.user_id,
            "details": "Project created"
        })
        self.client.get("/api/history/1", params={
            "entity_type": self.entity_type,
            "offset": 0,
            "limit": 20
        })

    @task(2)
    def update_history(self):
        response = self.client.post("/api/history/", json={
            "entity_type": self.entity_type,
            "entity_id": 1,
            "change_type": "create",
            "user_id": self.user_id,
            "details": "Project created"
        })
        if response.status_code != 200:
            logging.error(f"Failed to create history: {response.status_code} {response.text}")
            return

        history_id = response.json().get("id")
        response = self.client.put(f"/api/history/{history_id}", json={
            "entity_type": self.entity_type,
            "entity_id": 1,
            "change_type": "update",
            "user_id": self.user_id,
            "details": "Project updated"
        })
        if response.status_code != 200:
            logging.error(f"Failed to update history: {response.status_code} {response.text}")

    @task(3)
    def delete_history(self):
        response = self.client.post("/api/history/", json={
            "entity_type": self.entity_type,
            "entity_id": 1,
            "change_type": "create",
            "user_id": self.user_id,
            "details": "Project created"
        })
        if response.status_code != 200:
            logging.error(f"Failed to create history: {response.status_code} {response.text}")
            return

        history_id = response.json().get("id")
        response = self.client.delete(f"/api/history/{history_id}/")
        if response.status_code != 200:
            logging.error(f"Failed to delete history: {response.status_code} {response.text}")

    @task(4)
    def get_large_history(self):
        for i in range(100):
            self.client.post("/api/history/", json={
                "entity_type": self.entity_type,
                "entity_id": 2,
                "change_type": "create",
                "user_id": self.user_id,
                "details": f"Project created {i}"
            })

        self.client.get("/api/history/2", params={
            "entity_type": self.entity_type,
            "offset": 0,
            "limit": 100
        })