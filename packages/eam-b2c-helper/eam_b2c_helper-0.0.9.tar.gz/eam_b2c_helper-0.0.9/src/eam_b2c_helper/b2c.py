import requests
import json
import logging

logger = logging.getLogger("azure")
logger.setLevel(logging.WARN)



def build_user_object(user_details: dict, extension_id: str, b2c_prefix: str) -> dict:
  
  
  if user_details['role'] == '8amAdmin':
    user_details['password'] = 'eightamAdmin!23'
  else:
    user_details['password'] = 'eightam!23'

  return {      
    "accountEnabled": True,
    "displayName": f"{user_details['firstName']} {user_details['lastName']}",
    "mailNickname": user_details['firstName'],
    "identities": [
      {
        "issuer": f"{b2c_prefix}.onmicrosoft.com",
        "issuerAssignedId": user_details['email'],
        "signInType": "emailAddress"
      }
    ],
    "passwordProfile" : {
      "forceChangePasswordNextSignIn": False,
      "password": user_details['password']
    },
    "mobilePhone": user_details['phone'],
    f"extension_{extension_id}_OrganizationID": user_details['company_id'],
    f"extension_{extension_id}_SignUpCode": user_details['sign_up_code'],
    f"extension_{extension_id}_UserRoles": user_details['role'],
    f"extension_{extension_id}_mustResetPassword": user_details['reset_password']  
  }


class B2CHelper:
  def __init__(self, token_request_data) -> None:
    self.token_request_data = {
      'grant_type': token_request_data['grant_type'],
      'client_id': token_request_data['user_mgmt_client_id'],
      'scope': token_request_data['scope'],
      'client_secret': token_request_data['user_mgmt_client_secret'],
      'b2c_tenant_id': token_request_data['tenant_id'],
      'extension_id': token_request_data['ext_app_client_id']
    }


  def get_token(self) -> str:
    return requests.post(
      f"https://login.microsoftonline.com/{self.token_request_data['b2c_tenant_id']}/oauth2/v2.0/token",
        data=self.token_request_data).json()['access_token'] 


  def get_auth_header(self) -> dict:
    return {
      'Authorization': f'Bearer {self.get_token()}',
      'Content-type': 'application/json',
    }
  

  def create_item(self, auth_header: dict, item: dict) -> requests.Response:     
    return requests.post(
      "https://graph.microsoft.com/beta/users", 
      headers=auth_header,
      data=json.dumps(item)
    )

  
  def update_item(self, auth_header: dict, item: dict, id: str) -> requests.Response:
    del item['passwordProfile']    
    return requests.patch(
      f"https://graph.microsoft.com/beta/users/{id}",
      headers=auth_header,
      data=json.dumps(item)
    )
      
  
  def delete_item(self, auth_header: dict, user_id: dict) -> requests.Response:
    return requests.delete(f"https://graph.microsoft.com/beta/users/{user_id}",
      headers=auth_header
    )


  def get_user(self, user_id: str) -> dict:
    user = requests.get(f"https://graph.microsoft.com/beta/users/{user_id}", headers=self.get_auth_header()).json() 
    del user["@odata.context"]
    return user


  def compile_entire_user_list(self, filter_extension: str) -> list:
    users = requests.get(f"https://graph.microsoft.com/beta/users{filter_extension}", headers=self.get_auth_header())

    if '@odata.nextLink' in users.json():      
      next_link = users.json()["@odata.nextLink"]      
    else:
      next_link = None
    
    return_list = users.json()['value']

    while next_link is not None:           
      
      users_next = requests.get(
        next_link,      
        headers=self.get_auth_header(),
      )

      for user in users_next.json()['value']:      
        return_list.append(user)
    
      if '@odata.nextLink' in users_next.json():
        next_link = users_next.json()["@odata.nextLink"]
      else:
        next_link = None
        
    return return_list


  def get_users(self, company_id: str=None, role_type: str=None) -> list:
    if company_id is not None:      
      filter_extension = f"?$filter=extension_{self.token_request_data['extension_id']}_OrganizationID eq '{company_id}'"
      users = self.compile_entire_user_list(filter_extension)

    elif role_type is not None:      
      filter_extension = f"?$filter=extension_{self.token_request_data['extension_id']}_UserRoles eq '{role_type}'"
      users = self.compile_entire_user_list(filter_extension)
    
    else:           
      filter_extension = ''      
      users = [x  for x in self.compile_entire_user_list(filter_extension) if x['mailNickname'] != 'Daveg_8amsolutions.com#EXT#']

    return users


  def create_user(self, user_details: dict, b2c_prefix: str) -> dict:
    user = build_user_object(user_details, self.token_request_data['extension_id'], b2c_prefix)
    return self.create_item(self.get_auth_header(), user)


  def create_users(self, user_details_list: list, b2c_prefix: str) -> list:   
    auth_header = self.get_auth_header()
    results = []
    for user_detail in user_details_list:
      user = build_user_object(user_detail, self.token_request_data['extension_id'], b2c_prefix)
      results.append(self.create_item(auth_header, user))
    return results


  def update_user(self, user_details: dict, b2c_prefix: str) -> dict:
    user = build_user_object(user_details, self.token_request_data['extension_id'], b2c_prefix)  
    return self.update_item(self.get_auth_header(), user, user_details['id'])  


  def update_users(self, user_details_list: list, b2c_prefix: str) -> list:    
    auth_header = self.get_auth_header()
    results = []
    for user_detail in user_details_list:
      user = build_user_object(user_detail, self.token_request_data['extension_id'], b2c_prefix)
      results.append(self.update_item(auth_header, user, user_detail['id']))
    return results


  def delete_user(self, user_id: str) -> dict:
    return self.delete_item(self.get_auth_header(), user_id)


  def delete_users(self, user_id_list) -> list:
    ## Add code to delete by companyId  
    auth_header = self.get_auth_header() 
    results = [] 
    for user_id in user_id_list:
      results.append(self.delete_item(auth_header, user_id))
    return results
  