<template>
  <div class="hello">
    <h1>Welcome, {{ userInfo.name }}</h1>
    <div class="flex-space-between">
      <div class="flex">
        <h2>Books</h2>
        <books-list v-if="checkIfUserHasBookReaderRole()" />
        <div v-else>
          You don't have book reader permission to list all books
        </div>
      </div>
      <div class="flex">
        <h2>Create book</h2>
        <add-book v-if="checkIfUserHasBookCreatorRole()" />
        <div v-else>
          You don't have book creator permission to create a book
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import BooksList from "../components/BooksList.vue";
import AddBook from "../components/AddBook.vue";

export default {
  components: {
    BooksList,
    AddBook,
  },
  name: "Home",
  props: {
    userInfo: Object,
  },
  methods: {
    checkIfUserHasBookReaderRole() {
      return this.userInfo['https://hasura.io/jwt/claims'] &&
        this.userInfo['https://hasura.io/jwt/claims']['x-hasura-allowed-roles'] &&
        this.userInfo['https://hasura.io/jwt/claims']['x-hasura-allowed-roles'].includes('book-reader')
    },
    checkIfUserHasBookCreatorRole() {
      return this.userInfo['https://hasura.io/jwt/claims'] &&
        this.userInfo['https://hasura.io/jwt/claims']['x-hasura-allowed-roles'] &&
        this.userInfo['https://hasura.io/jwt/claims']['x-hasura-allowed-roles'].includes('book-creator')
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1 {
  color:#2f56ff;
}
.button {
  margin-top: 20px;
  font-size: 15px;
  background-color: #2f56ff;
  border-radius: 5px;
  padding: 6px 20px;
  color: white;
  text-decoration: none;
  margin-left: 5px;
  margin-right: 5px;
}
.flex-space-between {
  display: flex;
  padding: 0 100px;
  max-width: 1000px;
  margin: 50px auto 0 auto;
}
.flex {
  flex: 1;
  padding: 20px 40px;
}
</style>
