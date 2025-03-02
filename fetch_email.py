import imaplib
import email
from email.header import decode_header

# Email account credentials
EMAIL_ACCOUNTS = [
    {
        "IMAP_SERVER": "imap.gmail.com",  # Gmail IMAP server
        "EMAIL_ACCOUNT": "shri8ya@gmail.com",
        "EMAIL_PASSWORD": "bilx lxyu eobi xwpx",
    },
    {
        "IMAP_SERVER": "imap.gmail.com",  # Outlook IMAP server
        "EMAIL_ACCOUNT": "shriya.ms389@gmail.com",
        "EMAIL_PASSWORD": "sjkb krmi fuvv odqw",
    }
]


def fetch_emails(imap_server, email_account, email_password):
    """Fetches emails from a given IMAP server."""
    print(f"\n🔹 Connecting to {imap_server} for {email_account}...\n")

    # Connect to the IMAP server
    mail = imaplib.IMAP4_SSL(imap_server)

    # Login to the account
    try:
        mail.login(email_account, email_password)
        print("✅ Logged in successfully!")
    except imaplib.IMAP4.error:
        print("❌ Login failed. Check your credentials.")
        return

    # Select the mailbox (INBOX)
    mail.select("inbox")

    # Search for all emails
    result, data = mail.search(None, "ALL")
    if result != "OK":
        print("❌ No emails found!")
        return

    email_ids = data[0].split()
    print(f"📩 Found {len(email_ids)} emails.")

    # Fetch latest 5 emails (change this as needed)
    for email_id in email_ids[-5:]:
        res, msg_data = mail.fetch(email_id, "(RFC822)")
        if res != "OK":
            print(f"⚠️ Failed to fetch email with ID: {email_id}")
            continue

        # Parse email content
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])

                # Decode email subject
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding or "utf-8")

                print(f"\n📌 Subject: {subject}")
                print(f"📤 From: {msg['From']}")
                print(f"📅 Date: {msg['Date']}")

                # Print email body (only plain text)
                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))

                        if content_type == "text/plain" and "attachment" not in content_disposition:
                            body = part.get_payload(decode=True).decode(errors="ignore")
                            print(f"📄 Body:\n{body}")
                            break
                else:
                    body = msg.get_payload(decode=True).decode(errors="ignore")
                    print(f"📄 Body:\n{body}")

    # Close the connection
    mail.logout()
    print(f"\n✅ Finished fetching emails from {email_account}\n")


# Run for both email accounts
for account in EMAIL_ACCOUNTS:
    fetch_emails(account["IMAP_SERVER"], account["EMAIL_ACCOUNT"], account["EMAIL_PASSWORD"])

