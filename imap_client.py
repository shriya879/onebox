from elasticsearch import Elasticsearch
from imapclient import IMAPClient
import email
from email.header import decode_header
from datetime import datetime, timedelta
from config import EMAIL_ACCOUNTS

# Connect to Elasticsearch
es = Elasticsearch("http://localhost:9200")

def store_email_in_es(email_data):
    es.index(index="emails", document=email_data)

def fetch_last_30_days_emails():
    for account in EMAIL_ACCOUNTS:
        try:
            with IMAPClient(account["imap_server"]) as client:
                client.login(account["email"], account["password"])
                client.select_folder("INBOX")

                date_cutoff = (datetime.now() - timedelta(days=30)).strftime("%d-%b-%Y")
                messages = client.search([f"SINCE {date_cutoff}"])

                for msg_id in messages:
                    raw_message = client.fetch(msg_id, ["RFC822"])[msg_id][b"RFC822"]
                    msg = email.message_from_bytes(raw_message)

                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding or "utf-8")

                    email_data = {
                        "from": msg["From"],
                        "subject": subject,
                        "date": msg["Date"],
                        "account": account["email"]
                    }

                    store_email_in_es(email_data)

                client.logout()

        except Exception as e:
            print(f"Error fetching emails for {account['email']}: {str(e)}")
