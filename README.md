# POC Keycloak Hasura

- [Cadrage du POC](docs/poc.md)
- [Retours suite au POC](docs/feedback.md)
- [Manipuler en local le POC](docs/dev.md)
- [France connect avec Keycloak](docs/france-connect.md)

## Todo

- [ ] Events SPI :
  - [ ] setup dev/publish workflow : dedicated GH repo keycloak-user-webhook with semantic-release
  - [ ] use configurable webhook with `getUserById` payload instead of graphql
  - [ ] webhook : use an hasura action with token verificaiton
  - [ ] enable at keycloak init
- [ ] K8s integration
