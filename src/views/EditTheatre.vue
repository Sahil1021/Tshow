<template>
    <p>Edit Theatre Page</p>
</template>
<!-- <template>
    <div class="container w-50">
        <h1 class="mb-3">Edit Theatre</h1>
        <form @submit.prevent="updateTheatre">
            <div class="form-group">
                <label>Name:</label>
                <input class="mb-3 form-control" v-model="editedTheatre.name" type="text" required/>
            </div>
            <div class="form-group">
                <label>Address:</label>
                <input class="mb-3 form-control" v-model="editedTheatre.address" type="text" required />
            </div>
            <div class="form-group">
                <label>Capacity:</label>
                <input class="mb-3 form-control mb-3" v-model="editedTheatre.capacity" type="number" required />
            </div>
            <button class="btn btn-primary" type="submit">Update Theatre</button>
            <router-link to="/theatres" class="btn btn-secondary ml-2">Cancel</router-link> 

        </form>
    </div>
</template>

<script>
import api from "../api";

export default {
    data() {
        return {
            editedTheatre: {
                name: "",
                address: "",
                capacity: 0,
            },
        };
    },
    async created() {
        try {
            const theatreId = this.$route.params.id; // Get the theatre ID from the route parameter
            const response = await api.get(`/theatres/${theatreId}`);
            this.editedTheatre = response.data; // Set the fetched theatre data to the editedTheatre object
        } catch (error) {
            console.error(error);
        }
    },

    methods: {
        async updateTheatre() {
            try {
                const theatreId = this.$route.params.id;
                await api.put(`/theatres/edit/${theatreId}`, this.editedTheatre);
                alert("Theatre updated successfully!");
                this.$router.push("/theatres");
            } catch (error) {
                console.error(error);
            }
        },
    },
};
</script> -->