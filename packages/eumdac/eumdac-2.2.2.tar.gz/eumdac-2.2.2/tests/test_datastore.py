from eumdac.token import AccessToken
from eumdac.datastore import DataStore, DataStoreError
from eumdac.collection import Collection

from .base import DataServiceTestCase


class TestDataStore(DataServiceTestCase):
    def setUp(self):
        super().setUp()
        self.token = AccessToken(self.credentials)
        self.datastore = DataStore(token=self.token)

    def test_property_collections(self):
        collections = self.datastore.collections
        self.assertIsInstance(collections, list)
        self.assertIn("EO:EUM:DAT:MSG:HRSEVIRI", map(str, collections))
        self.assertIsInstance(collections[0], Collection)
