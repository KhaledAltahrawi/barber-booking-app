<template>
  <div id="app">
    <img alt="Vue logo" src="./assets/logo.png">
    <HelloWorld/>
    <ServiceList/>
    <BookingForm/> </div>
</template>

<script>
import HelloWorld from './components/HelloWorld.vue';
import ServiceList from './components/ServiceList.vue';
import BookingForm from './components/BookingForm.vue'; 

export default {
  name: 'App',
  components: {
    HelloWorld,
    ServiceList,
    BookingForm 
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