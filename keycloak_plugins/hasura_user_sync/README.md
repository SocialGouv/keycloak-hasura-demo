# keycloak-hasura-user-sync-spi

A Keycloak SPI that sync user to hasura when user change events(REGISTER, UPDATE_EMAIL, UPDATE_PROFILE).

## Local requirement
- Maven

## Doc explaining how this plugin was created
- https://dev.to/adwaitthattey/building-an-event-listener-spi-plugin-for-keycloak-2044
- https://access.redhat.com/documentation/en-us/red_hat_single_sign-on/7.3/html/server_developer_guide/providers
- https://www.keycloak.org/docs-api/6.0/javadocs/org/keycloak/events/EventType.html

## Build
```bash
mvn clean install
```

## Deploy
Copy target/event-listener-mqtt-jar-with-dependencies.jar to {KEYCLOAK_HOME}/standalone/deployments

Edit standalone.xml, standalone-ha.xml, domain.xml to configure the plugin settings. Find the following section in the configuration:
```
<subsystem xmlns="urn:jboss:domain:keycloak-server:1.1">
    <web-context>auth</web-context>
```
And add below:

```
<spi name="eventsListener"> 
    <provider name="hasurausersync" enabled="true">
        <properties>
            <property name="hasuraUri" value="http://hasura:8080/v1/graphql"/>
            <property name="hasuraToken" value="<YOUR HASURA ADMIN TOKEN>"/>
        </properties>
    </provider>
</spi>
```

Restart the keycloak server.
