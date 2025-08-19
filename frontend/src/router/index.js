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
import tripRoutes from '@/modules/trips/routes'

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
      { path: 'marketing', name: 'MarketingViews', component: () => import('@/modules/marketing/pages/MarketingViews.vue') },
      ...quoteRoutes,
      ...contactRoutes,
      ...financialRoutes,
      ...settingsRoutes,
      ...tripRoutes
      // Do NOT include ...marketingRoutes here for public pages
    ],
  },
  // Public trip routes (no auth required)
  {
    path: '/marketing/trips/:slug',
    name: 'TripPublic',
    component: () => import('@/modules/marketing/pages/TripPublic.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/marketing/trips/private/:slug',
    name: 'TripPrivate',
    component: () => import('@/modules/marketing/pages/TripPrivate.vue'),
    meta: { requiresAuth: false }
  },
  // Trip registration route (requires customer authentication)
  {
    path: '/trips/register/:id',
    name: 'TripRegistration',
    component: () => import('@/modules/trips/TripRegistrationForm.vue'),
    meta: { requiresAuth: false } // Will handle auth internally
  },
  { path: '/login', name: 'Login', component: Login },
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
