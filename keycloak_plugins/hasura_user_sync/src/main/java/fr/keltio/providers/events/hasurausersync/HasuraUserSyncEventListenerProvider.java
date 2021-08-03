/*
 * Copyright 2019 Red Hat, Inc. and/or its affiliates
 * and other contributors as indicated by the @author tags.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package fr.keltio.keycloak.providers.events.hasurausersync;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;

import java.lang.Exception;
import java.util.Map;
import java.util.Set;
import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.HttpClientBuilder;
import org.apache.http.entity.StringEntity;
import org.keycloak.events.Event;
import org.keycloak.events.EventListenerProvider;
import org.keycloak.events.EventType;
import org.keycloak.events.admin.AdminEvent;
import org.keycloak.events.admin.OperationType;
import org.keycloak.models.KeycloakSession;
import org.keycloak.models.RealmModel;
import org.keycloak.models.UserModel;


// "REGISTER"
// Exemple of event data :
// Event Occurred:{'type': 'REGISTER', 'realmId': '92540ba1-3bb9-4cb1-89e3-b6970cee033b', 'clientId': 'hasura-app', 'userId': 'eba06150-f89a-4164-9cc5-638ecc91aa37', 'ipAddress': '172.21.0.1', 'details': {'auth_method': 'openid-connect', 'auth_type': 'code', 'register_method': 'form', 'last_name': 'Titi', 'redirect_uri': 'http://localhost:8082/#/', 'first_name': 'Toto', 'code_id': 'fcfbec68-d73c-492d-88d8-4811feaf78ef', 'email': 'john@tot.com', 'username': 'username', }}
// "UPDATE_PROFILE"
// Event Occurred:{'type': 'UPDATE_PROFILE', 'realmId': '92540ba1-3bb9-4cb1-89e3-b6970cee033b', 'clientId': 'account', 'userId': 'eba06150-f89a-4164-9cc5-638ecc91aa37', 'ipAddress': '172.21.0.1' }
// "UPDATE_EMAIL"
// "CLIENT_REGISTER"

/**
 * @author <a href="mailto:kevin@keltio.fr">Kévin Didelot</a>
 */
public class HasuraUserSyncEventListenerProvider implements EventListenerProvider {
  private KeycloakSession session;
  private String hasuraServerUri;
  private String hasuraToken;

  public HasuraUserSyncEventListenerProvider(
    KeycloakSession session,
    String hasuraServerUri,
    String hasuraToken
  ) {
    this.session = session;
    this.hasuraServerUri = hasuraServerUri;
    this.hasuraToken = hasuraToken;
  }

  @Override
  public void onEvent(Event event) {
    // System.out.println("\n\nEvent Occurred:" + toString(event)); 
    if (event.getType() == EventType.REGISTER) {
      String userId        = event.getUserId();
      String userMail      = "";
      String username      = "";
      String userFirstName = "";
      String userLastName  = "";
      for (Map.Entry<String, String> e : event.getDetails().entrySet()) {
        if (e.getKey() == "email") {
          userMail = e.getValue();
        } else if (e.getKey() == "username") {
          username = e.getValue();
        } else if (e.getKey() == "last_name") {
          userLastName = e.getValue();
        } else if (e.getKey() == "first_name") {
          userFirstName = e.getValue();
        }
      }
      this.createUserOnHasura(userId, userMail, username, userFirstName, userLastName)   ;   
    } else if (event.getType() == EventType.UPDATE_PROFILE) {
      RealmModel realm = session.realms().getRealm(event.getRealmId());
      UserModel user   = session.users().getUserById(event.getUserId(), realm);

      String userId        = event.getUserId();
      String userMail      = user.getEmail();
      String username      = user.getUsername();
      String userFirstName = user.getFirstName();
      String userLastName  = user.getLastName();
      this.updateUserOnHasura(userId, userMail, username, userFirstName, userLastName);
    }
  }
  
  public void createUserOnHasura(String userId, String userMail, String username, String userFirstName, String userLastName) {
    String query = "mutation addUser {\\n"
    + "  insert_user(\\n"
    + "    objects: [\\n"
    + "      { id: \\\"" + userId + "\\\", email: \\\"" + userMail + "\\\", username: \\\"" + username + "\\\", last_name: \\\"" + userLastName + "\\\", first_name: \\\"" + userFirstName + "\\\" }\\n"
    + "    ]\\n"
    + "  ) {\\n"
    + "    returning {\\n"
    + "      id\\n"
    + "    }\\n"
    + "  }\\n"
    + "}\\n\\n";

    HttpClient httpClient = HttpClientBuilder.create().build();
    HttpPost request      = new HttpPost(this.hasuraServerUri);

    try {        
      StringEntity params = new StringEntity("{ \"query\": \"" + query + "\", \"operationName\": \"addUser\" }", "UTF-8");
      params.setContentType("text/plain");
      request.addHeader("content-type", "text/plain;charset=UTF-8");
      request.addHeader("Accept", "*/*");
      request.addHeader("x-hasura-admin-secret", this.hasuraToken);
      request.setEntity(params);

      HttpResponse response = httpClient.execute(request);
      BufferedReader rd = new BufferedReader(new InputStreamReader(
        response.getEntity().getContent()));
      String line = "";
      while ((line = rd.readLine()) != null) {
        System.out.println(line);
      }
    } catch (IOException e) {
      e.printStackTrace();
    }
  }

