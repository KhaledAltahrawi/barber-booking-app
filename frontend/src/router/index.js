import { createRouter, createWebHistory } from "vue-router";
import BookingForm from "../components/BookingForm.vue";
import BarberLogin from "../components/BarberLogin.vue";

const routes = [
  {
    path: "/",
    redirect: "/book", // Redirect root to booking
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
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
