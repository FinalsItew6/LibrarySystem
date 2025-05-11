import { createRouter, createWebHistory } from 'vue-router';
import BookList from '../components/BookList.vue';
import BorrowForm from '../components/BorrowForm.vue';
import ReturnForm from '../components/ReturnForm.vue';
import TransactionList from '../components/TransactionList.vue';

const routes = [
  { path: '/', component: BookList },
  { path: '/borrow', component: BorrowForm },
  { path: '/return', component: ReturnForm },
  { path: '/transactions', component: TransactionList },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