  public void updateUserOnHasura(String userId, String userMail, String username, String userFirstName, String userLastName) {
    String query = "mutation updateUser {\\n"
    + "  update_user_by_pk(pk_columns: {id: \\\"" + userId + "\\\"}, _set: { first_name: \\\""+ userFirstName + "\\\", last_name: \\\""+ userLastName + "\\\", username: \\\""+ username + "\\\", email: \\\""+ userMail + "\\\"}) {\\n"
    + "    id\\n"
    + "  }\\n"
    + "}\\n\\n";

    HttpClient httpClient = HttpClientBuilder.create().build();
    HttpPost request      = new HttpPost(this.hasuraServerUri);

    try {        
      StringEntity params = new StringEntity("{ \"query\": \"" + query + "\", \"operationName\": \"updateUser\" }", "UTF-8");
      params.setContentType("text/plain");
      request.addHeader("content-type", "text/plain;charset=UTF-8");
      request.addHeader("Accept", "*/*");
      request.addHeader("x-hasura-admin-secret", this.hasuraToken);
      request.setEntity(params);

      HttpResponse response = httpClient.execute(request);
      BufferedReader rd = new BufferedReader(new InputStreamReader(
        response.getEntity().getContent()));
      String line = "";
      while ((line = rd.readLine()) != null) {
        System.out.println(line);
      }
    } catch (IOException e) {
      e.printStackTrace();
    }
  }

  @Override
  public void onEvent(AdminEvent event, boolean includeRepresentation) {
    // if (event.getOperationType() == "UPDATE") {
    //   // TODO create user in hasura
    // } else {
    // }
    // System.out.println("Admin Event Occurred:" + toString(event));
  }

  private String toString(Event event) {
    StringBuilder sb = new StringBuilder();

    sb.append("{'type': '");
    sb.append(event.getType());
    sb.append("', 'realmId': '");
    sb.append(event.getRealmId());
    sb.append("', 'clientId': '");
    sb.append(event.getClientId());
    sb.append("', 'userId': '");
    sb.append(event.getUserId());
    sb.append("', 'ipAddress': '");
    sb.append(event.getIpAddress());
    sb.append("'");

    if (event.getError() != null) {
      sb.append(", 'error': '");
      sb.append(event.getError());
      sb.append("'");
    }
    sb.append(", 'details': {");
    if (event.getDetails() != null) {
      for (Map.Entry<String, String> e : event.getDetails().entrySet()) {
        sb.append("'");
        sb.append(e.getKey());
        sb.append("': '");
        sb.append(e.getValue());
        sb.append("', ");
      }
      sb.append("}}");
    }

    return sb.toString();
  }

  private String toString(AdminEvent adminEvent) {
    StringBuilder sb = new StringBuilder();

    sb.append("{'type': '");
    sb.append(adminEvent.getOperationType());
    sb.append("', 'realmId': '");
    sb.append(adminEvent.getAuthDetails().getRealmId());
    sb.append("', 'clientId': '");
    sb.append(adminEvent.getAuthDetails().getClientId());
    sb.append("', 'userId': '");
    sb.append(adminEvent.getAuthDetails().getUserId());
    sb.append("', 'ipAddress': '");
    sb.append(adminEvent.getAuthDetails().getIpAddress());
    sb.append("', 'resourcePath': '");
    sb.append(adminEvent.getResourcePath());
    sb.append("'");

    if (adminEvent.getError() != null) {
      sb.append(", 'error': '");
      sb.append(adminEvent.getError());
      sb.append("'");
    }
    sb.append("}");
  
    // Example of result :
    // Admin Event Occurred:{'type': 'UPDATE', 'realmId': 'master', 'clientId': 'cd5a380e-48e3-4b3d-947b-e8d7dbb5038a', 'userId': '1ab475d3-843f-4212-ace6-924f2556d170', 'ipAddress': '172.21.0.1', 'resourcePath': 'users/63a5a721-7426-4b79-9110-cd04b49c37b9'}
    return sb.toString();
  }

  @Override
  public void close() {}
}
