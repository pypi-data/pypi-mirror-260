from unittest import mock

from src.eam_b2c_helper.b2c import B2CHelper



# This method will be used by the mock to replace requests.post
def mocked_requests_post(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if args[0] == 'https://login.microsoftonline.com/90/oauth2/v2.0/token':
        return MockResponse({"access_token": "eyJ"}, 200)
    
    elif args[0] == 'https://graph.microsoft.com/beta/users':
        return MockResponse(
            {
              "@odata.context": "https://graph.microsoft.com/v1.0/$metadata#users/$entity",
              "id": "87d349ed-44d7-43e1-9a83-5f2406dee5bd",
              "businessPhones": [],
              "displayName": "Adele Vance",
              "givenName": "Adele",
              "jobTitle": "Product Marketing Manager",
              "mail": "AdeleV@contoso.com",
              "mobilePhone": "+1 425 555 0109",
              "officeLocation": "18/2111",
              "preferredLanguage": "en-US",
              "surname": "Vance",
              "userPrincipalName": "AdeleV@contoso.com"
            }, 
            201
        )

    return MockResponse(None, 404)


def mocked_requests_patch(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if args[0] == 'https://graph.microsoft.com/beta/users/test_id':
        return MockResponse("No Content", 204)

    return MockResponse(None, 404)


def mocked_requests_delete(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if args[0] == 'https://graph.microsoft.com/beta/users/test_id':
        return MockResponse("No Content", 204)

    return MockResponse(None, 404)



def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if args[0] == 'https://graph.microsoft.com/beta/users/test_id':
        return MockResponse(
            {
              "@odata.context": "https://graph.microsoft.com/v1.0/$metadata#users/$entity",
              "id": "87d349ed-44d7-43e1-9a83-5f2406dee5bd",
              "businessPhones": [],
              "displayName": "Adele Vance",
              "givenName": "Adele",
              "jobTitle": "Product Marketing Manager",
              "mail": "AdeleV@contoso.com",
              "mobilePhone": "+1 425 555 0109",
              "officeLocation": "18/2111",
              "preferredLanguage": "en-US",
              "surname": "Vance",
              "userPrincipalName": "AdeleV@contoso.com"
            }, 
            201
        )
    
    if args[0] == 'https://graph.microsoft.com/beta/users_filter_extension':
      return MockResponse(
          {
              '@odata.context': 'https://graph.microsoft.com/v1.0/$metadata#users',
              '@odata.nextLink': 'https://graph.microsoft.com/beta/users_filter_extension?$skiptoken=1',
              'value': [
                {
                  "displayName": "Conf Room Adams",
                  "id": "6ea91a8d-e32e-41a1-b7bd-d2d185eed0e0"
                },
                {
                  "displayName": "MOD Administrator",
                  "id": "4562bcc8-c436-4f95-b7c0-4f8ce89dca5e"
                }
              ]
          },
          200
      )
    
    if args[0] == 'https://graph.microsoft.com/beta/users_filter_extension?$skiptoken=1':
      return MockResponse(
          {
              '@odata.context': 'https://graph.microsoft.com/v1.0/$metadata#users',
              'value': [
                {
                  "displayName": "Conf Room Adams",
                  "id": "6ea91a8d-e32e-41a1-b7bd-d2d185eed0e0"
                },
                {
                  "displayName": "MOD Administrator",
                  "id": "4562bcc8-c436-4f95-b7c0-4f8ce89dca5e"
                }
              ]
          },
          200
      )
    
    if args[0] == "https://graph.microsoft.com/beta/users?$filter=extension_abc_OrganizationID eq '12345'":
      return MockResponse(
          {
              '@odata.context': 'https://graph.microsoft.com/v1.0/$metadata#users',
              'value': [
                {
                  "displayName": "Conf Room Adams",
                  "id": "6ea91a8d-e32e-41a1-b7bd-d2d185eed0e0"
                },
                {
                  "displayName": "MOD Administrator",
                  "id": "4562bcc8-c436-4f95-b7c0-4f8ce89dca5e"
                }
              ]
          },
          200
      )
    
    if args[0] == "https://graph.microsoft.com/beta/users?$filter=extension_abc_UserRoles eq 'Test Role'":
      return MockResponse(
          {
              '@odata.context': 'https://graph.microsoft.com/v1.0/$metadata#users',
              'value': [
                {
                  "displayName": "Conf Room Adams",
                  "id": "6ea91a8d-e32e-41a1-b7bd-d2d185eed0e0"
                },
                {
                  "displayName": "MOD Administrator",
                  "id": "4562bcc8-c436-4f95-b7c0-4f8ce89dca5e"
                }
              ]
          },
          200
      )
    
    if args[0] == "https://graph.microsoft.com/beta/users":
      return MockResponse(
          {
              '@odata.context': 'https://graph.microsoft.com/v1.0/$metadata#users',
              'value': [
                {
                  "displayName": "Conf Room Adams",
                  "id": "6ea91a8d-e32e-41a1-b7bd-d2d185eed0e0",
                  'mailNickname': 'Daveg_8amsolutions.com#EXT#'
                },
                {
                  "displayName": "MOD Administrator",
                  "id": "4562bcc8-c436-4f95-b7c0-4f8ce89dca5e",
                  'mailNickname': 'test@test.com'
                }
              ]
          },
          200
      )

    return MockResponse(None, 404)



token_request_data = {
  'grant_type': 'client_credentials',
  'user_mgmt_client_id': '12345',
  'scope': 'https://graph.microsoft.com/.default',
  'user_mgmt_client_secret': '678',
  'tenant_id': '90',
  'ext_app_client_id': 'abc'
}

b2c = B2CHelper(token_request_data)


# Test the get_token method
@mock.patch('requests.post', side_effect=mocked_requests_post)
def test_get_token(mock_post):
    assert b2c.get_token() == 'eyJ'


# Test the get_auth_header method
@mock.patch('requests.post', side_effect=mocked_requests_post)
def test_get_auth_header(mock_post):
    assert b2c.get_auth_header() == {
        'Authorization': 'Bearer eyJ',
        'Content-type': 'application/json',
    }


# Test the create_item method
@mock.patch('requests.post', side_effect=mocked_requests_post)
def test_create_item(mock_post):
    assert b2c.create_item(b2c.get_auth_header(), {'key1': 'value1'}).json() == {
      "@odata.context": "https://graph.microsoft.com/v1.0/$metadata#users/$entity",
      "id": "87d349ed-44d7-43e1-9a83-5f2406dee5bd",
      "businessPhones": [],
      "displayName": "Adele Vance",
      "givenName": "Adele",
      "jobTitle": "Product Marketing Manager",
      "mail": "AdeleV@contoso.com",
      "mobilePhone": "+1 425 555 0109",
      "officeLocation": "18/2111",
      "preferredLanguage": "en-US",
      "surname": "Vance",
      "userPrincipalName": "AdeleV@contoso.com"
    }


# Test the update_item method
@mock.patch('requests.post', side_effect=mocked_requests_post)
@mock.patch('requests.patch', side_effect=mocked_requests_patch)
def test_update_item(mock_post, mock_patch):
    assert b2c.update_item(b2c.get_auth_header(), {'passwordProfile': 'testPassword'}, 'test_id').json() == "No Content"


# Test the delete_item method
@mock.patch('requests.post', side_effect=mocked_requests_post)
@mock.patch('requests.delete', side_effect=mocked_requests_delete)
def test_delete_item(mock_post, mock_delete):
    assert b2c.delete_item(b2c.get_auth_header(), 'test_id').json() == "No Content"


# Test the get_user method
@mock.patch('requests.post', side_effect=mocked_requests_post)
@mock.patch('requests.get', side_effect=mocked_requests_get)
def test_get_user(mock_post, mock_get):
    assert b2c.get_user('test_id') == {
      "id": "87d349ed-44d7-43e1-9a83-5f2406dee5bd",
      "businessPhones": [],
      "displayName": "Adele Vance",
      "givenName": "Adele",
      "jobTitle": "Product Marketing Manager",
      "mail": "AdeleV@contoso.com",
      "mobilePhone": "+1 425 555 0109",
      "officeLocation": "18/2111",
      "preferredLanguage": "en-US",
      "surname": "Vance",
      "userPrincipalName": "AdeleV@contoso.com"
    }


# Test the compile_entire_user_list method
@mock.patch('requests.post', side_effect=mocked_requests_post)
@mock.patch('requests.get', side_effect=mocked_requests_get)
def test_compile_entire_user_list(mock_post, mock_get):
    assert b2c.compile_entire_user_list('_filter_extension') == [
        {
          "displayName": "Conf Room Adams",
          "id": "6ea91a8d-e32e-41a1-b7bd-d2d185eed0e0"
        },
        {
          "displayName": "MOD Administrator",
          "id": "4562bcc8-c436-4f95-b7c0-4f8ce89dca5e"
        },
        {
          "displayName": "Conf Room Adams",
          "id": "6ea91a8d-e32e-41a1-b7bd-d2d185eed0e0"
        },
        {
          "displayName": "MOD Administrator",
          "id": "4562bcc8-c436-4f95-b7c0-4f8ce89dca5e"
        }
      ]
    

# Test the get_users method
@mock.patch('requests.post', side_effect=mocked_requests_post)
@mock.patch('requests.get', side_effect=mocked_requests_get)
def test_get_users(mock_post, mock_get):
    assert b2c.get_users(company_id=12345) == [
        {
          "displayName": "Conf Room Adams",
          "id": "6ea91a8d-e32e-41a1-b7bd-d2d185eed0e0"
        },
        {
          "displayName": "MOD Administrator",
          "id": "4562bcc8-c436-4f95-b7c0-4f8ce89dca5e"
        }
      ]
    
    assert b2c.get_users(company_id=None, role_type='Test Role') == [
        {
          "displayName": "Conf Room Adams",
          "id": "6ea91a8d-e32e-41a1-b7bd-d2d185eed0e0"
        },
        {
          "displayName": "MOD Administrator",
          "id": "4562bcc8-c436-4f95-b7c0-4f8ce89dca5e"
        }
      ]
    

    assert b2c.get_users() == [
        {
          "displayName": "MOD Administrator",
          "id": "4562bcc8-c436-4f95-b7c0-4f8ce89dca5e",
          'mailNickname': 'test@test.com'
        }
      ]


# Test the create_user method
@mock.patch('requests.post', side_effect=mocked_requests_post)
def test_create_user(mock_post):
    assert b2c.create_user(
        {
              'key1': 'value1', 
              'role': '8amAdmin',
              'firstName': 'Dave',
              'lastName': 'G',
              'email': 'test@test.com',
              'phone': '1234567890',
              'company_id': '12345',
              'sign_up_code': '12345',
              'reset_password': False
          }, 'test_prefix'
    ).status_code == 201


# Test the create_users method
@mock.patch('requests.post', side_effect=mocked_requests_post)
def test_create_users(mock_post):
    
    test_list = b2c.create_users([
          {
              'key1': 'value1', 
              'role': '8amAdmin',
              'firstName': 'Dave',
              'lastName': 'G',
              'email': 'test@test.com',
              'phone': '1234567890',
              'company_id': '12345',
              'sign_up_code': '12345',
              'reset_password': False
          }, 
          {
              'key2': 'value2', 
              'role': 'Admin',
              'firstName': 'John',
              'lastName': 'Doe',
              'email': 'test@test.com',
              'phone': '1234567890',
              'company_id': '12345',
              'sign_up_code': '12345',
              'reset_password': True
          }
        ], 'test_prefix')
    
    for item in test_list:
        assert item.status_code == 201
 

# Test the update user method
@mock.patch('requests.post', side_effect=mocked_requests_post)
@mock.patch('requests.patch', side_effect=mocked_requests_patch)
def test_update_user(mock_post, mock_patch):
    assert b2c.update_user(
        {
              'id': 'test_id', 
              'role': '8amAdmin',
              'firstName': 'Dave',
              'lastName': 'G',
              'email': 'test@test.com',
              'phone': '1234567890',
              'company_id': '12345',
              'sign_up_code': '12345',
              'reset_password': False
          }, 'test_prefix'
    ).status_code == 204


# Test the update_users method
@mock.patch('requests.post', side_effect=mocked_requests_post)
@mock.patch('requests.patch', side_effect=mocked_requests_patch)
def test_update_users(mock_post, mock_patch):
    
    test_list = b2c.update_users([
        {
            'id': 'test_id', 
            'role': '8amAdmin',
            'firstName': 'Dave',
            'lastName': 'G',
            'email': 'test@test.com',
            'phone': '1234567890',
            'company_id': '12345',
            'sign_up_code': '12345',
            'reset_password': False
        }, 
        {
            'id': 'test_id', 
            'role': 'Admin',
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'test@test.com',
            'phone': '1234567890',
            'company_id': '12345',
            'sign_up_code': '12345',
            'reset_password': True
        }
      ], 'test_prefix'
    )

    for item in test_list:
      assert item.status_code == 204


# Test the delete_user method
@mock.patch('requests.post', side_effect=mocked_requests_post)
@mock.patch('requests.delete', side_effect=mocked_requests_delete)
def test_delete_user(mock_post, mock_delete):
    assert b2c.delete_user('test_id').status_code == 204

# Test the delete_users method
@mock.patch('requests.post', side_effect=mocked_requests_post)
@mock.patch('requests.delete', side_effect=mocked_requests_delete)
def test_delete_users(mock_post, mock_delete):
    test_list = b2c.delete_users(['test_id', 'test_id'])
    for item in test_list:
        assert item.status_code == 204