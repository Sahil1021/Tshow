<template>
    <div class="container">
        <h1 class="mb-3">Edit Theatre</h1>
        <form @submit.prevent="updateTheatre">
            <div class="form-group">
                <label for="nameInput">Theatre Name:</label>
                <input v-model="form.name" type="text" class="form-control" id="nameInput" required />
            </div>
            <div class="form-group">
                <label for="addressInput">Theatre Address:</label>
                <input v-model="form.address" type="text" class="form-control" id="addressInput" required />
            </div>
            <div class="form-group">
                <label for="capacityInput">Capacity:</label>
                <input v-model.number="form.capacity" type="number" class="form-control" id="capacityInput" required />
            </div>
            <button type="submit" class="btn btn-primary">Update Theatre</button>
        </form>
    </div>
</template>


<script>
import api from "../api";

export default {
    data() {
        return {
            form: {
                name: "",
                address: "",
                capacity: 0,
            },
        };
    },
    async created() {
        // Fetch the theatre data for editing and set it to the form
        const theatreId = this.$route.params.id;
        try {
            const response = await api.get(`/theatres/${theatreId}`);
            this.form = response.data;
        } catch (error) {
            console.error("Error fetching theatre data for editing:", error);
        }
    },
    methods: {
        async updateTheatre() {
            const theatreId = this.$route.params.id;
            try {
                const response = await api.put(`/theatres/${theatreId}`, this.form);
                console.log("Update Theatre Response:", response);

                if (response.status === 200) {
                    // Show success alert
                    alert("Theatre updated successfully!");
                    // Redirect back to the TheatreList page after updating
                    this.$router.push({ name: "TheatresList" });
                }
            } catch (error) {
                console.error("Error updating theatre:", error);
            }
        },
    },
};
</script>