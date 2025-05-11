<template>
    <div class="p-4">
      <h2 class="text-xl font-semibold mb-2">Return Book</h2>
  
      <form @submit.prevent="returnBookNow" class="space-y-2 max-w-md">
        <input v-model="form.transaction_id" placeholder="Transaction ID" class="input" required />
        <button type="submit" class="btn">Return</button>
      </form>
  
      <p v-if="message" :class="{ 'text-green-600': success, 'text-red-600': !success }" class="mt-2">
        {{ message }}
      </p>
    </div>
  </template>
  
  <script>
  import { returnBook, getBooks } from '../services/api'
  
  export default {
    data() {
      return {
        form: { transaction_id: '' },
        message: '',
        success: false,
        books: []
      }
    },
    methods: {
      async returnBookNow() {
        try {
          await returnBook(this.form.transaction_id)
          this.success = true
          this.message = '✅ Book returned successfully!'
          this.form.transaction_id = ''
  
          // Optional: refresh the book list if needed elsewhere
          const res = await getBooks()
          this.books = res.data
        } catch {
          this.success = false
          this.message = '❌ Return failed. Check the Transaction ID.'
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
    @apply bg-yellow-600 text-white px-4 py-2 rounded;
  }
  </style>
  