import { createRouter, createWebHistory } from 'vue-router'
import DefaultLayout from '@/layaouts/DefaultLayout.vue'
import Login         from '@/modules/users/pages/Login.vue'

/* ------------------------------------------------------------
   1.  Manually import each module routes file
------------------------------------------------------------ */
import quoteRoutes     from '@/modules/quotes/routes'
import contactRoutes   from '@/modules/contacts/routes'
import financialRoutes from '@/modules/financials/routes'
import marketingRoutes from '@/modules/marketing/routes'
import settingsRoutes from '@/modules/settings/routes'

/* ------------------------------------------------------------
   2.  Root-level routes
------------------------------------------------------------ */
const routes = [
  {
    path: '/',
    component: DefaultLayout,
    meta: { requiresAuth: true },
    children: [
      { path: '',          name: 'Dashboard',  component: () => import('@/modules/dashboard/pages/Dashboard.vue') },
      ...quoteRoutes,
      ...contactRoutes,
      ...financialRoutes,
      ...marketingRoutes,
      ...settingsRoutes
    ],
  },
  { path: '/login', name: 'Login', component: Login },
  
  /* Public trip routes (outside authentication) - comment out until components exist */
  // { path: '/trip/:id',       name: 'public',  component: () => import('@/modules/marketing/pages/TripPage.vue') },
  // { path: '/p/:token',       name: 'private', component: () => import('@/modules/marketing/components/TripPrivate.vue') },
  // { path: '/register/:id',   name: 'register', component: () => import('@/modules/marketing/components/RegisterForm.vue') },
  
  { path: '/:pathMatch(.*)*', redirect: '/login' },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router




// import { createRouter, createWebHistory } from 'vue-router'
// import Login from '@/views/Login.vue'
// import Dashboard from '@/views/Dashboard.vue'
// import DefaultLayout from '@/layouts/DefaultLayout.vue'
// import QuoteList from '@/views/QuotesList.vue'
// const QuoteView   = () => import('@/views/QuoteView.vue')
// const QuoteEdit   = () => import('@/views/QuoteEdit.vue')
// const QuoteCreate = () => import('@/views/QuoteCreate.vue')
// const ContactList = () => import('@/views/ContactList.vue')

// const routes = [
//   {
//     path: '/',
//     component: DefaultLayout,
//     meta: { requiresAuth: true },
//     children: [
//       {
//         path: '',            //  → /
//         name: 'Dashboard',
//         component: Dashboard
//       },
//       { path: '',              name: 'Dashboard',  component: Dashboard },
//       { path: 'quotes',        name: 'QuoteList',  component: QuoteList },

//       // NEW — one view per quote
//       { path: 'quotes/new',    name: 'QuoteCreate', component: QuoteCreate },
//       { path: 'quotes/:id',    name: 'QuoteView',   component: QuoteView,   props: true },
//       { path: 'quotes/:id/edit', name: 'QuoteEdit', component: QuoteEdit,   props: true }, 
//       // Contacts
//       { path: 'contacts',    name: 'ContactList', component: ContactList },
//       //  → /financials/payments
//       {                     
//         path: 'financials/payments',
//         name: 'Payments',
//         component: () => import('@/views/Payments.vue')
//       },
//       {
//         path: 'financials/expenses',
//         name: 'Expenses',
//         component: () => import('@/views/Expenses.vue')
//       },
//       {
//         path: 'financials/reports',
//         name: 'Reports',
//         component: () => import('@/views/Reports.vue')
//       }
//     ]
//   },
//   {
//     path: '/login',
//     name: 'Login',
//     component: Login
//   },
//   {
//     path: '/:pathMatch(.*)*',
//     redirect: '/login'
//   }
// ]

// const router = createRouter({
//   history: createWebHistory(),
//   routes
// })

// export default router
