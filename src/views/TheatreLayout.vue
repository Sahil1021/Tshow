<template>
    <div class="container">
        <h1>Theater Layout for {{ theater.name }}</h1>
        <p>Theater Capacity: {{ theater.capacity }}</p>
        <div class="theater-layout">
            <div class="seat" v-for="seatNumber in theater.capacity" :key="seatNumber"
                :class="{ 'seat-booked': isSeatBooked(seatNumber) }">
                {{ seatNumber }}
            </div>
        </div>
    </div>
</template>

<style>
.theater-layout {
    display: flex;
    flex-wrap: wrap;
    gap: 5px;
    margin-top: 20px;
}

.seat {
    width: 40px;
    height: 40px;
    background-color: lightgray;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 1px solid #ccc;
}

.seat-booked {
    background-color: red;
    cursor: not-allowed;
}
</style>

<script>
import api from "../api";

export default {
    data() {
        return {
            theater: null,
            bookedSeats: [],
        };
    },
    async created() {
        try {
            const theaterId = this.$route.params.theatreId;
            this.theater = await this.getTheaterById(theaterId);
            this.bookedSeats = await this.getBookedSeatsByTheater(theaterId);
        } catch (error) {
            console.error(error);
        }
    },
    methods: {
        async getTheaterById(theaterId) {
            try {
                const response = await api.get(`/theatres/${theaterId}`);
                return response.data;
            } catch (error) {
                console.error(error);
                return null;
            }
        },
        async getBookedSeatsByTheater(theaterId) {
            try {
                const response = await api.get(`/theatres/${theaterId}/booked-seats`);
                return response.data;
            } catch (error) {
                console.error(error);
                return [];
            }
        },
        isSeatBooked(seatNumber) {
            return this.bookedSeats.includes(seatNumber);
        },
    },
};
</script>
