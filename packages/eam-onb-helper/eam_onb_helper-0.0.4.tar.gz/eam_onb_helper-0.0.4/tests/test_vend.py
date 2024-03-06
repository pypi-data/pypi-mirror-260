from unittest import mock, TestCase

from src.eam_onb_helper.vend import VendBuilder
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


class TestVendBuilder(TestCase):
    @mock.patch('uuid.uuid4', return_value='test_id')
    def test_format(self, mock_uuid4):
        vend_builder = VendBuilder(database, ['test_company_name'])
        item = {
            'itemType': 'company'
        }
        formatted_item = vend_builder.format(item)
        self.assertEqual(formatted_item, {'id': 'test_id', 'type': 'company'})


    @mock.patch('random.choice', return_value={'name': 'test_name'})
    @mock.patch('random.randint', return_value=1234)
    def test_generate_sign_up_code(self, mock_choice, mock_randint):
        vend_builder = VendBuilder(database, ['test_company_name'])
        sign_up_code = vend_builder.generate_sign_up_code()
        self.assertEqual(sign_up_code, 'test_name1234')


    @mock.patch('uuid.uuid4', return_value='test_company_id')
    @mock.patch('src.eam_onb_helper.vend.VendBuilder.generate_sign_up_code', return_value='test_signup_code')
    @mock.patch('time.time', return_value=123456)
    def test_build_company(self, mock_uuid4, mock_signup_code, mock_time):
        
        database.client.results = [{'dates': {'added': 123456}, 'itemType': 'company'}]
        vend_builder = VendBuilder(database, ['test_company_name', 'test_demo', 'test_subscription_type', 'test_website', 'test_street', 'test_city', 'test_province', 'test_postal_code', 'test_country', 'test_office', 'test_phone', '', '', '', 'test_email'])
        company = vend_builder.build_company()
        
        self.assertEqual(company, {
            'id': 'test_company_id',
            'name': 'test_company_name',
            'email': 'test_email',
            'isDemo': 'test_demo',
            'signUpCode': 'test_signup_code',
            'subscriptionType': 'test_subscription_type',
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
            'dates': {'added': 123456},
            'type': 'company'
        })


    @mock.patch('uuid.uuid4', return_value='test_company_id')
    def test_build_profile_state(self, mock_uuid4):
        database.client.results = [{
            "itemType": "vendorPreQualProfileState"
        }]   

        vend_builder = VendBuilder(database, ['test_company_name'])
        profile_state = vend_builder.build_profile_state()
        self.assertEqual(profile_state, {
            "id": "test_company_id",
            "type": "vendorPreQualProfileState",
            "vendorId": "test_company_id",
            "vendorName": "test_company_name",
        })     


    @mock.patch('uuid.uuid4', return_value='test_company_id')
    def build_payment_state(self, mock_uuid4):
        database.client.results = [{
            "itemType": "vendorPreQualPaymentState"
        }]   

        vend_builder = VendBuilder(database, ['test_company_name'])
        payment_state = vend_builder.build_payment_state()
        self.assertEqual(payment_state, {
            "id": "test_company_id",
            "type": "vendorPreQualPaymentState",
            "vendorId": "test_company_id",
            "vendorName": "test_company_name",
        })

    
    @mock.patch('uuid.uuid4', return_value='test_company_id')
    def test_build_documents_state(self, mock_uuid4):
        database.client.results = [{
            "itemType": "vendorPreQualDocumentsState"
        }]   

        vend_builder = VendBuilder(database, ['test_company_name'])
        documents_state = vend_builder.build_documents_state()
        self.assertEqual(documents_state, {
            "id": "test_company_id",
            "type": "vendorPreQualDocumentsState",
            "vendorId": "test_company_id",
            "vendorName": "test_company_name",
        })

    
    @mock.patch('uuid.uuid4', return_value='test_company_id')
    def test_build_requirements_state(self, mock_uuid4):
        database.client.results = [{
            "itemType": "vendorPreQualRequirementsState"
        }]   

        vend_builder = VendBuilder(database, ['test_company_name'])
        requirements_state = vend_builder.build_requirements_state()
        self.assertEqual(requirements_state, {
            "id": "test_company_id",
            "type": "vendorPreQualRequirementsState",
            "vendorId": "test_company_id",
            "vendorName": "test_company_name",
        })


    @mock.patch('uuid.uuid4', return_value='test_company_id')
    def test_build_stepper_state(self, mock_uuid4):
        database.client.results = [{
            "itemType": "vendorStepperState"
        }]   

        vend_builder = VendBuilder(database, ['test_company_name'])
        stepper_state = vend_builder.build_stepper_state()
        self.assertEqual(stepper_state, {
            "id": "test_company_id",
            "type": "vendorStepperState",
            "vendorId": "test_company_id",
            "vendorName": "test_company_name",
        })


    @mock.patch('uuid.uuid4', return_value='test_id')
    def test_build_additional_requirements(self, mock_uuid4):
        database.client.results = [{'text': 'test_text'}]
        vend_builder = VendBuilder(database, ['test_company_name'])
        additional_requirements = vend_builder.build_additional_requirements()
        
        self.assertEqual(additional_requirements, [{
            "id": "test_id",
            "type": "vendorAdditionalRequirement",
            "text": "test_text",
            "defaultDocumentIdList": ["4270e05d-8339-4d13-b2ec-2f7a6848a063"],
            "additionalRequirementId": "test_id",
            "vendorId": "test_id",
            "isActive": False
        }])


    @mock.patch('uuid.uuid4', return_value='test_id')
    def test_build_safety_stats(self, mock_uuid4):
        database.client.results = [{
            "itemType": "vendorSafetyStats",
            "vendorName": "test_company_name"
        }]
        vend_builder = VendBuilder(database, ['test_company_name'])
        safety_stats = vend_builder.build_safety_stats()
        self.assertEqual(safety_stats, {
            "id": "test_id",
            "type": "vendorSafetyStats",
            "vendorId": "test_id"
        })


