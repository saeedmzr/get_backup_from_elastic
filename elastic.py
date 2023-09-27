from elasticsearch import Elasticsearch


class ElasticSearch:
    def __init__(self, es_host, es_port, es_index, es_username=None, es_password=None):
        if es_password is None or es_username is None:
            self.es = Elasticsearch([f'http://{es_host}:{es_port}'], timeout=120)
        else:
            self.es = Elasticsearch([f'http://{es_host}:{es_port}'], http_auth=(es_username, es_password), timeout=120)
        self.es_index = es_index

    def index_document(self, document, document_id=None):
        try:
            response = self.es.index(index=self.es_index, body=document, id=document_id)
            return response
        except Exception as e:
            # Handle any exceptions here, e.g., ElasticsearchException
            print(f"Failed to index document: {str(e)}")
            return None

    def receive_data(self, query):
        res = self.es.search(index=self.es_index, body=query)
        return res['hits']['hits']

    def create_snapshot(self, snapshot_repository, snapshot_name, snapshot_payload):
        return self.es.snapshot.create(repository=snapshot_repository, snapshot=snapshot_name, body=snapshot_payload)

    def create_index_if_not_exists(self):
        if not self.es.indices.exists(index=self.es_index):
            self.es.indices.create(index=self.es_index, mappings={})

    def bulk_insert_data(self, data_to_insert):
        self.create_index_if_not_exists()
        actions = [
            {
                "_op_type": "index",
                "_index": self.es_index,
                "_source": data,
            }
            for data in data_to_insert
        ]
        for data in data_to_insert:
            self.index_document(data['_source'])
        # success_count, failed_count = helpers.bulk(client=self.es, actions=actions, refresh=True)

        return True
