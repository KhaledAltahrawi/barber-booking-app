<template>
  <div>
    <h2>Barber Login</h2>
    <form @submit.prevent="login">
      <div>
        <label for="username">Username:</label>
        <input type="text" id="username" v-model="username" required />
      </div>
      <div>
        <label for="password">Password:</label>
        <input type="password" id="password" v-model="password" required />
      </div>
      <button type="submit" :disabled="loading">
        {{ loading ? "Logging in..." : "Login" }}
      </button>
      <div v-if="error" class="error-message">{{ error }}</div>
    </form>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "BarberLogin",
  data() {
    return {
      username: "",
      password: "",
      loading: false,
      error: null,
    };
  },
  methods: {
    async login() {
      this.loading = true;
      this.error = null;
      try {
        const response = await axios.post("http://localhost:5000/login", {
          username: this.username,
          password: this.password,
        });
        // Future: Store login information (e.g., token) and redirect the barber to their dashboard
        console.log("Login successful:", response.data);
        this.$router.push("/barber/dashboard"); // Temporary redirection
      } catch (error) {
        console.error(
          "Login failed:",
          error.response ? error.response.data : error.message
        );
        this.error = error.response
          ? error.response.data.error
          : "Login failed.";
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
form {
  display: flex;
  flex-direction: column;
  max-width: 300px;
  margin: 20px auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

div {
  margin-bottom: 10px;
}

label {
  display: block;
  margin-bottom: 5px;
}

input[type="text"],
input[type="password"] {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-sizing: border-box;
}

button[type="submit"] {
  padding: 10px 15px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button[type="submit"]:hover {
  background-color: #0056b3;
}

button[type="submit"]:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.error-message {
  color: red;
  margin-top: 10px;
}
</style>
