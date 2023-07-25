<template>
  <div class="container">
    <h1 class="mb-3">Shows List</h1>
    <div class="form-group">
      <label for="dateInput">Select Date:</label>
      <input
        type="date"
        class="form-control"
        id="dateInput"
        v-model="selectedDate"
        @change="filterShows"
      />
    </div>
    <div class="form-group">
      <label for="theaterInput">Enter Theater Name:</label>
      <input
        type="text"
        class="form-control"
        id="theaterInput"
        v-model="theaterInput"
        @input="filterShows"
      />
    </div>
    <div class="row mt-3" v-if="filteredShows.length > 0">
      <div
        class="col-12 col-sm-6 col-md-6 mb-4"
        v-for="show in filteredShows"
        :key="show.id"
      >
        <div class="card">
          <div class="card-body">
            <h5 class="card-title text-decoration-underline">
              Show {{ show.id }}
            </h5>
            <p class="card-text">Show Name: {{ show.name }}</p>
            <p class="card-text">Theater Name: {{ show.theatre_name }}</p>
            <p class="card-text">Show Time: {{ show.time }}</p>
          </div>
        </div>
      </div>
    </div>
    <p v-else>No shows found for the selected date and theater.</p>
    <router-link to="/shows/create" class="btn btn-primary mb-4"
      >Create New Show</router-link
    >
  </div>
</template>

<script>
import api from "../api";

export default {
  data() {
    return {
      shows: [],
      selectedDate: "", // Variable to hold the selected date
      theaterInput: "", // Variable to hold the input theater name
    };
  },
  async created() {
    try {
      this.shows = await this.getShows();
    } catch (error) {
      console.error(error);
    }
  },
  computed: {
    filteredShows() {
      // Filter shows based on the selected date and theater name
      const selectedDate = new Date(this.selectedDate);
      const keyword = this.theaterInput.trim().toLowerCase();

      if (!selectedDate.getTime() && !keyword) {
        // Display all shows if no date and theater name are selected
        return this.shows;
      }

      return this.shows.filter((show) => {
        const showDate = new Date(show.date);
        const theaterName = show.theatre_name.toLowerCase();

        // Use toDateString for date comparison
        const isDateMatch =
          !selectedDate.getTime() ||
          showDate.toDateString() === selectedDate.toDateString();

        // Use includes for partial theater name match
        const isTheaterMatch = !keyword || theaterName.includes(keyword);

        return isDateMatch && isTheaterMatch;
      });
    },
  },
  methods: {
    async getShows() {
      try {
        const response = await api.get("/shows");
        return response.data; // Return the shows data from the response
      } catch (error) {
        console.error(error);
        return []; // Return an empty array in case of an error
      }
    },
  },
};
</script>
