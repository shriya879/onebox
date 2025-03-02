from flask import Flask, jsonify
from flask_cors import CORS
import imaplib
import email
from email.header import decode_header

app = Flask(__name__)
CORS(app)

EMAIL_ACCOUNT = "shri8ya@gmail.com"
EMAIL_PASSWORD = "bilx lxyu eobi xwpx"
IMAP_SERVER = "imap.gmail.com"

def fetch_gmail_emails(limit=5):
    emails = []
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
        mail.select("inbox")

        result, data = mail.search(None, "ALL")
        if result != "OK":
            return []

        email_ids = data[0].split()
        for email_id in email_ids[-limit:]:
            res, msg_data = mail.fetch(email_id, "(RFC822)")
            if res != "OK":
                continue

            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding or "utf-8")

                    sender = msg["From"]
                    date = msg["Date"]

                    body = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == "text/plain":
                                body = part.get_payload(decode=True).decode(errors="ignore")
                                break
                    else:
                        body = msg.get_payload(decode=True).decode(errors="ignore")

                    emails.append({
                        "subject": subject,
                        "sender": sender,
                        "date": date,
                        "body": body
                    })

        mail.logout()
    except Exception as e:
        print(f"Error fetching emails: {e}")

    return emails

@app.route('/emails', methods=['GET'])
def get_emails():
    emails = fetch_gmail_emails(limit=5)
    return jsonify(emails)

if __name__ == '__main__':
    app.run(debug=True)
