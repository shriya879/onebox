from elasticsearch import Elasticsearch, helpers

def connect_elasticsearch():
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    return es

def create_index(es, index_name):
    if not es.indices.exists(index_name):
        es.indices.create(index=index_name, body={
            "mappings": {
                "properties": {
                    "subject": {"type": "text"},
                    "from": {"type": "keyword"},
                    "to": {"type": "keyword"},
                    "date": {"type": "date"},
                    "body": {"type": "text"}
                }
            }
        })
def index_email(es, index_name, email_data):
    es.index(index=index_name, document=email_data)

def search_emails(es, index_name, query):
    response = es.search(index=index_name, body={
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["subject", "body"]
            }
        }
    })
    return [hit["_source"] for hit in response['hits']['hits']]
