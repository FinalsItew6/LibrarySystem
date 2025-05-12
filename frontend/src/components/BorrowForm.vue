<template>
    <div class="p-4">
      <h2 class="text-xl font-semibold mb-2">Borrow Book</h2>
  
      <form @submit.prevent="borrowBook" class="space-y-2 max-w-md">
        <label>User:</label>
        <select v-model="form.user" class="input" required>
          <option v-for="user in users" :value="user.id" :key="user.id">{{ user.username }}</option>
        </select>
  
        <label>Book:</label>
        <select v-model="form.book" class="input" required>
          <option v-for="book in books" :value="book.id" :key="book.id">
            {{ book.title }} ({{ book.copies_available }} copies)
          </option>
        </select>
  
        <p v-if="selectedBook && selectedBook.copies_available === 0" class="text-red-600 text-sm">
          ❌ No copies available for this book.
        </p>
  
        <button type="submit" class="btn" :disabled="!canBorrow">Borrow</button>
      </form>
    </div>
  </template>
  
  <script>
  import { borrowBook, getBooks, getUsers } from '../services/api'
  
  export default {
    data() {
      return {
        form: { user: '', book: '' },
        users: [],
        books: []
      }
    },
    computed: {
      selectedBook() {
        return this.books.find(book => book.id === this.form.book) || null
      },
      canBorrow() {
        return this.form.user && this.form.book && this.selectedBook?.copies_available > 0
      }
    },
    async created() {
      const [usersRes, booksRes] = await Promise.all([getUsers(), getBooks()])
      this.users = usersRes.data
      this.books = booksRes.data
    },
    methods: {
      async borrowBook() {
        if (!this.canBorrow) return
  
        try {
          const res = await borrowBook({
            user: this.form.user,
            book: this.form.book,
            status: 'borrowed'
          })
          alert(`✅ Borrow successful! Transaction ID: ${res.data.id}`)
          this.form = { user: '', book: '' }
  
          const booksRes = await getBooks()
          this.books = booksRes.data
        } catch (error) {
          console.error('Borrow failed:', error)
          alert('❌ Borrow failed. Check Book/User selection.')
        }
      }
    }
  }
  </script>
  
  <style scoped>
  .input {
    @apply border w-full px-3 py-2 rounded;
  }
  .btn {
    @apply bg-purple-600 text-white px-4 py-2 rounded;
  }
  .btn:disabled {
    @apply bg-purple-300 cursor-not-allowed;
  }
  </style>
  
