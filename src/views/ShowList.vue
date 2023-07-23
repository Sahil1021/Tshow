<template>
    <div class="container">
        <h1 class="mb-3">Shows List</h1>
        <div class="form-group">
            <label for="theaterInput w-50">Enter Theater Name:</label>
            <input type="text" class="form-control" id="theaterInput" v-model="theaterInput" />
            <button class="btn btn-primary mt-2" @click="filterShowsByTheater">
                Search
            </button>
        </div>
        <div class="row mt-3" v-if="filteredShows.length > 0">
            <div class="col-12 col-sm-6 col-md-6 mb-4" v-for="show in filteredShows" :key="show.id">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title text-decoration-underline">Show {{ show.id }}</h5>
                        <p class="card-text">Show Name: {{ show.name }}</p>
                        <p class="card-text">Theater Name: {{ show.theatre_name }}</p>
                        <p class="card-text">Show Time: {{ show.time }}</p>
                    </div>
                </div>
            </div>
        </div>
        <p v-else>No shows found for the given theater.</p>
        <router-link to="/shows/create" class="btn btn-primary mb-4">Create New Show</router-link>
    </div>
</template>

<script>
import api from "../api";

export default {
    data() {
        return {
            shows: [],
            filteredShows: [],
            theaterInput: "", // Input field to get theater name from the user
        };
    },
    async created() {
        try {
            this.shows = await this.getShows();
            this.filteredShows = this.shows; // Display all shows initially
        } catch (error) {
            console.error(error);
        }
    },
    methods: {
        async getShows() {
            try {
                const response = await api.get("/shows");
                return response.data; // Return the shows data from the response
            } catch (error) {
                console.error(error);
                return []; // Return an empty array in case of an error
            }
        },
        viewTheaterLayout(theaterId) {
            this.$router.push({ name: "TheaterLayout", params: { theatreId: theaterId } });
            console.log("View theater layout for theater with ID:", theaterId);
        },
        filterShowsByTheater() {
            // Filter shows based on the theater name input by the user
            const keyword = this.theaterInput.trim().toLowerCase();
            if (!keyword) {
                this.filteredShows = this.shows; // Display all shows if no keyword is provided
            } else {
                this.filteredShows = this.shows.filter((show) => {
                    const theaterName = show.theatre_name.toLowerCase();
                    return theaterName === keyword; // Use strict equality for exact match
                });
            }
        },
    },
};
</script>
