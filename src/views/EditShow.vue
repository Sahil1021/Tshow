<template>
  <div class="container">
    <h1 class="mb-3">Edit Show</h1>
    <form @submit.prevent="updateShow">
      <div class="form-group">
        <label for="showName">Show Name:</label>
        <input
          v-model="form.name"
          type="text"
          class="form-control"
          id="showName"
          required
        />
      </div>
      <div class="form-group">
        <label for="showTime">Show Time:</label>
        <input
          v-model="form.time"
          type="time"
          class="form-control"
          id="showTime"
          required
        />
      </div>
      <div class="form-group">
        <label for="theatreInput">Theater Name:</label>
        <input
          v-model="form.theatre_name"
          type="text"
          class="form-control"
          id="theatreInput"
          :disabled="true"
        />
      </div>
      <div class="form-group">
        <label for="showDate">Date:</label>
        <input
          v-model="form.date"
          type="date"
          class="form-control"
          id="showDate"
          required
        />
      </div>
      <button type="submit" class="btn btn-primary">Update Show</button>
    </form>
  </div>
</template>

<script>
import api from "../api";

export default {
  data() {
    return {
      form: {
        name: "",
        time: "",
        theatre_name: "",
        date: "",
      },
    };
  },
  async created() {
    // Fetch the show data for editing and set it to the form
    const showId = this.$route.params.id;
    try {
      const response = await api.get(`/shows/${showId}`);
      this.form = response.data;
    } catch (error) {
      console.error("Error fetching show data for editing:", error);
    }
  },
  methods: {
    async updateShow() {
      const showId = this.$route.params.id;
      try {
        const response = await api.put(`/shows/${showId}`, {
          name: this.form.name,
          time: this.form.time,
          date: this.form.date,
        });

        console.log("Update Show Response:", response);

        if (response.status === 200) {
          // Show success alert
          alert("Show updated successfully!");
          // Redirect back to the ShowsList page after updating
          this.$router.push({ name: "ShowList" });
        }
      } catch (error) {
        console.error("Error updating show:", error);
      }
    },
  },
};
</script>
