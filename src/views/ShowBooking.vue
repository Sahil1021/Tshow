<template>
  <div class="container">
    <h1>Book Shows</h1>
    <div v-if="shows.length > 0">
      <div class="card mb-3" v-for="show in shows" :key="show.id">
        <div class="card-body">
          <h5 class="card-title">{{ show.name }}</h5>
          <p class="card-text">Genre: {{ show.genre }}</p>
          <p class="card-text">Theater Name: {{ show.theatre_name }}</p>
          <p class="card-text">Theater address: {{ show.theatre_address }}</p>
          <p class="card-text">Date: {{ show.date }}</p>
          <p class="card-text">Show Time: {{ show.time }}</p>
          <p class="card-text">Ticket Price: {{ show.ticket_price }}</p>
          <p class="card-text">Description: {{ show.description }}</p>

          <p class="btn btn-warning" v-if="show.available_seats === 0">
            Houseful
          </p>
          <p v-else-if="show.available_seats !== null">
            Available Seats: {{ show.available_seats }}
          </p>
          <p v-else>Loading...</p>
          <br />
          <!-- Display loading message while fetching available seats -->

          <!-- <button @click="bookShow(show.id)" class="btn btn-success">
            Book Tickets
          </button> -->
          <button
            @click="bookShow(show.id)"
            class="btn btn-success"
            :disabled="show.available_seats === 0"
          >
            Book Tickets
          </button>
        </div>
      </div>
    </div>
    <p v-else>No shows available for booking.</p>
  </div>
</template>

<script>
import api from "../api";

export default {
  data() {
    return {
      shows: [],
    };
  },
  async created() {
    try {
      const allShows = await this.getAvailableShows();
      const currentDateTime = new Date();

      // Filter shows to keep only those with date and time greater than current date and time
      this.shows = allShows.filter((show) => {
        const showDateTime = new Date(`${show.date}T${show.time}`);
        return showDateTime > currentDateTime;
      });
    } catch (error) {
      console.error(error);
    }
  },

  methods: {
    async getAvailableShows() {
      try {
        const response = await api.get("/shows");
        return response.data;
      } catch (error) {
        console.error(error);
        return [];
      }
    },

    async bookShow(showId) {
      try {
        console.log("Booking show with ID:", showId);
        const numTickets = prompt("Enter the number of tickets to book:");
        if (
          numTickets === null ||
          isNaN(numTickets) ||
          parseInt(numTickets) <= 0
        ) {
          return;
        }

        // Get the JWT token from Local Storage
        const token = localStorage.getItem("access_token");

        // Check if the token is available
        if (!token) {
          console.error("JWT token not available");
          return;
        }

        // Include the JWT token in the request headers
        const headers = {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        };

        // Make the POST request to book the show with the JWT token in the header
        const response = await api.post(
          `/shows/${showId}/book`,
          { numTickets: parseInt(numTickets) },
          { headers }
        );

        console.log(response.data);

        // Update the available seats for the selected show
        const updatedShow = this.shows.find((show) => show.id === showId);
        if (updatedShow) {
          updatedShow.available_seats -= parseInt(numTickets);
        }

        alert("Booking is Successful!!");
      } catch (error) {
        console.error(error);
      }
    },
  },
};
</script>
