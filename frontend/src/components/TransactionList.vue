<template>
  <div class="p-6">
    <h2 class="text-2xl font-semibold mb-6 text-gray-800">📄 Transaction History</h2>

    <div class="overflow-x-auto rounded shadow border border-gray-200 bg-white">
      <table class="min-w-full table-auto">
        <thead class="bg-blue-700 text-white text-sm uppercase">
          <tr>
            <th class="px-6 py-3 text-left border-b">Transaction ID</th>
            <th class="px-6 py-3 text-left border-b">User</th>
            <th class="px-6 py-3 text-left border-b">Book</th>
            <th class="px-6 py-3 text-left border-b">Status</th>
            <th class="px-6 py-3 text-left border-b">Borrowed At</th>
            <th class="px-6 py-3 text-left border-b">Returned At</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="!transactions.length">
            <td colspan="6" class="text-center py-6 text-gray-500">
              No transactions recorded.
            </td>
          </tr>
          <tr
            v-for="(tx, index) in transactions"
            :key="tx.id"
            :class="index % 2 === 0 ? 'bg-white' : 'bg-gray-50'"
            class="hover:bg-gray-100 transition-colors"
          >
            <td class="px-6 py-4 border-b">{{ tx.id }}</td>
            <td class="px-6 py-4 border-b">{{ tx.user_name }}</td>
            <td class="px-6 py-4 border-b">{{ tx.book_title }}</td>
            <td class="px-6 py-4 border-b">
              <span
                :class="tx.status === 'returned' ? 'text-green-600 font-medium' : 'text-yellow-600 font-medium'"
              >
                {{ tx.status }}
              </span>
            </td>
            <td class="px-6 py-4 border-b">{{ formatDate(tx.borrow_date) }}</td>
            <td class="px-6 py-4 border-b">{{ tx.return_date ? formatDate(tx.return_date) : '—' }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import { getTransactions } from '../services/api'

export default {
  data() {
    return {
      transactions: []
    }
  },
  async created() {
    const res = await getTransactions()
    this.transactions = res.data
  },
  methods: {
    formatDate(date) {
      if (!date) return '—'
      const parsed = new Date(date)
      return !isNaN(parsed) ? parsed.toLocaleString() : '—'
    }
  }
}
</script>

<style scoped>
table {
  @apply text-sm;
}
</style>
