<template>
  <div class="books-list">
    <div v-if="books.length">
      <table>
        <tr>
          <th width="60%">Name</th>
          <th width="30%">Creator</th>
          <th width="10%"></th>
        </tr>
        <tr v-for="book in books" :key="book.id">
          <td>{{ book.name }}</td>
          <td>{{ book.creator.username }}</td>
          <td class="delete" @click="deleteBook(book.id)">Delete</td>
        </tr>
      </table>
    </div>
    <div v-else>
      No books found
    </div>
  </div>
</template>

<script>
import gql from "graphql-tag";

const GET_BOOKS = gql`
  query getBooks {
    books {
      id
      name
      creator {
        username
        id
      }
      publication_date
    }
  }
`;

const DELETE_BOOK = gql`
mutation deleteBook($id: Int!) {
  delete_books_by_pk (
  	id: $id
  ) {
  	id
  }
}
`

export default {
  name: "BooksList",
  data() {
    return {
      books: [],
    };
  },
  apollo: {
    books: {
      query: GET_BOOKS,
      context : {
        headers: {
          'x-hasura-role': 'book-reader'
        },        
      }
    },
  },
  props: {
    userInfo: Object,
  },
  methods: {
    async deleteBook(bookId) {
      await this.$apollo.mutate({
        mutation: DELETE_BOOK,
        variables: {
          id: bookId,
        },
        context: {
          headers: {
            'x-hasura-role': 'book-creator'
          },
        },
        refetchQueries: ["getBooks"]
      });
    }
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
table {
  font-family: arial, sans-serif;
  border-collapse: collapse;
  margin: auto;
}

td, th {
  border-bottom: 1px solid #dddddd;
  text-align: left;
  padding: 8px;
  font-size: 15px;
}
th {
  font-weight: 600;
}

.delete {
  color: red;
  cursor: pointer;
}
</style>
