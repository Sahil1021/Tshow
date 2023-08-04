<template>
  <div class="container">
    <h1 class="mb-3">Theatres List</h1>
    <div class="row mt-3">
      <div class="col-12 col-sm-6 col-md-6 mb-4" v-for="theatre in theatres" :key="theatre.id">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title text-decoration-underline">
              Theatre ID: {{ theatre.id }}
            </h5>
            <p class="card-text">Theatre Name: {{ theatre.name }}</p>
            <p class="card-text">Theatre Address: {{ theatre.address }}</p>
            <p class="card-text">Capacity: {{ theatre.capacity }}</p>
            <div class="d-flex justify-content-center">
              <button @click="editTheatre(theatre.id)" class="btn btn-primary mr-2">
                <i class="fa fa-edit"></i> Edit
              </button>
              <button @click="showDeleteConfirmation(theatre.id)" class="btn btn-danger ml-2">
                <i class="fa fa-trash"></i> Delete
              </button>
              <div class="d-flex justify-content-center">
                <router-link :to="{ name: 'TheatreShows', params: { id: theatre.id } }" class="btn btn-warning ml-2">
                  <i class="fa fa-trash"></i> View shows
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <router-link to="/theatres/create" class="btn btn-primary mb-4">Create New Theatre</router-link>

    <div v-if="showConfirmationPrompt" class="confirmation-prompt">
      <div class="prompt-container bg-white p-4 rounded">
        <p>Are you sure you want to delete this theatre?</p>
        <div class="d-flex justify-content-end">
          <button @click="deleteTheatre" class="btn btn-danger">Delete</button>
          <button @click="cancelDeletion" class="btn btn-secondary ml-2">Cancel</button>
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
      theatres: [],
      selectedTheatreId: null,
      showConfirmationPrompt: false,
    };
  },
  async created() {
    try {
      this.theatres = await this.getTheatres();
    } catch (error) {
      console.error(error);
    }
  },
  methods: {
    async getTheatres() {
      try {
        const response = await api.get("/theatres");
        return response.data;
      } catch (error) {
        console.error(error);
        return [];
      }
    },
    editTheatre(theatreId) {
      this.$router.push({ name: "EditTheatre", params: { id: theatreId } });
    },
    showDeleteConfirmation(theatreId) {
      this.selectedTheatreId = theatreId;
      this.showConfirmationPrompt = true;
    },
    cancelDeletion() {
      this.showConfirmationPrompt = false;
    },
    deleteTheatre() {
      // Perform the deletion operation here using API call
      // You can use Axios or Fetch API to send a DELETE request to your backend
      api.delete(`/theatres/${this.selectedTheatreId}`) // Corrected the URL here
        .then((response) => {
          if (response.status === 200) {
            // Deletion was successful, remove the theater from the list
            this.theatres = this.theatres.filter(
              (theatre) => theatre.id !== this.selectedTheatreId
            );
            console.log("Theatre deleted successfully");
          } else {
            console.error("Error deleting theatre:", response.data.error);
          }
        })
        .catch((error) => {
          console.error("Error deleting theatre:", error);
        });

      // Hide the confirmation prompt
      this.showConfirmationPrompt = false;
    },
  },
};
</script>

<style>
.confirmation-prompt {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}
</style>