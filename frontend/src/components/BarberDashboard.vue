<template>
  <div class="dashboard-container">
    <header class="dashboard-header">
      <h1>Barber Dashboard</h1>
      <button @click="handleLogout" class="logout-btn">Logout</button>
    </header>

    <div class="dashboard-content">
      <section class="appointments-section">
        <h2>Pending Appointments</h2>

        <div v-if="loading" class="loading-state">Loading appointments...</div>

        <div v-else-if="error" class="error-state">
          {{ error }}
        </div>

        <div v-else>
          <div v-if="appointments.length === 0" class="empty-state">
            No pending appointments
          </div>

          <div v-else class="appointments-list">
            <div
              v-for="appt in appointments"
              :key="appt.id"
              class="appointment-card"
            >
              <div class="appointment-info">
                <h3>{{ appt.customer_name }}</h3>
                <p>{{ formatPhone(appt.phone_number) }}</p>
                <p>{{ formatService(appt.service_name) }}</p>
                <p>{{ formatDateTime(appt.appointment_datetime) }}</p>
              </div>

              <div class="appointment-actions">
                <button
                  @click="confirmAppointment(appt.id)"
                  class="confirm-btn"
                >
                  Confirm
                </button>
                <button @click="cancelAppointment(appt.id)" class="cancel-btn">
                  Cancel
                </button>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "BarberDashboard",
  data() {
    return {
      appointments: [],
      loading: false,
      error: "",
    };
  },
  created() {
    this.fetchAppointments();
  },
  methods: {
    async fetchAppointments() {
      this.loading = true;
      this.error = "";

      try {
        const response = await axios.get(
          "http://localhost:5000/appointments?status=pending",
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("barber_token")}`,
            },
          }
        );

        this.appointments = response.data;
      } catch (err) {
        this.error = err.response?.data?.error || "Failed to load appointments";
        console.error("Fetch error:", err);
      } finally {
        this.loading = false;
      }
    },

    formatPhone(phone) {
      return `(${phone.slice(0, 3)}) ${phone.slice(3, 6)}-${phone.slice(6)}`;
    },

    formatService(service) {
      return `Service: ${service}`;
    },

    formatDateTime(datetime) {
      return new Date(datetime).toLocaleString();
    },

    handleLogout() {
      localStorage.removeItem("barber_token");
      localStorage.removeItem("barber_id");
      this.$router.push("/barber/login");
    },

    async confirmAppointment(appointmentId) {
      try {
        await axios.put(
          `http://localhost:5000/appointments/${appointmentId}`,
          { status: "confirmed" },
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("barber_token")}`,
            },
          }
        );

        this.fetchAppointments(); // Refresh the list
      } catch (err) {
        console.error("Confirm error:", err);
        alert("Failed to confirm appointment");
      }
    },

    cancelAppointment(appointmentId) {
      if (confirm("Are you sure you want to cancel this appointment?")) {
        // TODO: Implement cancellation
        console.log("Would cancel appointment", appointmentId);
      }
    },
  },
};
</script>

<style scoped>
.dashboard-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding-bottom: 15px;
  border-bottom: 1px solid #eee;
}

.logout-btn {
  padding: 8px 16px;
  background-color: #ff4444;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.appointments-section {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.loading-state,
.empty-state {
  text-align: center;
  padding: 20px;
  color: #666;
}

.error-state {
  color: #ff4444;
  text-align: center;
  padding: 20px;
}

.appointments-list {
  display: grid;
  gap: 15px;
}

.appointment-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  border: 1px solid #eee;
  border-radius: 4px;
}

.appointment-info h3 {
  margin: 0 0 5px 0;
}

.appointment-actions {
  display: flex;
  gap: 10px;
}

.confirm-btn {
  padding: 8px 16px;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.cancel-btn {
  padding: 8px 16px;
  background-color: #ffbb33;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
</style>
