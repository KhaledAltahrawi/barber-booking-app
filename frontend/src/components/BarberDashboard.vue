<template>
  <div>
    <h2>Barber Dashboard</h2>
    <h3>Upcoming Appointments</h3>
    <div v-if="loading">Loading appointments...</div>
    <div v-else-if="error">Error loading appointments: {{ error }}</div>
    <ul v-else-if="appointments.length > 0">
      <li v-for="appointment in appointments" :key="appointment.id">
        <strong>Customer:</strong> {{ appointment.customer_name }} ({{
          appointment.phone_number
        }}), <strong>Service:</strong> {{ appointment.service_name }},
        <strong>Time:</strong>
        {{ new Date(appointment.appointment_datetime).toLocaleString() }}
        <button @click="confirmAppointment(appointment.id)">Confirm</button>
        <button @click="cancelAppointment(appointment.id)">Cancel</button>
      </li>
    </ul>
    <div v-else>No upcoming appointments.</div>
    <button @click="$router.push('/barber/add-availability')">
      Add Availability
    </button>
  </div>
</template>

<script>
import axios from "axios";
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";

export default {
  name: "BarberDashboard",
  setup() {
    const appointments = ref([]);
    const loading = ref(false);
    const error = ref(null);
    const router = useRouter();

    const fetchAppointments = async () => {
      loading.value = true;
      error.value = null;
      try {
        const response = await axios.get(
          "http://localhost:5000/appointments?status=pending"
        );
        appointments.value = response.data;
      } catch (err) {
        error.value = err.message;
      } finally {
        loading.value = false;
      }
    };

    const confirmAppointment = async (id) => {
      try {
        const response = await axios.put(
          `http://localhost:5000/appointments/${id}`,
          {
            status: "confirmed",
          }
        );
        console.log(response.data.message); // Log the response message
        // Remove the appointment from the list after successful confirmation
        appointments.value = appointments.value.filter(
          (appointment) => appointment.id !== id
        );
      } catch (err) {
        error.value = err.message;
        console.error("Error confirming appointment:", err);
      }
    };

    const cancelAppointment = (id) => {
      router.push(`/barber/cancel-appointment/${id}`);
    };

    onMounted(fetchAppointments);

    return {
      appointments,
      loading,
      error,
      fetchAppointments,
      confirmAppointment,
      cancelAppointment,
      router,
    };
  },
};
</script>

<style scoped>
/* Basic styling for the dashboard */
ul {
  list-style-type: none;
  padding: 0;
}

li {
  border: 1px solid #eee;
  margin-bottom: 10px;
  padding: 10px;
  border-radius: 5px;
}

button {
  margin-left: 10px;
  padding: 8px 12px;
  cursor: pointer;
}
</style>
