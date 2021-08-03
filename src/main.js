import Vue from "vue";
import App from "./App.vue";
import VueLogger from "vuejs-logger";
import * as Keycloak from "keycloak-js";
import router from "./router";
import { ApolloClient } from "apollo-client";
import VueApollo from "vue-apollo";
import { HttpLink } from "apollo-link-http";
import { InMemoryCache } from "apollo-cache-inmemory";


Vue.config.productionTip = false;

// Logger configuration
const isProduction = process.env.NODE_ENV === "production";
const options = {
  isEnabled: true,
  logLevel: isProduction ? "error" : "debug",
  stringifyArguments: false,
  showLogLevel: true,
  showMethodName: true,
  separator: "|",
  showConsoleColors: true,
};
Vue.use(VueLogger, options);

Vue.mixin({
  methods: {
    goTo(route) {
      if (this.$route.path !== route) {
        this.$router.push(route);
      }
    },
  },
});

// Keycloak init options
const initOptions = {
  url: "http://localhost:8081/auth/",
  realm: "hasura",
  clientId: "hasura-app",
  onLoad: "login-required",
  promiseType: "native",
  flow: "implicit",
};

export const keycloak = Keycloak(initOptions);

export const updateKeycloakToken = async (timeBeforeForceRefresh) => {
  keycloak
    .updateToken(timeBeforeForceRefresh)
    .then((refreshed) => {
      if (refreshed) {
        Vue.$log.debug("Token refreshed" + refreshed);
        localStorage.setItem("vue-token", keycloak.token);
        localStorage.setItem("vue-refresh-token", keycloak.refreshToken);
      }
    })
    .catch(() => Vue.$log.error("Failed to refresh token"));
};

keycloak
  .init({ onLoad: initOptions.onLoad, promiseType: "native" })
  .then((auth) => {
    if (!auth) {
      window.location.reload();
    } else {
      Vue.$log.info("Authenticated");
    }

    const httpLink = new HttpLink({
      uri: "http://localhost:8080/v1/graphql",
      headers: {
        Authorization: `Bearer ${keycloak.token}`,
        'x-hasura-role': 'anonymous'
      },
    });
    const apolloClient = new ApolloClient({
      link: httpLink,
      connectToDevTools: true,
      cache: new InMemoryCache()
    });
    const apolloProvider = new VueApollo({
      defaultClient: apolloClient,
    });
    Vue.use(VueApollo);

    new Vue({ router, apolloProvider, render: (h) => h(App) }).$mount("#app");

    localStorage.setItem("vue-token", keycloak.token);
    localStorage.setItem("vue-refresh-token", keycloak.refreshToken);

    setInterval(() => {
      updateKeycloakToken(70);
    }, 30000);
  })
  .catch(() => {
    Vue.$log.error("Authenticated Failed");
  });
