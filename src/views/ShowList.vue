<template>
    <div>
        <h1>Show List for {{ theatreName }}</h1>
        <ul v-if="shows.length > 0">
            <li v-for="show in shows" :key="show.id">
                <strong>Show Name:</strong> {{ show.name }}
                <br />
                <strong>Show Time:</strong> {{ show.time }}
            </li>
        </ul>
        <p v-else>No shows found for this theater.</p>
        <p v-if="error">{{ error }}</p>
    </div>
</template>

<script>
import api from "../api";

export default {
    data() {
        return {
            theatreName: this.$route.params.theatreName,
            shows: [],
            error: "",
        };
    },
    async created() {
        try {
            this.shows = await this.getShowsByTheatreName(this.theatreName);
        } catch (error) {
            console.error(error);
            this.error = "An error occurred while fetching shows.";
        }
    },
    methods: {
        async getShowsByTheatreName(theatreName) {
            const response = await api.get(`/api/theatres/${theatreName}/shows`);
            return response.data;
        },
    },
};
</script>
