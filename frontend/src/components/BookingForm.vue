<template>
  <div class="booking-form">
    <h2>Book Appointment</h2>
    <form @submit.prevent="handleSubmit">
      <!-- Customer Info -->
      <div class="form-group">
        <label>Full Name:</label>
        <input v-model="form.name" required />
      </div>

      <div class="form-group">
        <label>Phone Number:</label>
        <input
          v-model="form.phone"
          pattern="[0-9]{10}"
          placeholder="1234567890"
          required
        />
      </div>

      <!-- Service Selection -->
      <div class="form-group">
        <label>Service:</label>
        <select v-model="form.serviceId" required>
          <option disabled value="">Select a service</option>
          <option
            v-for="service in services"
            :key="service.id"
            :value="service.id"
          >
            {{ service.name }} ({{ service.duration_minutes }} mins)
          </option>
        </select>
      </div>

      <!-- Date/Time (Temporary - TODO: Replace with slot picker) -->
      <div class="form-group">
        <label>Appointment Time:</label>
        <input
          type="datetime-local"
          v-model="form.datetime"
          :min="minDateTime()"
          required
        />
      </div>

      <button type="submit" :disabled="loading">
        {{ loading ? "Booking..." : "Confirm Booking" }}
      </button>

      <!-- Status Message -->
      <div v-if="message" :class="['alert', messageType]">
        {{ message }}
      </div>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      services: [],
      form: {
        name: "",
        phone: "",
        serviceId: "",
        datetime: "",
      },
      loading: false,
      message: "",
      messageType: "",
    };
  },
  async created() {
    // Load services
    try {
      const response = await fetch("http://localhost:5000/services");
      this.services = await response.json();
    } catch (error) {
      this.showMessage("Failed to load services", "error");
    }
  },
  methods: {
    minDateTime() {
      // Set minimum datetime to current time
      const now = new Date();
      now.setMinutes(now.getMinutes() + 30); // Buffer time
      return now.toISOString().slice(0, 16);
    },
    async handleSubmit() {
      this.loading = true;
      this.message = "";

      try {
        // Format datetime for backend
        const formattedDateTime = this.form.datetime.replace("T", " ") + ":00";

        const response = await fetch("http://localhost:5000/appointments", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            customer_name: this.form.name,
            phone_number: this.form.phone,
            service_id: this.form.serviceId,
            appointment_datetime: formattedDateTime,
          }),
        });

        const data = await response.json();
        if (!response.ok) throw new Error(data.error || "Booking failed");

        this.showMessage("Booking successful!", "success");
        this.resetForm();
      } catch (error) {
        this.showMessage(error.message, "error");
      } finally {
        this.loading = false;
      }
    },
    resetForm() {
      this.form = {
        name: "",
        phone: "",
        serviceId: "",
        datetime: "",
      };
    },
    showMessage(text, type) {
      this.message = text;
      this.messageType = type;
    },
  },
};
</script>

<style scoped>
.booking-form {
  max-width: 500px;
  margin: 0 auto;
  padding: 20px;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
}

input,
select {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

button {
  background: #42b983;
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:disabled {
  background: #ccc;
}

.alert {
  margin-top: 15px;
  padding: 10px;
  border-radius: 4px;
}

.error {
  background: #ffebee;
  color: #f44336;
}

.success {
  background: #e8f5e9;
  color: #4caf50;
}
</style>
