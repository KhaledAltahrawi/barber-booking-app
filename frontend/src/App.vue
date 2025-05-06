<template>
  <div id="app">
    <img alt="Vue logo" src="./assets/logo.png">
    <HelloWorld/>
    <ServiceList/>
  </div>
</template>

<script>
import HelloWorld from './components/HelloWorld.vue';
import ServiceList from './components/ServiceList.vue'; // Import ServiceList

export default {
  name: 'App',
  components: {
    HelloWorld,
    ServiceList // Registering ServiceList to use it in the template.
  }
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