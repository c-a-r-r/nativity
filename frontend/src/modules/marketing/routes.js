import TripPublic from './pages/TripPublic.vue'
import TripPrivate from './pages/TripPrivate.vue'
import TripList from './pages/TripList.vue'

export default [
  {
    path: '/trips',
    name: 'TripList',
    component: TripList,
    meta: {
      requiresAuth: false
    }
  },
  {
    path: '/trips/:slug',
    name: 'TripPublic',
    component: TripPublic,
    meta: {
      requiresAuth: false
    }
  },
  {
    path: '/trips/private/:token',
    name: 'TripPrivate', 
    component: TripPrivate,
    meta: {
      requiresAuth: false
    }
  }
]