import { createRouter, createWebHistory } from "vue-router";
import BarberLogin from "../components/BarberLogin.vue";
import HelloWorld from "../components/HelloWorld.vue";
import BarberDashboard from "../components/BarberDashboard.vue";
import BarberCancelAppointment from "../components/BarberCancelAppointment.vue"; // Import the new component

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
  {
    path: "/barber/cancel-appointment/:id",
    name: "BarberCancelAppointment",
    component: BarberCancelAppointment,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
