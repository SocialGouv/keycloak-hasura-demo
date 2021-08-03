import os
import requests
from keycloak import KeycloakAdmin


KEYCLOAK_ADMIN_USER               = os.environ.get('KEYCLOAK_ADMIN_USER', 'admin')
KEYCLOAK_ADMIN_PASSWORD           = os.environ.get('KEYCLOAK_ADMIN_PASSWORD', 'admin')
KEYCLOAK_URL                      = os.environ.get('KEYCLOAK_URL', 'http://localhost:8081/auth/')
KEYCLOAK_REALM                    = os.environ.get('KEYCLOAK_REALM', 'hasura')
KEYCLOAK_CLIENT                   = os.environ.get('KEYCLOAK_CLIENT', 'hasura-app')


def get_keycloak_admin_instance():
    return KeycloakAdmin(server_url=KEYCLOAK_URL,
                         username=KEYCLOAK_ADMIN_USER,
                         password=KEYCLOAK_ADMIN_PASSWORD,
                         realm_name="master",
                         verify=True)


def create_realm_auth_client(keycloak_admin):
    client_data = {
        'clientId': KEYCLOAK_CLIENT,
        'redirectUris': ['*'],
        'webOrigins': ['*'],
        'publicClient': True,
        'directAccessGrantsEnabled': True
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
                'access.token.claim': 'true',
                'claim.name': 'has_been_acknowledged',
                'id.token.claim': 'true',
                'user.attribute': 'has_been_acknowledged',
                'userinfo.token.claim': 'true',
                'jsonType.label': 'boolean'
            },
            'name': 'has_been_acknowledged',
            'protocol': 'openid-connect',
            'protocolMapper': 'oidc-usermodel-attribute-mapper'
        })
    except Exception as err:
        if '409' not in str(err):
            raise Exception(err)

    return auth_client


def init_keycloak():
    print('INIT KEYCLOAK')
    keycloak_admin_master = get_keycloak_admin_instance()
    keycloak_admin_master.create_realm(payload={
      "realm": KEYCLOAK_REALM,
      "enabled": True,
      "emailTheme": "poc",
      "registrationAllowed": True,
      "rememberMe": True,
      "resetPasswordAllowed": True
    }, skip_exists=True)

    print('  create realm OK')

    keycloak_admin_master.realm_name = KEYCLOAK_REALM
    create_realm_auth_client(keycloak_admin_master)
    print('  create realm auth client OK')

    print('END INIT KEYCLOAK')

init_keycloak()
