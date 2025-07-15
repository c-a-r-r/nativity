export default [
  {
    path: 'financials/payments',
    name: 'Payments',
    component: () => import('./pages/Payments.vue'),
  },
  {
    path: 'financials/expenses',
    name: 'Expenses',
    component: () => import('./pages/Expenses.vue'),
  },
  {
    path: 'financials/reports',
    name: 'Reports',
    component: () => import('./pages/Reports.vue'),
  },
]