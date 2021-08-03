<template>
  <div id="app" v-if="isLoaded">
    <NavBar :userInfo="userInfo" />
    <router-view :userInfo="userInfo" />
  </div>
</template>

<script>
import NavBar from "./components/NavBar.vue";
import { keycloak } from "@/main.js";

export default {
  name: "App",
  components: {
    NavBar,
  },
  data() {
    return {
      isLoaded: false,
      userInfo: null,
    };
  },
  async created() {
    this.userInfo = await keycloak.loadUserInfo();
    this.isLoaded = true;
  },
};
</script>

<style>
html, body, #app {
  height: 100%;
  margin: 0;
}
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin: 0;
}
</style>
