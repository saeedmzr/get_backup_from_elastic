import time
from datetime import datetime

import py7zr
from minio import Minio

from elastic import ElasticSearch
from setting import MINIO_HOST, MINIO_ACCESS_KEY, \
    MINIO_SECRET_KEY, MINIO_BUCKET_NAME, DESTINATION_ES_HOST, DESTINATION_ES_INDEX, DESTINATION_ES_PORT

# Minio configuration
minio_client = Minio(
    MINIO_HOST,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=True
)

# Elasticsearch configuration
snapshot_repository = 'my_repository2'
snapshot_name = f'snapshot_{datetime.now().strftime("%Y%m%d%H%M%S")}'


class DataProcessor:
    def __init__(self):
        self.elastic = ElasticSearch(es_host=DESTINATION_ES_HOST, es_port=DESTINATION_ES_PORT,
                                     es_index=DESTINATION_ES_INDEX)

    def make_snapshot(self):
        repository_payload = {
            'type': 'fs',
            'settings': {
                'location': '/usr/share/elasticsearch/snapshots'  # Specify the location for the repository
            }
        }

        snapshot_payload = {
            'indices': '_all',
            'ignore_unavailable': True,
            'include_global_state': False,
        }
        self.elastic.es.snapshot.create_repository(repository=snapshot_repository, name=snapshot_repository,
                                                   body=repository_payload)
        snapshot = self.elastic.create_snapshot(snapshot_repository, snapshot_name, snapshot_payload)
        print(snapshot)
        # Compress the snapshot into a 7-Zip archive
        time.sleep(10)
        archive_name = f'snapshot_{snapshot_name}.7z'
        source_directory = 'elasticsearch_snapshots'
        with py7zr.SevenZipFile(archive_name, 'w') as archive:
            archive.writeall(source_directory, '')

        # Upload the archive to Minio
        try:
            minio_client.fput_object(MINIO_BUCKET_NAME, archive_name, archive_name)
            print(
                f'Snapshot "{snapshot_name}" created and uploaded to Minio bucket "{MINIO_BUCKET_NAME}" as "{archive_name}"')
        except Exception as e:
            print(f'Error uploading the snapshot to Minio: {e}')


if __name__ == '__main__':
    data_processor = DataProcessor()
    data_processor.make_snapshot()
