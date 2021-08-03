# POC keycloak hasura


## Description de l’application

L’application est composée d’un frontend en Vuejs et d’un backend en Hasura.
Pour gérer l’authentification et les autorisations nous utiliserons Keycloak.

Keycloak générera un token JWT qui contiendra les rôles de l’utilisateur.
De cette façon le backend Hasura devra vérifier dans le token si l’utilisateur a le droit de faire une requête, puis retournera les ressources si l’utilisateur est autorisé

Dans le backend Hasura nous allons créer une table :
Book : Une table qui contient une liste de livre (nom, createur, date de publication)
User : 

Dans keycloak nous allons créer deux rôles :
Book creator : Permet de créer, modifier et supprimer un livre
Book reader : Permet de lister les livres

De cette façon, sur le frontend, l’utilisateur devra pouvoir créer un livre uniquement s’il a le rôle livre creator et voir la liste des livres uniquement s’il a le rôle livre reader.

Le backend doit retourner une 401 si l’utilisateur qui fait la requête n’a pas les droits de faire la requête.

Pour des raisons de performances nous devons dupliquer les utilisateurs de Keycloak dans Hasura, il faudra donc faire en sorte que lorsqu’un utilisateur est créé sur l’interface de Keycloak que l'utilisateur soit créer aussi sur Hasura. Pour se faire il faudra vérifier s’il est possible de créer des webhooks sur Keycloak lorsqu’un utilisateur est créé. Sinon il faudra créer des classes Java et surcharger les classes de Keycloak.


## Les critères d’acceptation du POC

Si je ne suis pas authentifié sur le frontend, je dois être redirigé vers la page de connexion de Keycloak
Si je suis authentifié sur le frontend mais que je n’ai pas les rôles dans keycloak pour lister les livres alors ça m’affiche un message pour me dire qu je n’ai pas les droits
Si je suis authentifié sur le frontend mais que je n’ai pas les rôles dans keycloak pour créer un livre alors ça m’affiche un message pour me dire qu je n’ai pas les droits


## Les tâches réalisées

### Frontend

Créer une application vierge en vuejs qui :
- Redirige vers Keycloak si l’utilisateur n’est pas connecté
- Affiche les roles utilisateurs une fois connecté dans une partie dédié
- Permet de lister les livres d’éléments en fonction de ses droits sur Keycloak
- Permet de créer un livre en fonction de ses droits sur Keycloak

### Backend Hasura

Créer la base de données
Faire en sorte que le token de Keycloak avec les rôles fonctionne et retourne 401 si n’a pas le rôle et 200 si a le rôle (Transformation du jwt possible à faire directement dans la configuration de keycloak)

### Keycloak

Créer un event listener qui va détecter les changements sur les utilisateurs (création, mise à jour, suppression) et mettre à jour la base Hasura automatiquement.
https://stackoverflow.com/questions/57431092/keycloak-subscribe-events-like-create-user-to-trigger-a-webservice
https://www.keycloak.org/docs/latest/server_development/index.html#_events
https://github.com/keycloak/keycloak-quickstarts/tree/latest/event-listener-sysout
Créer un identity provider github dans le realm keycloak d'hasura
Créer un thème custom Keycloak

## Important à lire

Pour mieux comprendre les rôles :
- https://stackoverflow.com/questions/60963627/can-someone-forge-a-request-to-hasura-graphql-engine-by-setting-x-hasura-role
Retours suite au POC :
- Il est hyper important de bien réfléchir aux rôles en amont car cela impacte tout profondement derrière.
  Raison 1 :
  Etant donné que seul le rôle stipulé dans les header durant la requête fait loi d'authorisation, un utilisateur ayant plusieurs rôles peut voir sa requete refusé pour un certain rôle alors qu'il possède bien la permission dans un autre de ses rôles.
  Raison 2 :
  Si les permissions changent avec le temps, il faudra propager dans toutes les applications les nouveaux header qui possèdent les droits d'accès (lecture / écriture) sur les ressources
  Raison 3 :
  Si l'on souhaite faire des requêtes avec des foreign key, les rôles peuvent bloquer les requêtes
    Exemple :
      books {
        id
        name
        author {
          id
          name
        }
      }
    Dans cet exemple si mon rôle possède le droit de lister les books mais n'a pas le droit de lister les user (author) alors cela retournera une erreur

A avoir en tête lors de la création du plugin keycloak :
- Les dépendances supplémentaires sont assez complexe à installer (avis d'une personne n'ayant pas fait de java depuis un moment)

## Pour aller plus loin

- [Manipuler en local le POC](docs/dev.md)
