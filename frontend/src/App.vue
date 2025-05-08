<template>
  <div id="app">
    <img alt="Vue logo" src="./assets/logo.png" />
    <router-view></router-view>
  </div>
</template>

<script>
import { useRouter } from "vue-router";

export default {
  name: "App",
  components: {
    // HelloWorld,
    // ServiceList,
    // BookingForm,
    // BarberLogin is not imported here; it will be rendered by router-view
  },
  setup() {
    const router = useRouter();

    return {
      router,
    };
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
