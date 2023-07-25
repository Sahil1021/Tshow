<template>
  <div>
    <h1>Create a New Show</h1>
    <form class="container w-25" @submit.prevent="createShow">
      <label>Theatre ID:</label>
      <input class="form-control" v-model="theatreId" type="number" required />
      <br />
      <label>Show Name:</label>
      <input class="form-control" v-model="showName" type="text" required />
      <br />
      <label>Show Date:</label>
      <input class="form-control" v-model="showDate" type="date" required />
      <br />
      <label>Show Time:</label>
      <input class="form-control" v-model="showTime" type="time" required />
      <br />
      <button class="btn btn-primary" type="submit">Create Show</button>
    </form>
    <p v-if="errorMessage">{{ errorMessage }}</p>
  </div>
</template>

<script>
import api from "../api";
export default {
  data() {
    return {
      theatreId: "",
      showName: "",
      showDate: "",
      showTime: "",
      errorMessage: "",
    };
  },
  methods: {
    async createShow() {
      try {
        const showData = {
          theatre_id: this.theatreId,
          name: this.showName,
          date: this.showDate,
          time: this.showTime,
        };
        const response = await api.post("/shows", showData);

        if (response.status === 201) {
          alert("Show created successfully!");
          // Clear form inputs after creating a show
          this.theatreId = "";
          this.showName = "";
          this.showDate = "";
          this.showTime = "";
          this.errorMessage = ""; // Clear any previous error message
        }
      } catch (error) {
        if (error.response && error.response.status === 404) {
          this.errorMessage =
            "Theater not found. Please provide a valid Theater ID.";
        } else {
          this.errorMessage = "An error occurred while creating the show.";
        }
        console.error(error);
      }
    },
  },
};
</script>
