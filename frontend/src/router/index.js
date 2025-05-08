import { createRouter, createWebHistory } from "vue-router";
import BarberLogin from "../components/BarberLogin.vue";
import HelloWorld from "../components/HelloWorld.vue";
import BarberDashboard from "../components/BarberDashboard.vue";

const routes = [
  {
    path: "/",
    name: "Home",
    component: HelloWorld,
  },
  {
    path: "/barber/login",
    name: "BarberLogin",
    component: BarberLogin,
  },
  {
    path: "/barber/dashboard",
    name: "BarberDashboard",
    component: BarberDashboard,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
