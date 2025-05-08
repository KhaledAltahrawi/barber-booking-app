import { createRouter, createWebHistory } from "vue-router";
import BarberLogin from "../components/BarberLogin.vue";
import HelloWorld from "../components/HelloWorld.vue";
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
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
