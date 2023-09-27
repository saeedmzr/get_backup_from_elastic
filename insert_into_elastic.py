import concurrent
from concurrent.futures import ProcessPoolExecutor

from elastic import ElasticSearch
from setting import ES_PASSWORD, ES_HOST, ES_USERNAME, ES_INDEX, ES_PORT, DESTINATION_ES_HOST, DESTINATION_ES_PORT, \
    DESTINATION_ES_INDEX


class InsertIntoElastic:

    def __init__(self):
        self.elastic = ElasticSearch(es_host=ES_HOST, es_port=ES_PORT, es_username=ES_USERNAME, es_password=ES_PASSWORD,
                                     es_index=ES_INDEX)
        self.destination_elastic = ElasticSearch(es_host=DESTINATION_ES_HOST, es_port=DESTINATION_ES_PORT,
                                                 es_index=DESTINATION_ES_INDEX)

    def get_data_and_write(self):
        size = 10000
        query = {
            "size": size,
            "query": {
                "match_all": {}
            }
        }
        response = self.elastic.receive_data(query=query)
        self.destination_elastic.bulk_insert_data(response)

    def multiple(self):
        with ProcessPoolExecutor(max_workers=12) as executor:
            futures = []

            for i in range(20):
                futures.append(executor.submit(self.get_data_and_write()))
                for future in concurrent.futures.as_completed(futures):
                    try:
                        message = future.result()
                        if message is not None:
                            pass
                    except Exception as e:
                        print(e)


myInstance = InsertIntoElastic()
myInstance.multiple()
