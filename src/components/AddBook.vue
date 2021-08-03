<template>
  <form @submit="submit">
    <input type="text" placeholder="Name" v-model="name" />
    <input
      type="text"
      placeholder="Publication Date"
      v-model="publication_date"
    />
    <button class="button-primary button" type="submit">Create</button>
  </form>
</template>

<script>
import gql from "graphql-tag";
const ADD_BOOK = gql`
  mutation addBook(
    $name: String!
    $publication_date: String!
  ) {
    insert_books(
      objects: [
        { name: $name, publication_date: $publication_date }
      ]
    ) {
      returning {
        id
      }
    }
  }
`;
export default {
  name: "AddBook",
  data() {
    return {
      name: "",
      publication_date: ""
    };
  },
  apollo: {
  },
  methods: {
    async submit(e) {
      e.preventDefault();
      const { name, publication_date } = this.$data;
      await this.$apollo.mutate({
        mutation: ADD_BOOK,
        variables: {
          name,
          publication_date
        },
        context: {
          headers: {
            'x-hasura-role': 'book-creator'
          },
        },
        refetchQueries: ["getBooks"]
      });
      this.name = ""
      this.publication_date = ""
    }
  }
};
</script>

<style scoped>
input {
  display: block;
  margin: auto;
  height: 20px;
  border: 1px solid #cccccc;
  border-radius: 2px;
  padding: 15px 10px;
  margin-bottom: 10px;
  width: 100%;
  box-sizing: border-box;
}
.button {
  font-size: 15px;
  background-color: #2f56ff;
  border-radius: 5px;
  padding: 6px 20px;
  color: white;
  text-decoration: none;
  margin-left: 5px;
  margin-right: 5px;
  border: none;
  cursor: pointer;
}
.button:hover {
  background-color: white;
  color: #2f56ff; 
}
</style>
