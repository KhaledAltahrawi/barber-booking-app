<template>
    <div>
      <h2>Book an Appointment</h2>
      <form @submit.prevent="submitForm">
        <div>
          <label for="customer_name">Name:</label>
          <input type="text" id="customer_name" v-model="formData.customer_name" required>
        </div>
        <div>
          <label for="phone_number">Phone Number:</label>
          <input type="tel" id="phone_number" v-model="formData.phone_number" required>
        </div>
        <div>
          <label for="service_id">Service:</label>
          <select id="service_id" v-model="formData.service_id" required>
            <option v-for="service in services" :key="service.id" :value="service.id">
              {{ service.name }} ({{ service.duration_minutes }} minutes)
            </option>
          </select>
        </div>
        <div>
          <label for="appointment_datetime">Date and Time:</label>
          <input type="datetime-local" id="appointment_datetime" v-model="formData.appointment_datetime" required>
        </div>
        <button type="submit">Book Appointment</button>
        <div v-if="message" :class="{ success: isSuccess, error: !isSuccess }">{{ message }}</div>
      </form>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'BookingForm',
    data() {
      return {
        services: [],
        formData: {
          customer_name: '',
          phone_number: '',
          service_id: '',
          appointment_datetime: ''
        },
        message: null,
        isSuccess: false
      };
    },
    mounted() {
      this.fetchServices();
    },
    methods: {
      async fetchServices() {
        try {
          const response = await axios.get('http://localhost:5000/services');
          this.services = response.data;
        } catch (error) {
          console.error('Error loading services:', error);
          this.message = 'Failed to load services.';
        }
      },
      async submitForm() {
        try {
          const response = await axios.post('http://localhost:5000/appointments', this.formData);
          this.message = response.data.message;
          this.isSuccess = true;
          // Reset form data after successful booking
          this.formData = {
            customer_name: '',
            phone_number: '',
            service_id: '',
            appointment_datetime: ''
          };
        } catch (error) {
          console.error('Error booking appointment:', error.response ? error.response.data : error.message);
          this.message = error.response ? error.response.data.error : 'Failed to book appointment.';
          this.isSuccess = false;
        }
      }
    }
  };
  </script>
  
  <style scoped>
  /* يمكنك إضافة أنماط CSS هنا لتجميل النموذج */
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
  </style>