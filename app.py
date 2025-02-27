from flask import Flask, jsonify, request
try:
    from imap_sync import fetch_and_index_emails
    from ai_categorization import categorize_email
    from elasticsearch_util import search_emails
    from integrations import send_slack_notification, trigger_webhook
except ImportError as e:
    print(f"Error importing modules: {e}")
    fetch_and_index_emails = None
    categorize_email = None
    search_emails = None
    send_slack_notification = None
    trigger_webhook = None

app = Flask(__name__)


@app.route('/sync-emails', methods=['GET'])
def sync_emails():
    try:
        username = request.args.get('username')
        password = request.args.get('password')
        imap_server = request.args.get('imap_server')
        
        
        if not username or not password or not imap_server:
            return jsonify({"error": "Missing required parameters"}), 400


        if fetch_and_index_emails is None:
            return jsonify({"error": "fetch_and_index_emails function is not available"}), 500

        
        emails = fetch_and_index_emails(username, password, imap_server)
        return jsonify(emails), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/categorize-email', methods=['POST'])
def categorize():
    try:
        email_body = request.json.get('body')
        if not email_body:
            return jsonify({"error": "Email body is missing"}), 400

        
        if categorize_email is None:
            return jsonify({"error": "categorize_email function is not available"}), 500

        
        category = categorize_email(email_body)
        return jsonify({"category": category}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/slack-notify', methods=['POST'])
def slack_notify():
    try:
        subject = request.json.get('subject')
        slack_token = request.json.get('slack_token')
        slack_channel = request.json.get('slack_channel')
        
        
        if not subject or not slack_token or not slack_channel:
            return jsonify({"error": "Missing required parameters"}), 400

        
        if send_slack_notification is None:
            return jsonify({"error": "send_slack_notification function is not available"}), 500

        
        send_slack_notification(subject, slack_token, slack_channel)
        return jsonify({"status": "Notification sent"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/trigger-webhook', methods=['POST'])
def trigger():
    try:
        email_data = request.json.get('email')
        if not email_data:
            return jsonify({"error": "Email data is missing"}), 400

        
        if trigger_webhook is None:
            return jsonify({"error": "trigger_webhook function is not available"}), 500

        
        trigger_webhook(email_data)
        return jsonify({"status": "Webhook triggered"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/search-emails', methods=['GET'])
def search():
    try:
        query = request.args.get('query')
        if not query:
            return jsonify({"error": "Search query is missing"}), 400


        if search_emails is None:
            return jsonify({"error": "search_emails function is not available"}), 500

        
        results = search_emails(query)
        return jsonify(results), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')  # Set host to 0.0.0.0 to allow external access in Codespaces
