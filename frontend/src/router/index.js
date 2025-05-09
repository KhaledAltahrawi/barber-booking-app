import { createRouter, createWebHistory } from "vue-router";
import BarberLogin from "../components/BarberLogin.vue";
import BarberDashboard from "../components/BarberDashboard.vue";
import BookingForm from "../components/BookingForm.vue";

const routes = [
  {
    path: "/",
    redirect: "/book",
  },
  {
    path: "/book",
    name: "Booking",
    component: BookingForm,
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
    meta: { requiresAuth: true },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Auth guard
router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem("barber_token");

  if (to.meta.requiresAuth && !isAuthenticated) {
    next("/barber/login");
  } else {
    next();
  }
});

export default router;
