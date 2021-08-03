## Se connecter
En lançant l'application, une interface keycloak s'affichera en vous demandant des identifiants.
Vous pouvez soit vous inscrire, soit vous connecter avec l'user que nous avons généré: 
- Username: user
- Password: secret

## Changer le rôle d'un utilisateur
Si vous voulez ajouter ou supprimer un rôle d'un utilisateur, voici les étapes à suivre:
- Accéder au keycloak avec les identifiants du docker-compose
- Sélectionner le realm "Hasura"
- Accéder à l'onglet "Users"
- Cliquer sur "View all users"
- Cliquer sur l'id de l'user désiré
- Accéder à la sectiion "Role Mappings"
- Sélectionner le client "hasura-app"
- Ici vous verrez une colonne "Available Roles" avec les rôles book_reader et book_creator puis une colonne "Assigned Roles".
- Pour ajouter un certain rôle à l'utilisateur, il faut cliquer sur un rôle dans "Available Roles" puis cliquer sur "Add selected".
- Vous pourrez constater que le rôle se déplacera dans la colonne "Assigned Roles".

Le rôle est maintenant ajouté à l'utilisateur! 

Pour supprimer un rôle il suffit de le sélectionner dans la colonne "Assigned Roles" puis cliquer sur "Remove selected".
