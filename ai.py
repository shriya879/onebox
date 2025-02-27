from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def train_email_classifier(training_data, labels, model_file='email_classifier.pkl'):
    try:
        vectorizer = TfidfVectorizer()
        X_train = vectorizer.fit_transform(training_data)
        classifier = MultinomialNB()
        classifier.fit(X_train, labels)
        with open(model_file, 'wb') as f:
            pickle.dump((vectorizer, classifier), f)
        logger.info("AI model training completed and saved.")
    except Exception as e:
        logger.error(f"Error training the classifier: {e}")

def load_email_classifier(model_file='email_classifier.pkl'):
    try:
        with open(model_file, 'rb') as f:
            vectorizer, classifier = pickle.load(f)
        logger.info("AI model loaded successfully.")
        return vectorizer, classifier
    except Exception as e:
        logger.error(f"Error loading the classifier: {e}")
        return None, None

def categorize_email(email_body, vectorizer, classifier):
    try:
        email_tfidf = vectorizer.transform([email_body])
        category = classifier.predict(email_tfidf)[0]
        return category
    except Exception as e:
        logger.error(f"Error categorizing the email: {e}")
        return None

if __name__ == "__main__":
    training_data = [
        "I'm interested in your product.",
        "Can we schedule a meeting next week?",
        "I am not interested at the moment.",
        "This is a spam email.",
        "I'm out of the office until next Monday."
    ]

    labels = [
        "Interested",
        "Meeting Booked",
        "Not Interested",
        "Spam",
        "Out of Office"
    ]

    train_email_classifier(training_data, labels)

    vectorizer, classifier = load_email_classifier()

    new_email_body = "I'd like to know more about your services. Can we book a meeting?"
    category = categorize_email(new_email_body, vectorizer, classifier)
    
    print(f"The email is categorized as: {category}")
