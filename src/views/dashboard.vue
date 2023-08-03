<template>
    <div class="dashboard">
        <h1 class="mb-3 mt-5">Movie Ticket Booking Dashboard</h1>
        <div class="form-group mb-3 mx-auto">
            <label for="theatreIdInput ">Enter Theatre ID:</label>
            <input type="number" class="mx-auto form-control w-75" id="theatreIdInput" v-model="theatreId">
        </div>
        <button class="btn btn-primary" @click="exportTheatreData">Export Theatre Data as CSV</button>
    </div>
</template>

<script>
import api from "../api"; // Import your axios instance configured with baseURL

export default {
    data() {
        return {
            theatreId: null
        };
    },
    methods: {
        exportTheatreData() {
            if (!this.theatreId) {
                alert("Please enter a valid theatre ID.");
                return;
            }

            api.get(`/theatres/${this.theatreId}/export_csv`, {
                responseType: "blob", // Set response type to blob for file download
                headers: {
                    Authorization: `Bearer ${localStorage.getItem("access_token")}` // Include JWT token in the headers
                }
            })
                .then(response => {
                    const url = window.URL.createObjectURL(new Blob([response.data]));
                    const link = document.createElement("a");
                    link.href = url;
                    link.setAttribute("download", "theatre_data.csv");
                    document.body.appendChild(link);
                    link.click();
                })
                .catch(error => {
                    console.error("Error:", error);
                });
        }
    }
};
</script>
