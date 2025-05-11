<template>
  <div>
    <!-- Global Navbar -->
    <nav class="bg-red-900 text-white px-6 py-4 flex shadow-md">
  <div class="ml-auto flex gap-6">
    <router-link
      v-for="link in links"
      :key="link.to"
      :to="link.to"
      class="text-white hover:underline"
      :class="$route.path === link.to ? 'font-bold underline' : ''"
    >
      {{ link.label }}
    </router-link>
  </div>
</nav>


    <!-- Page Content -->
    <router-view />
  </div>
</template>

<script>
export default {
  data() {
    return {
      links: [
        { to: '/', label: 'Books' },
        { to: '/borrow', label: 'Borrow' },
        { to: '/return', label: 'Return' },
        { to: '/transactions', label: 'Transactions' }
      ]
    }
  }
}
</script>
