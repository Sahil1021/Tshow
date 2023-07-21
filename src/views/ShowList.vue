<template>
    <div>
        <h1>Shows List</h1>
        <ul>
            <li v-for="show in shows" :key="show.id">
                {{ show.id }} - {{ show.name }} - {{ show.address }}
            </li>

        </ul>
        <router-link to="/shows/create">Create New show</router-link>
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
            this.shows = await this.getShows(); // Call the getTheatres method
        } catch (error) {
            console.error(error);
        }
    },
    methods: {
        async getShows() {
            const response = await api.get("/shows");
            return response.data; // Return the data from the response
        },
    },
};
</script>