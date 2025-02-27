from slack_sdk import WebClient
import requests

def send_slack_notification(email_subject, slack_token, slack_channel):
    client = WebClient(token=slack_token)
    client.chat_postMessage(channel=slack_channel, text=f"New Interested email: {email_subject}")

def trigger_webhook(email_data):
    webhook_url = "https://webhook.site/your-webhook-url"
    requests.post(webhook_url, json=email_data)
