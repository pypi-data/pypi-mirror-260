import uuid
import time
import random
import geonamescache


class VendBuilder:
  def __init__(self, db, company_data: list) -> None:
    self.company_id = str(uuid.uuid4())
    self.company_name = company_data[0]
    self.db = db
    self.company_data = company_data

  
  def format(self, item) -> dict:
    item['id'] = str(uuid.uuid4())
    item['type'] = item['itemType']

    if item['type'] != 'company':
      item['vendorId'] = self.company_id
      item['vendorName'] = self.company_name

    del item['itemType']

    return item
  

  def generate_sign_up_code(self) -> str:
    gc = geonamescache.GeonamesCache()
    counties = gc.get_us_counties()
    random_county = random.choice(counties)["name"].split(" ")[0]
    random_number = str(random.randint(0, 9999))

    return random_county + random_number

  
  def build_company(self) -> dict:
    company = self.db.get_result(query="SELECT * FROM c WHERE c.type = 'template' AND c.itemType = 'company'")

    company['name'] =  self.company_name
    company['email'] = self.company_data[14]
    company['isDemo'] = self.company_data[1]  
    company['signUpCode'] = self.generate_sign_up_code() 
    company['subscriptionType'] = self.company_data[2]        
    company['website'] = self.company_data[3]
    company['address'] = {
      'street': self.company_data[4],
      'city': self.company_data[5],
      'province': self.company_data[6],
      'postalCode': self.company_data[7],
      'country': self.company_data[8],
      'office': self.company_data[9]
    }
    company['phone'] = self.company_data[10]
    company['dates']['added'] = int(time.time())

    company = self.format(company)

    company['id'] = self.company_id
    return company


  def build_profile_state(self) -> dict:
    return self.format(self.db.get_result(query="SELECT * FROM c WHERE c.type = 'template' AND c.itemType = 'vendorPreQualProfileState'"))


  def build_payment_state(self) -> dict:
    return self.format(self.db.get_result(query="SELECT * FROM c WHERE c.type = 'template' AND c.itemType = 'vendorPreQualPaymentState'"))
  

  def build_documents_state(self) -> dict:
    return self.format(self.db.get_result(query="SELECT * FROM c WHERE c.type = 'template' AND c.itemType = 'vendorPreQualDocumentsState'"))


  def build_requirements_state(self) -> dict:
    return self.format(self.db.get_result(query="SELECT * FROM c WHERE c.type = 'template' AND c.itemType = 'vendorPreQualRequirementsState'"))


  def build_stepper_state(self) -> dict:
    return self.format(self.db.get_result(query="SELECT * FROM c WHERE c.type = 'template' AND c.itemType = 'vendorStepperState'"))


  ## Remove After Refactor
  def build_additional_requirements(self) -> list:
    additional_requirements = self.db.get_results(query="SELECT * FROM c WHERE c.type = 'additionalRequirement'")
    for item in additional_requirements:
      item["id"] = str(uuid.uuid4())
      item["type"] = "vendorAdditionalRequirement"
      item["text"] = item['text']
      item["defaultDocumentIdList"] = ["4270e05d-8339-4d13-b2ec-2f7a6848a063"]
      item["additionalRequirementId"] = item['id']
      item["vendorId"] = self.company_id
      item["isActive"] = False

    return additional_requirements


  def build_safety_stats(self) -> dict:
    safety_stats = self.format(self.db.get_result(query="SELECT * FROM c WHERE c.type = 'template' AND c.itemType = 'vendorSafetyStats'"))
    del safety_stats['vendorName']
    
    return safety_stats
  


      




