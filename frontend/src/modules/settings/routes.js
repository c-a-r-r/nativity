import SettingsMenuTiles from './pages/SettingsMenuTiles.vue'
import TripTemplateManager from './pages/TripTemplateManager.vue'
import WebsiteTemplateCreator from './pages/WebsiteTemplateCreator.vue'
import WebsiteTemplateEdit from './pages/WebsiteTemplateEdit.vue'

export default [
  {
    path: '/settings',
    name: 'Settings',
    component: SettingsMenuTiles,
    meta: {
      title: 'Settings',
      requiresAuth: true
    }
  },
  {
    path: '/settings/trip-templates',
    name: 'TripTemplates',
    component: TripTemplateManager,
    meta: {
      title: 'Trip Templates',
      requiresAuth: true
    }
  },
  {
    path: '/settings/trip-templates/create',
    name: 'CreateTemplate',
    component: WebsiteTemplateCreator,
    meta: {
      title: 'Create Template',
      requiresAuth: true
    }
  },
  {
    path: '/settings/trip-templates/edit/:id',
    name: 'EditTemplate',
    component: WebsiteTemplateEdit,
    meta: {
      title: 'Edit Template',
      requiresAuth: true
    }
  }
  // Add more settings routes as needed:
  // {
  //   path: '/settings/users',
  //   name: 'UserManagement',
  //   component: () => import('./pages/UserManagement.vue'),
  //   meta: { title: 'User Management', requiresAuth: true }
  // }
]