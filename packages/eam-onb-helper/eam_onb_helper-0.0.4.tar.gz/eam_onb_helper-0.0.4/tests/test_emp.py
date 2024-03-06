from unittest import mock, TestCase

from src.eam_onb_helper.emp import EmpBuilder
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


class TestEmpBuilder(TestCase):
    @mock.patch('uuid.uuid4', return_value='test_id')
    def test_format(self, mock_uuid4):
        emp_builder = EmpBuilder(database, ['test_company_name'])
        item = {
            'itemType': 'company'
        }
        formatted_item = emp_builder.format(item)
        self.assertEqual(formatted_item, {'id': 'test_id', 'type': 'company'})


    @mock.patch('random.choice', return_value={'name': 'test_name'})
    @mock.patch('random.randint', return_value=1234)
    def test_generate_sign_up_code(self, mock_choice, mock_randint):
        emp_builder = EmpBuilder(database, ['test_company_name'])
        sign_up_code = emp_builder.generate_sign_up_code()
        self.assertEqual(sign_up_code, 'test_name1234')


    @mock.patch('uuid.uuid4', return_value='test_company_id')
    @mock.patch('src.eam_onb_helper.emp.EmpBuilder.generate_sign_up_code', return_value='test_sign_up_code')
    @mock.patch('time.time', return_value=1234)
    def test_build_company(self, mock_uuid4, mock_generate_sign_up_code, mock_time):
        database.client.results = [{'itemType': 'test_item_type', 'dates': {'added': 1234}}]
        emp_builder = EmpBuilder(database, ['test_company_name', 'test_is_demo', 'test_website', 'test_street', 'test_city', 'test_province', 'test_postal_code', 'test_country', 'test_office', 'test_phone', '', '', '', 'test_email'])

        company = emp_builder.build_company()

        self.assertEqual(company, {
            'id': 'test_company_id',
            'type': 'company',
            'name': 'test_company_name',
            'accountType': 'employer',
            'email': 'test_email',
            'isDemo': 'test_is_demo',
            'signUpCode': 'test_sign_up_code',
            'website': 'test_website',
            'address': {
                'street': 'test_street',
                'city': 'test_city',
                'province': 'test_province',
                'postalCode': 'test_postal_code',
                'country': 'test_country',
                'office': 'test_office'
            },
            'phone': 'test_phone',
            'dates': {'added': 1234}
        })


    @mock.patch('uuid.uuid4', return_value='test_company_id')
    @mock.patch('src.eam_onb_helper.emp.EmpBuilder.format', return_value={'type': 'test_item_type'})
    def test_build_tags(self, mock_uuid, mock_format):
        database.client.results = [{'type': 'test_item_type'}]
        emp_builder = EmpBuilder(database, ['test_company_name'])
        tags = emp_builder.build_tags()
        self.assertEqual(tags, {'companyId': 'test_company_id', 'type': 'test_item_type'})


    @mock.patch('uuid.uuid4', return_value='test_company_id')
    @mock.patch('src.eam_onb_helper.emp.EmpBuilder.format', return_value={'type': 'test_item_type'})
    def test_build_employer_doc_config(self, mock_uuid, mock_format):
        database.client.results = [{'type': 'test_item_type'}]
        emp_builder = EmpBuilder(database, ['test_company_name'])
        employer_doc_config = emp_builder.build_employer_doc_config()
        self.assertEqual(employer_doc_config, {'type': 'test_item_type', 'employerId': 'test_company_id', 'employerName': 'test_company_name'})        

