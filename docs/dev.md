# Lancer et configurer le POC

## Lancer les composants
```bash
docker-compose up -d
```
Attendre que le keycloak démarre puis faire
```bash
docker-compose start hasura
```
Vérifier que les 4 containers sont up 

## Configurer keycloak
Se connecter au keycloak avec les identifiants du docker-compose.yml

Voici les étapes à réaliser dans keycloak :
- Créer un realm "hasura"                                                                                         (OK)
- Créer un client "hasura-app"                                                                                    (OK)
- Créer un user dans le realm hasura                                                                              (NOT OK)
- Dans le realm "hasura", créer les roles book_creator et book_reader                                             (NOT OK)
- Créer un groupe hasura-user avec les attributs suivant (nécessaire pour qu'Hasura puisse bien lire le token):   (NOT OK)
    Key: x-hasura-default-role                    Value: hasura-user
    Key x-hasura-allowed-roles                    Value: ['hasura-user', 'book_creator', 'book_reader']
- Ajouter les rôles souhaités à l'user
    Aller dans l'onglet groupe de la page de l'utilisateur et ajouter le dans le groupe que nous venons de créer.
    Aller dans les mappers du client et rajouter les mappers (voir les screens sur slack)
    MAPPER 1:
      Nom                        : x-hasura-default-role
      Mapper type                : Hardcoded claim
      User attribute             : x-hasura-default-role 
      Token claim name           : https://hasura\.io/jwt/claims.x-hasura-default-role
      Claim value                : anonymous
      Claim json type            : String
      Add to ID token            : Off
      Add to access token        : On
      Add to userinfo            : Off
      Multivalued                : Off
      Aggregate attribute values : Off
    MAPPER 2:
      Nom                        : x-hasura-allowed-roles
      Mapper type                : User Client Role
      Client id                  : hasura-app
      User attribute             : x-hasura-allowed-roles 
      Multivalued                : On
      Token claim name           : https://hasura\.io/jwt/claims.x-hasura-allowed-roles
      Claim json type            : String
      Add to ID token            : Off
      Add to access token        : On
      Add to userinfo            : Off
      Aggregate attribute values : Off
    MAPPER 3:
      Nom                        : hasura-user-id
      Mapper type                : User property
      property                   : id 
      Token claim name           : https://hasura\.io/jwt/claims.x-hasura-user-id
      Claim json type            : String
      Add to ID token            : Off
      Add to access token        : On
      Add to userinfo            : Off
      Multivalued                : Off
      Aggregate attribute values : Off
- Ajouter le github identity provider
  LOCALHOST
  Client ID: 2c1962ecf6d85ecec939
  Client secret: 0727434888c6cea1a076a72954243697be002ac5

## Github auth
- Need to create an apps in github
  https://github.com/settings/developers
  Homepage url: http://localhost:8081/auth/realms/hasura
  Authorization callback url: http://localhost:8081/auth/realms/hasura/broker/github/endpoint
  https://medium.com/keycloak/github-as-identity-provider-in-keyclaok-dca95a9d80ca


## Configurer Hasura
Ouvrir hasura et entrer le mot de passe dans le docker-compose

Voici les étapes à réaliser dans hasura :
- Onglet Data
- Dans le schéma public, créer une table "books" avec les attributs suivants : "id (integer-autoincrement") primary key, name (Text), author (Text), publication_date (Text)"
- Ajouter les rôles et leurs permissions.
    - book_creator peut créer, update et delete    
    - book_reader peut select
    - hasura-user n'a aucunes permissions (pas obligatoire)

## Tester quelques commandes dans hasura

```graphql
query getBooks {
  books {
    id
    name
    creator {
      name
      id
    }
    publication_date
  }
}

mutation addBook {
  insert_books(
    objects: [
      { name: "Test", publication_date: "01/03/1994" }
    ]
  ) {
    returning {
      id
    }
  }
}

mutation updateUser {
  update_user_by_pk(pk_columns: {id: "7d3a9671-381b-442a-b720-2d59ef5bbce6"}, _set: { first_name: "PETER"}) {
		id
  }
}

mutation deleteBook {
  delete_books_by_pk (
  	id: 21
  ) {
  	id
  }
}

```

## France connect
### Pour s'authentifier via france connect
https://partenaires.franceconnect.gouv.fr/fcp/fournisseur-service

### Pour être fournisseur d'identité sur france connect
https://partenaires.franceconnect.gouv.fr/fcp/fournisseur-identite
