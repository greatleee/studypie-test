import Vue from "vue";
import VueRouter from "vue-router";
import auth from "../common/auth";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Home",
    component: () => import("../views/home/Layout.vue"),
    meta: {
      requiresAuth: true,
    },
    children: [
      {
        path: "",
        name: "Home.Board",
        component: () => import("../views/home/Board.vue"),
      },
      {
        path: "posts/:id",
        name: "Home.Post",
        component: () => import("../views/home/Post.vue"),
        props: true,
      },
      {
        path: "points",
        name: "Home.Point",
        component: () => import("../views/home/Point.vue"),
      },
      {
        path: "alarms",
        name: "Home.Alarm",
        component: () => import("../views/home/Alarm.vue"),
      },
    ],
  },
  {
    path: "/login",
    name: "Login",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/Login.vue"),
  },
  {
    path: "/errors/network",
    name: "Network",
    component: () => import("../views/errors/Network.vue"),
  },
];

const router = new VueRouter({
  routes,
});

router.beforeEach(async (to, from, next) => {
  if (auth.getCookie("csrftoken") === null) {
    let isSucceeded = await auth.getCSRFToken();
    if (!isSucceeded) next({ path: "/errors/network" });
  }

  if (to.matched.some((record) => record.meta.requiresAuth)) {
    const isAuthenticated = await auth.loggedIn();
    if (!isAuthenticated) {
      next({ path: "/login" });
    }
  } else if (to.matched.some((record) => record.name === "Login")) {
    const isAuthenticated = await auth.loggedIn();
    if (isAuthenticated) {
      next({ path: "/" });
    }
  }
  next();
});

export default router;
