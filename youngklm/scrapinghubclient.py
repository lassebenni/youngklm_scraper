import logging

from scrapinghub import ScrapinghubClient

logger = logging.getLogger(__name__)


class ScrapingHubClient(ScrapinghubClient):
    _EVENTS_STORE = "events_store"
    EVENTS_KEY = "events_key"

    def __init__(self, api_key: str, project_id: int):
        super(ScrapingHubClient, self).__init__(api_key)
        self.project = self.get_project(project_id)

    def get_latest_job_for_project(self):
        latest_job_metadata = list(self.project.jobs.iter_last())[0]
        job_key = latest_job_metadata['key']
        latest_job = self.get_job(job_key)

        return latest_job

    def get_latest_items_for_project(self):
        items = self.get_latest_job_for_project().items
        return items.list()

    def get_key_val_store(self):
        collections = self.project.collections
        key_val_store = collections.get_store(self._EVENTS_STORE)
        return key_val_store

    def store_item_in_collections(self, key, value):
        self.get_key_val_store().set({
            '_key': key,
            'value': value
        })

    def list_all_items_in_collections(self):
        print(self.get_key_val_store().list())

    def get_stored_items(self, key):
        items = None
        try:
            items = self.get_key_val_store().get(key)['value']
        except Exception as e:
            pass
        return items
