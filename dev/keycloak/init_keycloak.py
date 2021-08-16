import os
import requests
from keycloak import KeycloakAdmin


KEYCLOAK_REALM_ANONYMOUS_GROUP = 'anonymous'
KEYCLOAK_ADMIN_USER = 'admin'
KEYCLOAK_ADMIN_PASSWORD = 'admin'
KEYCLOAK_URL = 'http://localhost:8081/auth/'
KEYCLOAK_SERVICE_ACCOUNT = 'user'
KEYCLOAK_SERVICE_ACCOUNT_PASSWORD = 'secret'
KEYCLOAK_REALM = 'hasura'
KEYCLOAK_CLIENT = 'hasura-app'


def get_keycloak_admin_instance():
    return KeycloakAdmin(server_url=KEYCLOAK_URL,
                         username=KEYCLOAK_ADMIN_USER,
                         password=KEYCLOAK_ADMIN_PASSWORD,
                         realm_name="master",
                         verify=True)

# This function will add the user we created to the group 'anonymous'
def group_user_add(admin_token, user_id, group_id):

    url_to_put = '{}admin/realms/{}/users/{}/groups/{}'.format(
        KEYCLOAK_URL,
        KEYCLOAK_REALM,
        user_id,
        group_id
    )

    res = requests.put(
        url_to_put,
        headers={
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(admin_token['access_token'])
        }
    )

    if res.status_code != 204:
        print('Error')
        print(res.reason)
        raise Exception(res)

# This function will create an identity provider for github login
def create_idp(admin_token):

    url_to_post = '{}admin/realms/{}/identity-provider/instances'.format(
        KEYCLOAK_URL,
        KEYCLOAK_REALM
    )

    res = requests.post(
        url_to_post,
        headers={
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(admin_token['access_token'])
        },
        json={
            "config":{
                "useJwksUrl":"true",
                "syncMode":"IMPORT",
                "clientId":"2c1962ecf6d85ecec939",
                "acceptsPromptNoneForwardFromClient":"",
                "disableUserInfo":"",
                "hideOnLoginPage":"",
                "clientSecret":"0727434888c6cea1a076a72954243697be002ac5"
                },
            "alias":"github",
            "providerId":"github",
            "enabled":"true",
            "authenticateByDefault":"false",
            "firstBrokerLoginFlowAlias":"first broker login",
            "postBrokerLoginFlowAlias":"",
            "storeToken":"",
            "addReadTokenRoleOnCreate":"",
            "trustEmail":"",
            "linkOnly":""
        }
    )

    if res.status_code != 201:
        print('Error')
        print(res.reason)
        raise Exception(res)

# This function will create the group 'anonymous'
def create_realm_anonymous_group(keycloak_admin):
    realm_anonymous_group = keycloak_admin.get_group_by_path(
        '/{}'.format(KEYCLOAK_REALM_ANONYMOUS_GROUP))
    if not realm_anonymous_group:
        # Creating the group with the required attributes
        keycloak_admin.create_group({'name': KEYCLOAK_REALM_ANONYMOUS_GROUP, "attributes": {
                      "x-hasura-default-role": ["anonymous"],
                      "x-hasura-allowed-roles": ["anonymous##book-creator##book-reader"]
                    }})
    realm_anonymous_group = keycloak_admin.get_group_by_path(
        '/{}'.format(KEYCLOAK_REALM_ANONYMOUS_GROUP))

    return realm_anonymous_group

# This function will create the client with all the mappers we need
def create_realm_auth_client(keycloak_admin):
    client_data = {
        'clientId': KEYCLOAK_CLIENT,
        'redirectUris': ['*'],
        'webOrigins': ['*'],
        'publicClient': True
    }
    keycloak_admin.create_client(client_data, skip_exists=True)

    auth_client = None
    clients = keycloak_admin.get_clients()
    for client in clients:
        if client_data['clientId'] == client.get('clientId'):
            auth_client = client
            break

    if not auth_client:
        raise Exception('Fail to create auth client for company')

    try:
        keycloak_admin.add_mapper_to_client(client.get('id'), {
            'config': {
                'access.token.claim': "true",
                'access.tokenResponse.claim': "false",
                'claim.name': "https://hasura\\.io/jwt/claims.x-hasura-default-role",
                'claim.value': "anonymous",
                'id.token.claim': "false",
                'jsonType.label': "String",
                'userinfo.token.claim': "true"
            },
            'name': "x-hasura-default-role",
            'protocol': "openid-connect",
            'protocolMapper': "oidc-hardcoded-claim-mapper"
        })
        keycloak_admin.add_mapper_to_client(client.get('id'), {
            'config': {
                'access.token.claim': "true",
                'claim.name': "https://hasura\\.io/jwt/claims.x-hasura-allowed-roles",
                'id.token.claim': "false",
                'jsonType.label': "String",
                'multivalued': "true",
                'userinfo.token.claim': "true",
                'usermodel.clientRoleMapping.clientId': "hasura-app"
            },
            'name': "x-hasura-allowed-roles",
            'protocol': "openid-connect",
            'protocolMapper': "oidc-usermodel-client-role-mapper"
        })
        keycloak_admin.add_mapper_to_client(client.get('id'), {
            'config': {
                'access.token.claim': "true",
                'claim.name': "https://hasura\\.io/jwt/claims.x-hasura-user-id",
                'id.token.claim': "false",
                'jsonType.label': "String",
                'user.attribute': "id",
                'userinfo.token.claim': "true"
            },
            'name': "hasura-user-id",
            'protocol': "openid-connect",
            'protocolMapper': "oidc-usermodel-property-mapper"
        })
    except Exception as err:
        if '409' not in str(err):
            raise Exception(err)

    return auth_client


def init_keycloak():
    print('INIT KEYCLOAK')
    keycloak_admin_master = get_keycloak_admin_instance()
    keycloak_admin_master.create_realm(payload={"realm": KEYCLOAK_REALM, "enabled": True, "emailTheme": "louping",
                                                "registrationAllowed": True, "rememberMe": True, "resetPasswordAllowed": True}, skip_exists=True)
    print('  create realm OK')

    keycloak_admin_master.realm_name = KEYCLOAK_REALM
    service_account_id = keycloak_admin_master.create_user({"email": "{}@localhost.fr".format(KEYCLOAK_SERVICE_ACCOUNT),
                                                            "username": KEYCLOAK_SERVICE_ACCOUNT,
                                                            "firstName": "Kévin",
                                                            "lastName": "Didelot",
                                                            "enabled": True,
                                                            "credentials": [{"value": KEYCLOAK_SERVICE_ACCOUNT_PASSWORD, "type": "password"}]})
    print('  create service account OK')


    client = create_realm_auth_client(keycloak_admin_master)
    print('  create realm auth client OK')

    keycloak_admin_master.create_client_role(client.get('id'), {'name': 'book-reader', 'clientRole': True})
    keycloak_admin_master.create_client_role(client.get('id'), {'name': 'book-creator', 'clientRole': True})
    print('  create roles for client OK')

    anonymous_group = create_realm_anonymous_group(keycloak_admin_master)
    print('  create realm anonymous group OK')

    group_user_add(keycloak_admin_master.token, service_account_id, anonymous_group.get('id'))
    print('  add user to anonymous group OK')

    create_idp(keycloak_admin_master.token)
    print('  create identity provider OK')

    print('END INIT KEYCLOAK')


init_keycloak()
