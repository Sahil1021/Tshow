<template>
  <div class="container">
    <h1 class="mt-5">Book Shows</h1>
    <div class="w-50" v-if="shows.length > 0">
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

          <p>Average Rating: {{ show.average_rating.toFixed(2) }}</p>
          <p>Number of Ratings: {{ show.num_ratings }}</p>
          <!-- <button @click="rateShow(show.id, show)" class="btn btn-primary">Rate Show</button> -->
          <button @click="rateShow(show.id, show)" class="btn btn-primary"
            :disabled="ratedByUser || ratedShows.includes(show.id)">
            {{ show.ratedByUser ? 'Rated' : 'Rate Show' }}
          </button>

          <button @click="bookShow(show.id)" class="btn btn-success" :disabled="show.available_seats === 0">
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
import { sortBy } from 'lodash';

export default {

  data() {
    return {
      shows: [],
      ratedShows: [],

    };
  },

  async created() {
    try {
      this.ratedShows = await this.getUserRatedShows();
      const allShows = await this.getAvailableShows();
      const currentDateTime = new Date();

      // Sort shows in descending order based on their creation date (assuming there is a `created_at` property)
      this.shows = sortBy(allShows, (show) => new Date(show.created_at)).reverse();

      // Filter shows to keep only those with date and time greater than current date and time
      this.shows = this.shows.filter((show) => {
        const showDateTime = new Date(`${show.date}T${show.time}`);
        const isDateInPast = showDateTime < currentDateTime;
        const isTodayShow = show.date === currentDateTime.toISOString().split("T")[0];

        // Return shows that have a future date or shows with today's date but show time is not yet passed
        return !isDateInPast || (isTodayShow && showDateTime > currentDateTime);
      });
      this.shows.forEach((show) => {
        show.average_rating = show.average_rating || 0;
        show.num_ratings = show.num_ratings || 0;
        show.ratedByUser = false; // Initialize the ratedByUser property
      });
    } catch (error) {
      console.error(error);
    }

  },

  methods: {
    async getUserRatedShows() {
      try {
        const token = localStorage.getItem("access_token");
        if (!token) {
          console.error("JWT token not available");
          return [];
        }

        const headers = {
          Authorization: `Bearer ${token}`,
        };

        const response = await api.get("/shows/UserRatedShows", { headers });
        return response.data;
      } catch (error) {
        console.error(error);
        return [];
      }
    },

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

    async rateShow(showId, show) {
      if (show.ratedByUser) {
        alert("You have already rated this show.");
        return;
      }
      try {

        const rating = parseFloat(prompt("Enter your rating (0-5):"));
        if (isNaN(rating) || rating < 0 || rating > 5) {
          alert("Invalid rating. Please provide a rating between 0 and 5.");
          return;
        }

        const token = localStorage.getItem("access_token");
        if (!token) {
          console.error("JWT token not available");
          return;
        }

        const headers = {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        };

        const response = await api.post(
          `/shows/${showId}/rate`,
          { rating },
          { headers }
        );

        console.log(response.data);
        alert("Show rated successfully!");

        // Update the frontend show data with the updated ratings from the response
        show.average_rating = response.data.average_rating;
        show.num_ratings = response.data.num_ratings;

        show.ratedByUser = true; // Mark the show as rated by the user
        this.ratedShows.push(showId); // Add the show ID to the ratedShows list


      } catch (error) {
        console.error(error);
        if (error.response && error.response.status === 400) {
          // Show an alert indicating that the show has already been rated

          alert("You've already rated this show.");
        } else {
          // Handle other error cases
          console.error("An error occurred:", error);
        }
      }
    }


  },

};
</script>