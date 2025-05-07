<template>
  <div id="app">
    <img alt="Vue logo" src="./assets/logo.png" />
    <HelloWorld />
    <ServiceList :services="services" :loading="loading" :error="error" />
    <BookingForm :services="services" />
  </div>
</template>

<script>
import HelloWorld from "./components/HelloWorld.vue";
import ServiceList from "./components/ServiceList.vue";
import BookingForm from "./components/BookingForm.vue";
import axios from "axios";

export default {
  name: "App",
  components: {
    HelloWorld,
    ServiceList,
    BookingForm,
  },
  data() {
    return {
      services: [],
      loading: false,
      error: null,
    };
  },
  mounted() {
    this.fetchServices();
  },
  methods: {
    async fetchServices() {
      this.loading = true;
      this.error = null;
      try {
        const response = await axios.get("http://localhost:5000/services");
        this.services = response.data;
      } catch (err) {
        this.error = err.message;
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
