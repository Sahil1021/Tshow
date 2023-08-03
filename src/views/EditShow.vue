<template>
  <div class="container">
    <h1 class="mb-3">Edit Show</h1>
    <form @submit.prevent="updateShow">
      <div class="form-group">
        <label for="showName">Show Name:</label>
        <input v-model="form.name" type="text" class="form-control" id="showName" required />
      </div>
      <div class="form-group">
        <label for="showTime">Show Time:</label>
        <input v-model="form.time" type="time" class="form-control" id="showTime" required />
      </div>
      <div class="form-group">
        <label for="theatreInput">Theater Name:</label>
        <input v-model="form.theatre_name" type="text" class="form-control" id="theatreInput" :disabled="true" />
      </div>
      <div class="form-group">
        <label for="showDate">Date:</label>
        <input v-model="form.date" type="date" class="form-control" id="showDate" required />
      </div>


      <div class="form-group">
        <label for="showDescription">Description:</label>
        <textarea v-model="form.description" class="form-control" id="showDescription" rows="4"></textarea>
      </div>
      <div class="form-group">
        <label for="showTicketPrice">Ticket Price:</label>
        <input v-model="form.ticket_price" type="number" step="0.01" class="form-control" id="showTicketPrice" required />
      </div>
      <div class="form-group">
        <label for="showGenre">Genre:</label>
        <input v-model="form.genre" type="text" class="form-control" id="showGenre" required />
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
        description: "",
        ticket_price: 0,
        genre: "",

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
          description: this.form.description,
          ticket_price: this.form.ticket_price,
          genre: this.form.genre,
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
