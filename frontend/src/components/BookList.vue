<template>
  <div>
    <!-- Main Content -->
    <div class="p-6">
      <h2 class="text-2xl font-semibold flex items-center gap-2 mb-4">
        📚 <span>Book List</span>
      </h2>

      <button
        @click="showForm = true; autoGenerateISBN()"
        class="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 mb-6 flex items-center gap-2"
      >
        <span class="text-lg">＋</span> Add Book
      </button>

      <!-- Grid of Book Cards -->
<div v-if="books.length" class="grid gap-4 md:grid-cols-2 lg:grid-cols-5">
  <div
    v-for="book in books"
    :key="book.id"
    class="bg-red-100 text-gray-800 rounded shadow p-4 flex flex-col justify-between hover:bg-red-200 hover:shadow-lg transition"
  >
    <div class="mb-3 space-y-1">
      <h3 class="text-lg font-semibold text-white-900 flex items-center gap-2">
        📘 <span>{{ book.title }}</span>
      </h3>
      <p class="text-sm text-gray-700">👤 {{ book.author }}</p>
      <p class="text-sm text-gray-600"> ISBN: {{ book.isbn }}</p>
      <p>
        <span class="inline-block text-xs font-bold bg-white text-red-700 px-3 py-1 rounded shadow">
          {{ book.copies_available }} copies available
        </span>
      </p>
    </div>
    <div class="flex gap-2">
      <button
        @click="editBook(book)"
        class="px-3 py-1 border border-blue-600 text-blue-600 rounded hover:bg-blue-600 hover:text-white transition"
      >
        ✏️ Edit
      </button>
      <button
        @click="deleteBook(book.id)"
        class="px-3 py-1 border border-red-700 text-red-700 rounded hover:bg-red-700 hover:text-white transition"
      >
        ❌ Delete
      </button>
    </div>
  </div>
</div>


      <p v-else class="text-gray-500 mt-4">No books available.</p>
    </div>

    <!-- Add/Edit Modal -->
    <div
      v-if="showForm"
      class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50"
    >
      <div class="bg-white p-6 rounded shadow-md w-full max-w-lg">
        <h3 class="text-lg font-semibold mb-4">
          {{ isEditing ? 'Edit Book' : 'Add Book' }}
        </h3>
        <form
          @submit.prevent="isEditing ? updateBook() : addBook()"
          class="grid grid-cols-2 gap-4"
        >
          <input v-model="form.title" placeholder="Title" class="input" required />
          <input v-model="form.author" placeholder="Author" class="input" required />
          <input v-model="form.isbn" placeholder="ISBN" class="input" readonly />
          <input
            v-model.number="form.copies_available"
            type="number"
            placeholder="Copies"
            class="input"
            required
          />
          <div class="col-span-2 flex justify-end gap-2">
            <button
              type="button"
              @click="cancelEdit"
              class="bg-red-500 hover:bg-red-700 text-white px-4 py-2 rounded"
            >
              Cancel
            </button>
            <button
              type="submit"
              class="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded"
            >
              {{ isEditing ? 'Update' : 'Add' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { getBooks, addBook, updateBook, deleteBook } from '../services/api'

export default {
  data() {
    return {
      books: [],
      form: { title: '', author: '', isbn: '', copies_available: 0 },
      isEditing: false,
      editId: null,
      showForm: false
    }
  },
  created() {
    this.fetchBooks()
  },
  methods: {
    async fetchBooks() {
      const res = await getBooks()
      this.books = res.data
    },
    autoGenerateISBN() {
      const random = Math.floor(1000000000000 + Math.random() * 9000000000000)
      this.form.isbn = random.toString()
    },
    async addBook() {
  try {
    await addBook(this.form)
    this.fetchBooks()
    alert('✅ Book added successfully.')
    this.resetForm()
  } catch (err) {
    console.error(err)
    alert('❌ Failed to add book.')
  }
},

    editBook(book) {
      this.form = { ...book }
      this.editId = book.id
      this.isEditing = true
      this.showForm = true
    },
    async updateBook() {
      await updateBook(this.editId, this.form)
      this.fetchBooks()
      this.resetForm()
    },
    cancelEdit() {
      this.resetForm()
    },
    resetForm() {
      this.isEditing = false
      this.editId = null
      this.form = { title: '', author: '', isbn: '', copies_available: 0 }
      this.showForm = false
    },
    async deleteBook(id) {
  const confirmDelete = confirm('Are you sure you want to delete this book?')
  if (!confirmDelete) return

  try {
    await deleteBook(id)
    this.fetchBooks()
    alert('✅ Book deleted successfully.')
  } catch (err) {
    const msg = err?.response?.data?.error || 'Failed to delete book.'
    alert('❌ ' + msg)
  }
}

  }
}
</script>

<style scoped>
.input {
  @apply border border-gray-300 px-3 py-2 rounded w-full;
}
</style>
