<template>
  <div>
    <h2>Cancel Appointment</h2>
    <p>Appointment ID: {{ appointmentId }}</p>
    <label for="cancellation-reason">Cancellation Reason:</label>
    <textarea
      id="cancellation-reason"
      v-model="cancellationReason"
      rows="4"
      cols="50"
      required
    ></textarea>
    <br />
    <button @click="submitCancellation">Submit Cancellation</button>
    <button @click="$router.go(-1)">Go Back</button>
    <div v-if="error" style="color: red">{{ error }}</div>
  </div>
</template>

<script>
import { ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import axios from "axios";

export default {
  name: "BarberCancelAppointment",
  setup() {
    const route = useRoute();
    const router = useRouter();
    const appointmentId = route.params.id;
    const cancellationReason = ref("");
    const error = ref(null);

    const submitCancellation = async () => {
      if (!cancellationReason.value.trim()) {
        error.value = "Please enter a cancellation reason.";
        return;
      }
      try {
        const response = await axios.put(
          `http://localhost:5000/appointments/${appointmentId}`,
          {
            status: "cancelled",
            cancellation_reason: cancellationReason.value,
          }
        );
        console.log(response.data.message);
        router.push("/barber/dashboard"); // Redirect to dashboard after successful cancellation
      } catch (err) {
        error.value = err.message;
        console.error("Error cancelling appointment:", err);
      }
    };

    return {
      appointmentId,
      cancellationReason,
      submitCancellation,
      error,
      router,
    };
  },
};
</script>

<style scoped>
/* Basic styling for the cancellation form */
label {
  display: block;
  margin-bottom: 5px;
}

textarea {
  margin-bottom: 10px;
}

button {
  margin-right: 10px;
  padding: 8px 12px;
  cursor: pointer;
}
</style>
