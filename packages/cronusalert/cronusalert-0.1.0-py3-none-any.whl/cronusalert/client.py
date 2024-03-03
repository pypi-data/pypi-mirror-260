import json
import requests


class AlertType:
    FIRING = "firing"
    RESOLVED = "resolved"
    NEUTRAL = "neutral"


class Alert:
    def __init__(self, summary, description, status):
        self.summary = summary
        self.description = description
        self.status = status


class CronusAlertClient:
    host = "https://cronusmonitoring.com"

    def __init__(self, token):
        self.token = token
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
            }
        )

    def build_req(self, alert):
        alert_req = {
            "status": alert.status,
            "annotations": {"summary": alert.summary, "description": alert.description},
        }

        alerts = {"alerts": [alert_req]}
        return json.dumps(alerts)

    def fire(self, alert):
        payload = self.build_req(alert)
        response = self.session.post(f"{self.host}/api/alert", data=payload)

        if response.status_code != 200:
            raise Exception(response.text)

        return response
