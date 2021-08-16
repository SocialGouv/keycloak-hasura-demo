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

Afin d'assurer une connexion entre Hasura et Keycloak, il est nécessaire de préconfigurer Keycloak (Realm, client, mappers ...). Pour ce faire, il suffit lancer le script d'initialisation de keycloak comme ci-dessous.
```bash
cd dev
pip3 install requests python-keycloak
python3 init_keycloak.py
```

### Github auth

Vous pouvez créer un auth provider sous Keycloak en suivant les étapes suivantes :

1. Créer une app sur github (https://github.com/settings/developers)

    Homepage url: http://localhost:8081/auth/realms/hasura

    Authorization callback url: http://localhost:8081/auth/realms/hasura/broker/github/endpoint

2. Créer un auth provider de type github sous keycloak en fournissant les secrets key dans l'interface
  

Plus d'info ici :
- https://medium.com/keycloak/github-as-identity-provider-in-keyclaok-dca95a9d80ca


## Configurer Hasura

Ouvrir hasura et entrer le mot de passe dans le docker-compose

Voici les étapes à réaliser dans hasura :
- Ouvrir les options (avec le bouton en haut à droite de la page)
- Accéder à l'onglet "Metadata Actions"
- Cliquer sur le bouton "Import metadata" puis importer le fichier hasura_metadata.json situé dans "./dev/hasura"
- Importer les fichiers de migration en suivant la documentation [Ici](hasura.md)

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
  update_user_by_pk(pk_columns: {id: "7d3a9671-381b-442a-b720-2d59ef5bbce6"}, _set: { first_name: "KEVIN" }) {
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

## Lancer l'application

Premièrement il faut installer les dépendances du frontend en local :
```bash
npm install
```

Vous pouvez maintenant lancer le frontend en lançant la commande suivante :
```bash
npm start
```

## Accéder aux différents composants

Voici les urls des différents composants :

```
Keycloak : http://localhost:8081
Hasura   : http://localhost:8080
Frontend : http://localhost:8082
```

Pour aller plus loin avec l'application :
- [Comment fonctionne l'application ?](app.md)
