# Retours suite au POC

## Bien choisir les rôles en amont
Il est hyper important de bien réfléchir aux rôles en amont car cela impacte tout profondement derrière.

Raison 1 :
Etant donné que seul le rôle stipulé dans les header durant la requête fait loi d'authorisation, un utilisateur ayant plusieurs rôles peut voir sa requete refusé pour un certain rôle alors qu'il possède bien la permission dans un autre de ses rôles.

Raison 2 :
Si les permissions changent avec le temps, il faudra propager dans toutes les applications les nouveaux header qui possèdent lesdroits d'accès (lecture / écriture) sur les ressources

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
Dans cet exemple si mon rôle possède le droit de lister les books mais n'a pas le droit de lister les user (author) alors celretournera une erreur

## Customiser les plugins keycloak est possible mais peut être complexe
Les dépendances supplémentaires sont assez complexe à installer (avis d'une personne n'ayant pas fait de java depuis un moment)

Si on souhaite ajouter des dépendances en plus dans le plugin keycloak :
- https://stackoverflow.com/questions/46205475/keycloak-extension-with-dependencies

## Pour aller plus loin
Pour mieux comprendre les rôles :
- https://stackoverflow.com/questions/60963627/can-someone-forge-a-request-to-hasura-graphql-engine-by-setting-x-hasura-role
