<template>
    <div>
        <h1>Create a New Show</h1>
        <form class="container w-25" @submit.prevent="createShow">
            <label>Theatre ID:</label>
            <input class="form-control" v-model="theatre_id" type="number" required />
            <br />
            <label>Show Name:</label>
            <input class="form-control" v-model="showName" type="text" required />
            <br />
            <label>Show Time:</label>
            <input class="form-control" v-model="showTime" type="text" required />
            <br />
            <button class="btn btn-primary" type="submit">Create Show</button>
        </form>
        <p v-if="errorMessage">{{ errorMessage }}</p>
    </div>
</template>

<script>
import api from "../api";
export default {
    data() {
        return {
            theatre_id: "",
            showName: "",
            showTime: "",
            errorMessage: "",
        };
    },
    methods: {
        async createShow() {
            try {
                const showData = {
                    theatre_id: this.theatre_id,
                    name: this.showName,
                    time: this.showTime,
                    
                };
                await api.post("/shows", showData);
                alert("Show created successfully!");
                // Clear form inputs after creating a show
                this.theatre_id = "";
                this.showName = "";
                this.showTime = "";
                this.errorMessage = "";
            } catch (error) {
                if (error.response && error.response.status === 404) {
                    this.errorMessage = "Theater not found. Please provide a valid Theater ID.";
                } else {
                    this.errorMessage = "An error occurred while creating the show.";
                }
                console.error(error);
            }
        },
    },
};
</script>
