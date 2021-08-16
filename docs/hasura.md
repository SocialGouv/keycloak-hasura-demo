# Hasura

## Installation du cli
Afin d'installer le cli, il suffit de suivre la documentation ici : https://hasura.io/docs/latest/graphql/core/hasura-cli/install-hasura-cli.html

## Configuration du cli
Il est nécessaire de créer un fichier config.yaml afin de pouvoir utiliser le cli.

Voici les informations à mettre dans le fichier config.yaml
```yaml
version: 3
endpoint: http://localhost:8080
admin_secret: myadminsecretkey
```

## Création des fichiers de migration de la base de données
```bash
hasura migrate create "init" --from-server
```

## Import des migrations
```bash
hasura migrate apply
```
