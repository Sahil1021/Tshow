<template>
    <div class="container">
        <h1>Your Booked Shows</h1>
        <div class="d-flex flex-wrap">
            <div class="col-12 col-sm-6 col-md-4 mb-4 mr-5" v-for="booking in userBookings" :key="booking.id">
                <div class="card">
                    <div class="card-body">
                        <strong>
                            <h5 class="card-title">{{ booking.show.name }}</h5>
                        </strong>
                        <!-- <p class="card-text">Genre: {{ booking.show.genre }}</p> -->
                        <p class="card-text">Theater Name: {{ booking.show.theatre_name }}</p>
                        <p class="card-text">Theater address: {{ booking.show.theatre_address }}</p>
                        <p class="card-text">Date: {{ booking.show.date }}</p>
                        <p class="card-text">Show Time: {{ booking.show.time }}</p>
                        <p class="card-text">Description: {{ booking.show.description }}</p>
                        <p class="card-text">Ticket Price: {{ booking.show.ticket_price }}</p>
                        <p class="card-text">Number of Tickets: {{ booking.num_tickets }}</p>
                        <p class="card-text btn btn-success">Total Amount Paid: {{
                            calculateTotalAmount(booking.show.ticket_price, booking.num_tickets) }}</p>
                        <p class="card-text">Booked On: {{ booking.booking_date }}</p>
                        
                        <!-- <p class="card-text">Booked By: {{ booking.user_id }}</p> Display the username here -->
                    </div>
                </div>
            </div>
        </div>
        <p v-if="userBookings.length === 0">No shows booked yet.</p>
    </div>
</template>


<script>
import axios from 'axios';
import { sortBy } from 'lodash';

export default {
    data() {
        return {
            userBookings: [], // Initialize as an empty array
        };
    },
    async created() {
        // Check if the user is authenticated and has a valid JWT token
        const userToken = localStorage.getItem('access_token');
        if (!userToken) {
            // Handle the case where the user is not authenticated
            console.error('User not authenticated.');
            return;
        }

        // Make the API call to fetch user bookings
        try {
            const response = await axios.get('http://localhost:5000/api/shows/UserBookings', {
                headers: {
                    Authorization: `Bearer ${userToken}`, // Include the JWT token in the request headers
                },
            });
            this.userBookings = response.data;

            // Sort the userBookings array based on the booking id in descending order (newly booked shows first)
            this.userBookings = sortBy(this.userBookings, (booking) => -booking.id);
        } catch (error) {
            // Handle the error
            console.error('Error fetching user bookings:', error);
        }
    },
    methods: {
        async getUserBookings(token) {
            try {
                const response = await axios.get('http://localhost:5000/api/shows/UserBookings', {
                    headers: {
                        Authorization: `Bearer ${token}`, // Include the JWT token in the request headers
                    },
                });
                this.userBookings = response.data;
            } catch (error) {
                // Handle the error
                console.error('Error fetching user bookings:', error);
            }
        },

        formatDate(dateTimeStr) {
            try {
                // Check if the date is valid
                const date = new Date(dateTimeStr);
                if (!isNaN(date)) {
                    // Format the valid date
                    const formattedDate = date.toLocaleDateString();
                    const formattedTime = date.toLocaleTimeString();
                    return `${formattedDate} ${formattedTime}`;
                } else {
                    return 'Invalid Date';
                }
            } catch (error) {
                console.error('Error parsing date:', error);
                return 'Invalid Date';
            }
        },
        
    },
    computed: {
        calculateTotalAmount() {
            return function (ticketPrice, numTickets) {
                return (ticketPrice * numTickets).toFixed(2); // Assuming ticketPrice is in float format
            };
        },
    },
};
</script>
