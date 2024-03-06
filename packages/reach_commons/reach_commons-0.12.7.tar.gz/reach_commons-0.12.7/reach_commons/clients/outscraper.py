import os

import requests


class OutscraperClient:
    def __init__(self):
        self.environment = os.environ.get("ENV", "Staging")
        self.base_url = "https://api.app.outscraper.com"

    @property
    def headers(self):
        common_headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        auth_token = {
            "Staging": "MWM5ZDg3MTdlNTE2NGIwMjgzNzRkNTVmNDhhMTQ0MzV8MzhhOWRmYjk3Mg",
            "Prod": "MWM5ZDg3MTdlNTE2NGIwMjgzNzRkNTVmNDhhMTQ0MzV8MzhhOWRmYjk3Mg",
        }.get(self.environment)

        return {**common_headers, "X-API-KEY": auth_token}

    @property
    def webhook_url(self):
        return {
            "Staging": "https://api-staging.getreach.ai/webhooks/data-bridge/outscraper/scraper-completed?token=tRm4k75N9hK1vF0dSwIi0HcMyV",
            "Prod": "https://api.getreach.ai/webhooks/data-bridge/outscraper/scraper-completed?token=tRm4k75N9hK1vF0dSwIi0HcMyV",
        }.get(self.environment)

    def search_google_maps_reviews(self, google_place_id: str, start_from: int):
        params = {
            "query": google_place_id,
            "webhook": self.webhook_url,
            "reviewsLimit": 0,
        }
        if start_from:
            params["start"] = start_from
        resp = requests.get(
            f"{self.base_url}/maps/reviews-v3",
            headers=self.headers,
            params=params,
        )
        return resp
