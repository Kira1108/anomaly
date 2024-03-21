import Vue from 'vue'
import VueRouter from 'vue-router'
// import HomeView from '../views/HomeView.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'login',
    component: () => import( '../views/login.vue')
  },
  {
    path: '/home',
    name: 'home',
    component: () => import( '../views/HomeView.vue'),
    redirect:'one',
    children: [
      {
        path: '/one',
        component: () => import( '../views/homeMenu/one.vue')
      },
      {
        path: '/two',
        name:'two',
        component: () => import( '../views/homeMenu/two.vue')
      },
      {
        path: '/three',
        name:'three',
        component: () => import( '../views/homeMenu/three.vue')
      },
      {
        path: '/four',
        name:'four',
        component: () => import( '../views/homeMenu/four.vue')
      }
    ]
  },
  // {
  //   path: '/about',
  //   name: 'about',
  //   // route level code-splitting
  //   // this generates a separate chunk (about.[hash].js) for this route
  //   // which is lazy-loaded when the route is visited.
  //   component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  // }
]

const router = new VueRouter({
  mode:'hash',
  routes
})

// 路由守卫;
router.beforeEach((to, from, next) => {
  const isLogin = sessionStorage.getItem("token") ? true : false;
  // // 未登录的情况下重定向到登录页
  if (to.path !== "/" && !isLogin) {
    next("/");
  }

  // // 已经登陆的情况下禁止访问登录页
  if (to.path === "/" && isLogin) {
    next("/home");
  }

  next();
});


export default router