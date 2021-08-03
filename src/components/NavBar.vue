<template>
  <div class="navbar flex-space-between">
    <div class="cursor" @click="logout">Logout</div>
  </div>
</template>

<script>
import { keycloak } from "@/main.js";
export default {
  name: "NavBar",
  props: {
    userInfo: Object,
  },
  methods: {
    logout: function() {
      keycloak.logout();
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.navbar {
  padding: 10px 20px;
}
.cursor {
  cursor: pointer;
  text-decoration: none;
  color: black;
}
.cursor:hover {
  color: blue;
}
.flex-space-between {
  display: flex;
  text-align: right;
  flex-direction: column;
}
.margin-right {
  margin-right: 20px;
}
</style>
