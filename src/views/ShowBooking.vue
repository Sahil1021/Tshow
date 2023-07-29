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
          <button @click="viewAvailableSeats(show.id)" class="btn btn-primary">
            View Available Seats
          </button>
          <button @click="bookShow(show.id)" class="btn btn-success">
            Book Tickets
          </button>
          <p v-if="!houseful && availableSeats !== null">Available Seats: {{ availableSeatsText }}</p>
          <p v-else-if="houseful">Houseful</p>
          <p v-else>Loading...</p>
        </div>
      </div>
    </div>
    <p v-else>No shows available for booking.</p>

    <!-- Available Seats Modal -->
    <div v-if="showSeatsModal" class="modal" tabindex="-1" role="dialog">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              Available Seats for {{ selectedShow.name }}
            </h5>
            <button type="button" class="close" @click="closeSeatsModal">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <p v-if="isLoadingSeats">Loading...</p>
            <template v-else-if="availableSeats !== null">
              <p v-if="availableSeats.length > 0">
                Available Seats: {{ availableSeats.join(", ") }}
              </p>
              <p v-else>No seats available for this show.</p>
            </template>
            <p v-else>No seats information available.</p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeSeatsModal">
              Close
            </button>
          </div>
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
      selectedShow: null,
      availableSeats: [],
      houseful: false,
      showSeatsModal: false,
      isLoadingSeats: false,
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


  computed: {
    availableSeatsText() {
      if (this.availableSeats !== null && Array.isArray(this.availableSeats)) {
        return this.availableSeats.join(", ");
      }
      return "";
    },
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
    async getAvailableSeats(showId) {
      try {
        const response = await api.get(`/shows/${showId}/seats`);
        return response.data.available_seats;
      } catch (error) {
        console.error(error);
        return null;
      }
    },

    async viewAvailableSeats(showId) {
      this.selectedShow = this.shows.find((show) => show.id === showId);

      this.isLoadingSeats = true;
      try {
        const availableSeats = await this.getAvailableSeats(showId);
        this.availableSeats = availableSeats;
        this.houseful = availableSeats.length === 0;
      } catch (error) {
        console.error(error);
        this.availableSeats = null;
        this.houseful = false;
      } finally {
        this.isLoadingSeats = false;
        this.showSeatsModal = true;
      }
      
    },

    closeSeatsModal() {
      this.showSeatsModal = false;
    },

    async bookShow(showId) {
      try {
        console.log("Booking show with ID:", showId);
        const numTickets = prompt("Enter the number of tickets to book:");
        if (numTickets === null || isNaN(numTickets) || parseInt(numTickets) <= 0) {
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
        const response = await api.post(`/shows/${showId}/book`, { numTickets: parseInt(numTickets) }, { headers });

        console.log(response.data);

        // Update the available seats after booking
        const updatedShow = this.shows.find((show) => show.id === showId);
        if (updatedShow) {
          updatedShow.available_seats -= parseInt(numTickets);
          this.availableSeats = updatedShow.available_seats; // Update the available seats for the selected show
          this.houseful = updatedShow.available_seats === 0; // Update houseful flag
        }

        // this.availableSeatsText = this.availableSeats.join(", ");

        // Refresh the available seats after booking
        this.refreshAvailableSeats(showId);
        alert("Booking is Successful!!");

      } catch (error) {
        console.error(error);
      }
    },

    async refreshAvailableSeats(showId) {
      try {
        // Fetch the updated available seats for the show
        const response = await api.get(`/shows/${showId}/seats`);
        const updatedAvailableSeats = response.data.available_seats;

        // Update the availableSeats data
        this.availableSeats = updatedAvailableSeats;

        // Update the houseful flag
        this.houseful = updatedAvailableSeats.length === 0;
      } catch (error) {
        console.error(error);
        this.availableSeats = null;
      }
    },

  },
};
</script>