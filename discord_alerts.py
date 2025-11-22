import requests

class DiscordAlert:
    def __init__(self, webhook_url):
        self.webhook = webhook_url

    def send(self, message):
        data = {"content": message}
        try:
            requests.post(self.webhook, json=data)
        except:
            print("Error sending Discord message")
