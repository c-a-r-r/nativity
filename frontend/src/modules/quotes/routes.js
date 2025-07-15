export default [
  { path:'quotes',           name:'QuoteList',  component:() => import('./pages/QuoteList.vue') },
  { path:'quotes/new',       name:'QuoteCreate',component:() => import('./pages/QuoteCreate.vue') },
  //{ path:'quotes/:id',       name:'QuoteView',  component:() => import('./pages/QuoteView.vue'),  props:true },
  { path:'quotes/:id/edit',  name:'QuoteEdit',  component:() => import('./pages/QuoteEdit.vue'), props:true },
]