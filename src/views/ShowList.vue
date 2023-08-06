<template>
  <div class="container">
    <h1 class="mb-3">Shows List</h1>
    <div class="form-group w-50 mx-auto">
      <label for="dateInput">Filter shows by Date:</label>
      <input type="date" class="form-control" id="dateInput" v-model="selectedDate" @change="filterShows" />
    </div>
    <div class="form-group w-50 mx-auto">
      <label for="theaterInput">Filter shows by Theater Name:</label>
      <input type="text" class="form-control" id="theaterInput" v-model="theaterInput" @input="searchByTheater" />
    </div>
    <div class="row mt-3" v-if="filteredShows.length > 0">
      <div class="col-12 col-sm-6 col-md-6 mb-4" v-for="show in filteredShows" :key="show.id">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title text-decoration-underline">
              Show {{ show.id }}
            </h5>
            <p class="card-text">Show Name: {{ show.name }}</p>
            <p class="card-text">Genre: {{ show.genre }}</p>
            <p class="card-text">Theater Name: {{ show.theatre_name }}</p>
            <p class="card-text">Theater address: {{ show.theatre_address }}</p>
            <p class="card-text">Date: {{ show.date }}</p>
            <p class="card-text">Show Time: {{ show.time }}</p>
            <p class="card-text">Ticket Price: {{ show.ticket_price }}</p>
            <p class="card-text">Description: {{ show.description }}</p>

            <div class="d-flex justify-content-center">
              <router-link :to="{ name: 'EditShow', params: { id: show.id } }" class="btn btn-primary mr-2">
                <i class="fa fa-edit"></i> Edit
              </router-link>
              <button @click="showDeleteConfirmation(show.id)" class="btn btn-danger ml-2">
                <i class="fa fa-trash"></i> Delete
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    <p v-else>No shows found for the selected date and theater.</p>
    <router-link to="/shows/create" class="btn btn-primary mb-4">Create New Show</router-link>

    <div v-if="showConfirmationPrompt" class="confirmation-prompt">
      <div class="prompt-container bg-white p-4 rounded">
        <p>Are you sure you want to delete this show?</p>
        <div class="d-flex justify-content-end">
          <button @click="deleteShow" class="btn btn-danger">Delete</button>
          <button @click="cancelDeletion" class="btn btn-secondary ml-2">
            Cancel
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from "../api";

export default {
  data() {
    return {
      shows: [],
      selectedDate: "",
      theaterInput: "",
      showConfirmationPrompt: false,
      selectedShowId: null,
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
      const selectedDate = new Date(this.selectedDate);
      const keyword = this.theaterInput.trim().toLowerCase();
      const currentDateTime = new Date(); // Get the current date and time

      if (!selectedDate.getTime() && !keyword) {
        return this.shows;
      }

      return this.shows.filter((show) => {
        const showDate = new Date(show.date);
        const showTime = show.time.split(":"); // Splitting the time string
        const showDateTime = new Date(showDate);

        // Set the hours and minutes of the showDateTime
        showDateTime.setHours(Number(showTime[0]), Number(showTime[1]));

        const theaterName = show.theatre_name.toLowerCase();

        const isDateMatch =
          !selectedDate.getTime() ||
          showDate.toDateString() === selectedDate.toDateString();

        const isTheaterMatch = keyword === "" || theaterName === keyword;

        // Compare the combined date and time of the show against the current date and time
        const isFutureShow = showDateTime > currentDateTime;

        return isDateMatch && isTheaterMatch && isFutureShow;
      });
    },
  },
  methods: {
    hasShowPassed(showDateTime) {
      const currentDateTime = new Date();
      return showDateTime < currentDateTime;
    },
    async getShows() {
      try {
        const response = await api.get("/shows");
        return response.data;
      } catch (error) {
        console.error(error);
        return [];
      }
    },

    showDeleteConfirmation(showId) {
      this.selectedShowId = showId;
      this.showConfirmationPrompt = true;
    },

    cancelDeletion() {
      this.showConfirmationPrompt = false;
    },
    deleteShow() {
      // Construct the request data to include the theatre_id
      const requestData = {
        theatre_id:
          this.shows.find((show) => show.id === this.selectedShowId)
            ?.theatre_id || null,
      };

      api
        .delete(`/shows/${this.selectedShowId}`, { data: requestData })
        .then((response) => {
          if (response.status === 200) {
            this.shows = this.shows.filter(
              (show) => show.id !== this.selectedShowId
            );
            console.log("Show deleted successfully");
          } else {
            console.error("Error deleting show:", response.data.error);
          }
        })
        .catch((error) => {
          console.error("Error deleting show:", error);
        });

      this.showConfirmationPrompt = false;
    },
  },
};
</script>
