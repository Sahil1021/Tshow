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
            <p v-if="availableSeats.length > 0">
              Available Seats: {{ availableSeats.join(", ") }}
            </p>
            <p v-else>No seats available for this show.</p>
          </div>
          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-secondary"
              @click="closeSeatsModal"
            >
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
      showSeatsModal: false,
    };
  },
  async created() {
    try {
      this.shows = await this.getAvailableShows();
    } catch (error) {
      console.error(error);
    }
  },
  methods: {
    async getAvailableShows() {
      try {
        const response = await api.get("/shows");
        return response.data; // Return the shows data from the response
      } catch (error) {
        console.error(error);
        return []; // Return an empty array in case of an error
      }
    },
    async getAvailableSeats(showId) {
      try {
        const response = await api.get(`/shows/${showId}/seats`);
        return response.data; // Return the available seats data from the response
      } catch (error) {
        console.error(error);
        return []; // Return an empty array in case of an error
      }
    },
    viewAvailableSeats(showId) {
      this.selectedShow = this.shows.find((show) => show.id === showId);
      this.availableSeats = this.getAvailableSeats(showId);
      this.showSeatsModal = true;
    },
    closeSeatsModal() {
      this.showSeatsModal = false;
    },
    async bookShow(showId) {
      try {
        console.log("Booking show with ID:", showId);
        const numTickets = prompt("Enter the number of tickets to book:");
        if (numTickets === null || isNaN(numTickets)) {
          return;
        }

        const response = await api.post(`/shows/${showId}/book`, {
          numTickets: parseInt(numTickets),
        });
        if (response.status === 200) {
          // Booking was successful
          await this.updateAvailableSeats(showId);
          this.shows = await this.getAvailableShows();
          alert("Show booked successfully.");
        } else {
          // Booking failed
          alert("Failed to book the show.");
        }
      } catch (error) {
        console.error(error);
        alert("Failed to book the show.");
      }
    },
    async updateAvailableSeats(showId) {
      // You can implement your update logic here, for example, by making an API request to update the available seats after booking.
      try {
        const response = await api.get(`/shows/${showId}/seats`);
        if (response.status === 200) {
          // Update available seats in the component state
          this.availableSeats = response.data;
        } else {
          console.log("Failed to fetch available seats.");
        }
      } catch (error) {
        console.error(error);
        alert("Failed to fetch available seats.");
      }
    },
  },
};
</script>
