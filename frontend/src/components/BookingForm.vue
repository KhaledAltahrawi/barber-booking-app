<template>
  <div>
    <h2>Book an Appointment</h2>
    <form @submit.prevent="submitForm">
      <div>
        <label for="customer_name">Name:</label>
        <input
          type="text"
          id="customer_name"
          v-model="formData.customer_name"
          @input="errors.customer_name = ''"
          required
        />
        <div v-if="errors.customer_name" class="error-message">
          {{ errors.customer_name }}
        </div>
      </div>
      <div>
        <label for="phone_number">Phone Number:</label>
        <input
          type="tel"
          id="phone_number"
          v-model="formData.phone_number"
          @input="errors.phone_number = ''"
          required
        />
        <div v-if="errors.phone_number" class="error-message">
          {{ errors.phone_number }}
        </div>
      </div>
      <div>
        <label for="service_id">Service:</label>
        <select id="service_id" v-model="formData.service_id" required>
          <option value="" disabled selected>Select a service</option>
          <option
            v-for="service in services"
            :key="service.id"
            :value="service.id"
          >
            {{ service.name }} ({{ service.duration_minutes }} minutes)
          </option>
        </select>
      </div>
      <div>
        <label for="appointment_datetime">Date and Time:</label>
        <input
          type="datetime-local"
          id="appointment_datetime"
          v-model="formData.appointment_datetime"
          @input="errors.appointment_datetime = ''"
          required
        />
        <div class="instructions">
          Please select the date and time. A calendar pop-up may appear on your
          mobile device.
        </div>
        <div v-if="errors.appointment_datetime" class="error-message">
          {{ errors.appointment_datetime }}
        </div>
      </div>
      <button
        type="submit"
        :disabled="Object.keys(errors).some((key) => errors[key])"
      >
        Book Appointment
      </button>
      <div v-if="message" :class="{ success: isSuccess, error: !isSuccess }">
        {{ message }}
      </div>
    </form>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "BookingForm",
  props: {
    services: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      formData: {
        customer_name: "",
        phone_number: "",
        service_id: "",
        appointment_datetime: "",
      },
      errors: {
        customer_name: "",
        phone_number: "",
        appointment_datetime: "",
      },
      message: null,
      isSuccess: false,
    };
  },
  methods: {
    async submitForm() {
      this.message = null;
      this.isSuccess = false;
      this.errors = {
        customer_name: "",
        phone_number: "",
        appointment_datetime: "",
      };

      let isValid = true;

      if (!this.formData.customer_name.trim()) {
        this.errors.customer_name = "Name is required.";
        isValid = false;
      } else if (!/^[a-zA-Z\s]+$/.test(this.formData.customer_name)) {
        this.errors.customer_name =
          "Name must contain only letters, spaces allowed for full name.";
        isValid = false;
      }

      if (!this.formData.phone_number.trim()) {
        this.errors.phone_number = "Phone number is required.";
        isValid = false;
      } else if (!/^\d{10}$/.test(this.formData.phone_number)) {
        this.errors.phone_number = "Phone number must be 10 digits.";
        isValid = false;
      }

      if (!this.formData.appointment_datetime) {
        this.errors.appointment_datetime = "Date and time are required.";
        isValid = false;
      } else {
        const selectedDateTime = new Date(this.formData.appointment_datetime);
        const now = new Date();
        if (selectedDateTime <= now) {
          this.errors.appointment_datetime =
            "Appointment time cannot be in the past.";
          isValid = false;
        }
      }

      if (isValid) {
        try {
          const response = await axios.post(
            "http://localhost:5000/appointments",
            this.formData
          );

          if (response.status === 201) {
            this.message = response.data.message;
            this.isSuccess = true;
            this.formData = {
              customer_name: "",
              phone_number: "",
              service_id: "",
              appointment_datetime: "",
            }; // Reset the form
          } else {
            this.message = "Failed to book appointment.";
            this.isSuccess = false;
          }
        } catch (error) {
          console.error(
            "Error booking appointment:",
            error.response ? error.response.data : error.message
          );
          this.message = error.response
            ? error.response.data.error
            : "Failed to book appointment.";
          this.isSuccess = false;
        }
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
  margin-top: 20px;
}

div {
  margin-bottom: 10px;
}

label {
  display: block;
  margin-bottom: 5px;
}

input[type="text"],
input[type="tel"],
input[type="datetime-local"],
select {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
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

.success {
  color: green;
  margin-top: 10px;
}

.error {
  color: red;
  margin-top: 10px;
}

.error-message {
  color: red;
  font-size: 0.8em;
  margin-top: 5px;
}

.instructions {
  font-size: 0.8em;
  color: #777;
  margin-top: 5px;
}
</style>
