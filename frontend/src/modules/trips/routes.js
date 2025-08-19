export default [
  {
    path: 'trips',
    name: 'TripList',
    component: () => import('./pages/TripList.vue'),
    meta: { 
      requiresAuth: true,
      title: 'Trip Management'
    }
  },
  {
    path: 'trips/:id/manage',
    name: 'TripManagement',
    component: () => import('./pages/TripManagement.vue'),
    meta: { 
      requiresAuth: true,
      title: 'Trip Management Details'
    }
  }
]
