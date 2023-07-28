<template>
  <div class="container">
    <h1>Your Booked Shows</h1>
    <div v-if="bookedShows.length > 0">
      <div class="card mb-3" v-for="show in bookedShows" :key="show.id">
        <div class="card-body">
          <h5 class="card-title">{{ show.name }}</h5>
          <p class="card-text">Genre: {{ show.genre }}</p>
          <p class="card-text">Theater Name: {{ show.theatre_name }}</p>
          <p class="card-text">Theater address: {{ show.theatre_address }}</p>
          <p class="card-text">Date: {{ show.date }}</p>
          <p class="card-text">Show Time: {{ show.time }}</p>
          <p class="card-text">Ticket Price: {{ show.ticket_price }}</p>
          <p class="card-text">Description: {{ show.description }}</p>
        </div>
      </div>
    </div>
    <p v-else>No shows booked yet.</p>
  </div>
</template>

<script>
// import api from "../api";
import axios from "axios";

export default {
  data() {
    return {
      bookedShows: [],
    };
  },
  created() {
        // Check if the user is authenticated and has a valid JWT token
        const userToken = localStorage.getItem('accessToken');
        if (!userToken) {
            // Handle the case where the user is not authenticated
            // Redirect to login page or display an error message
            return;
        }

        // Make the API call to fetch user bookings
        this.getUserBookings(userToken);
    },
  methods: {
        async getUserBookings(token) {
            try {
                const response = await axios.get('http://localhost:5000/api/shows/UserBookings', {
                    headers: {
                        Authorization: `Bearer ${token}`, // Include the JWT token in the request headers
                    },
                });
                // Process the response and update your component data with the user bookings
            } catch (error) {
                // Handle the error, display appropriate error message, or redirect to an error page
                console.error('Error fetching user bookings:', error);
            }
        },
  },
};
</script>

<style>
/* Add any custom CSS styles here */
</style>
