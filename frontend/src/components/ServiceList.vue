<template>
  <div>
    <h2>Available Services</h2>
    <ul>
      <li v-for="service in services" :key="service.id">
        {{ service.name }} ({{ service.duration_minutes }} minutes)
      </li>
    </ul>
    <p v-if="loading">Loading services...</p>
    <p v-if="error">Error loading services: {{ error }}</p>
  </div>
</template>

<script>
export default {
  name: "ServiceList",
  props: {
    services: {
      type: Array,
      required: true,
    },
    loading: {
      type: Boolean,
      default: false,
    },
    error: {
      type: String,
      default: null,
    },
  },
};
</script>

<style scoped>
h2 {
  margin-bottom: 10px;
}

ul {
  list-style: none;
  padding: 0;
}

li {
  padding: 5px 0;
  border-bottom: 1px solid #eee;
}

li:last-child {
  border-bottom: none;
}

.loading {
  font-style: italic;
  color: #777;
}

.error {
  color: red;
  font-weight: bold;
}
</style>
