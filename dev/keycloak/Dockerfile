FROM jboss/keycloak:14.0.0

COPY hasurausersync-14.0.0.jar /opt/jboss/keycloak/standalone/deployments/
COPY standalone.xml /opt/jboss/keycloak/standalone/configuration/standalone.xml
COPY standalone-ha.xml /opt/jboss/keycloak/standalone/configuration/standalone-ha.xml
COPY domain.xml /opt/jboss/keycloak/domain/configuration/domain.xml
