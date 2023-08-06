<template>
    <div class="container">
        <h1 class="mb-3">Shows List for : {{ theatreName }}</h1>
        <div class="row mt-3">
            <div class="col-12 col-sm-6 col-md-6 mb-4" v-for="show in shows" :key="show.id">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title text-decoration-underline">Show ID: {{ show.id }}</h5>
                        <p class="card-text">Show Name: {{ show.name }}</p>
                        <p class="card-text">Date: {{ show.date }}</p>
                        <p class="card-text">Time: {{ show.time }}</p>
                        <p class="card-text">Description: {{ show.description }}</p>
                        <p class="card-text">Genre: {{ show.genre }}</p>
                        <p class="card-text">Ticket Price: {{ show.ticket_price }}</p>
                        <p class="card-text">Available Seats: {{ show.available_seats }}</p>
                        <p class="btn btn-warning" v-if="show.available_seats === 0">
                            Houseful
                        </p>
                        <br />
                        <button v-if="showBookingClosed(show.date, show.time)" class="btn btn-danger" disabled>
                            Past Show - Booking Closed
                        </button>
                        <button v-else-if="show.available_seats != 0 && !showBookingClosed(show.date, show.time)"
                            class="btn btn-primary">
                            Booking Open
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
            theatreName: "",
            shows: [],
        };
    },
    async created() {
        const theatreId = this.$route.params.id;
        try {
            const response = await api.get(`/theatres/${theatreId}`);
            this.theatreName = response.data.name;
            this.shows = await this.getShowsForTheatre(theatreId); // Fetch shows for the selected theater
        } catch (error) {
            console.error(error);
        }
    },
    methods: {
        async getShowsForTheatre(theatreId) {
            try {
                const response = await api.get(`/theatres/${theatreId}/shows`); // Fetch shows for the theater using the API
                // Filter the shows to only include those with a date greater than or equal to today's date
                const currentDate = new Date().toISOString().split("T")[0];
                const filteredShows = response.data.filter((show) => show.date >= currentDate);
                return filteredShows;
            } catch (error) {
                console.error(error);
                return [];
            }
        },
        hasShowPassed(showDate) {
            const currentDateTime = new Date();
            const [showDateOnly] = showDate.split("T");
            const showDateTime = new Date(`${showDateOnly}T00:00:00`);
            return showDateTime < currentDateTime;
        },
        showBookingClosed(showDate, showTime) {
            const currentDateTime = new Date();
            const [showDateOnly] = showDate.split("T");
            const showDateTime = new Date(`${showDateOnly}T${showTime}`);
            return showDateTime < currentDateTime;
        },

        bookTicket(show) {
            // Implement the logic to book tickets for the selected show
            // You can navigate to a ticket booking page or display a modal for booking
            // For this example, I'll just log a message to the console
            console.log("Booking ticket for show:", show);
        },
    },
};
</script>