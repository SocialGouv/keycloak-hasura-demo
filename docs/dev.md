# Lancer et configurer le POC

## Lancer les composants
```bash
docker-compose up -d
```

Vérifier que les 4 containers sont up 
```bash
docker ps
```

## Configurer keycloak
```bash
cd dev
python init_keycloak.py
```

## Github auth
- Need to create an apps in github
  https://github.com/settings/developers
  Homepage url: http://localhost:8081/auth/realms/hasura
  Authorization callback url: http://localhost:8081/auth/realms/hasura/broker/github/endpoint
  https://medium.com/keycloak/github-as-identity-provider-in-keyclaok-dca95a9d80ca


## Configurer Hasura
Ouvrir hasura et entrer le mot de passe dans le docker-compose

Voici les étapes à réaliser dans hasura :
- Ouvrir les options (avec le bouton en haut à droite de la page)
- Accéder à l'onglet "Metadata Actions"
- Cliquer sur le bouton "Import metadata" puis importer le fichier hasura_metadata.json situé dans "./dev/hasura"

Vous avez maintenant une base de données prête à l'emploi!

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

## Accéder à l'application
Pour lancer l'application:
```bash
npm install
```
```bash
npm start
```
Vous êtes maintenant sur l'application!
- [Comment fonctionne l'application ?](app.md)

## France connect
### Pour s'authentifier via france connect
https://partenaires.franceconnect.gouv.fr/fcp/fournisseur-service

### Pour être fournisseur d'identité sur france connect
https://partenaires.franceconnect.gouv.fr/fcp/fournisseur-identite
