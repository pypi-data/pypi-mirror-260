from unittest import TestCase

from src.eam_onb_helper.common import CommonBuilder
from eightam_db_helper.src.eam_db_helper.db import DatabaseHelper



class CosmosClientMock:
    def __init__(self, uri, key):
        self.results = []

    def get_database_client(self, database):
        return self

    def get_container_client(self, container):
        return self

    def query_items(self, query: str, parameters: list = None, enable_cross_partition_query: bool=False):
        results = self.results
        self.results = []

        return results

    def upsert_item(self, body):        
        self.results.append(body)
        return body
    
    def delete_item(self, item_id, partition_key):
        self.results = None
    

database = DatabaseHelper(
    {
        'account_uri': 'test_uri',
        'key': 'test_key',
        'db_name': 'test_database',
        'container_name': 'test_container'
    }, 
    CosmosClientMock
  )


common_builder = CommonBuilder(
    database,
    {
        'vendor_id': 'test_vendor_id',
        'vendor_name': 'test_vendor_name',
        'vendor_address': 'test_vendor_address',
        'vendor_phone': 'test_vendor_phone',
        'vendor_icon': 'test_vendor_icon',
        'vendor_admin': 'test_vendor_admin',
        'vendor_overall_rating': 'test_vendor_overall_rating',
        'vendor_subscription_type': 'test_vendor_subscription_type',
        'vendor_dates': 'test_vendor_dates',
        'employer_id': 'test_employer_id',
        'employer_name': 'test_employer_name',
        'employer_address': 'test_employer_address',
        'employer_phone': 'test_employer_phone',
        'employer_icon': 'test_employer_icon',
        'employer_admin': 'test_employer_admin'
    }
)


# Test the build_vendor_list method
class TestCommonBuilder(TestCase):
    def test_build_vendor_list(self):
        database.client.results = [{'id': '1', 'itemType': 'template'}]
        vendor_list = common_builder.build_vendor_list()
        self.assertEqual(vendor_list, {
            'id': common_builder.item_id,
            'vendorId': 'test_vendor_id',
            'vendorName': 'test_vendor_name',
            'vendorAddress': 'test_vendor_address',
            'vendorPhone': 'test_vendor_phone',
            'vendorIcon': 'test_vendor_icon',
            'vendorAccountAdmin': 'test_vendor_admin',
            'vendorOverallRating': 'test_vendor_overall_rating',
            'vendorSubscriptionType': 'test_vendor_subscription_type',
            'vendorDates': 'test_vendor_dates',
            'employerId': 'test_employer_id',
            'employerName': 'test_employer_name',
            'employerAddress': 'test_employer_address',
            'employerPhone': 'test_employer_phone',
            'employerIcon': 'test_employer_icon',
            'employerAccountAdmin': 'test_employer_admin',
            'type': 'vendorList'
        })
    