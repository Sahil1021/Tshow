<template>
  <div class="container">
    <h1 class="mb-3">Theatres List</h1>
    <div class="row mt-3">
      <div class="col-12 col-sm-6 col-md-6 mb-4" v-for="theatre in theatres" :key="theatre.id">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title text-decoration-underline">Theatre ID:  {{ theatre.id }}</h5>
            <p class="card-text">Theatre Name: {{ theatre.name }}</p>
            <p class="card-text">Theatre Address: {{ theatre.address }}</p>
            <p class="card-text">Capacity: {{ theatre.capacity }}</p>
            <div class="d-flex justify-content-center">
              <button @click="editTheatre(theatre.id)" class="btnmargin btn btn-primary mr-5">
                <i class="fa fa-edit"></i> Edit
              </button>
              <button @click="deleteTheatre(theatre.id)" class="btn btn-danger ml-2">
                <i class="fa fa-trash"></i> Delete
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    <router-link to="/theatres/create" class="btn btn-primary mb-4">Create New Theatre</router-link>
  </div>
</template>

<style>
.btnmargin {
  margin-right: 5px;
}
</style>
<script>
import api from "../api";

export default {
  data() {
    return {
      theatres: [],
    };
  },
  async created() {
    try {
      this.theatres = await this.getTheatres(); // Call the getTheatres method
    } catch (error) {
      console.error(error);
    }
  },
  methods: {
    async getTheatres() {
      try {
        const response = await api.get("/theatres");
        return response.data; // Return the data from the response
      } catch (error) {
        console.error(error);
        return []; // Return an empty array in case of an error
      }
    },
    editTheatre(theatreId) {
      this.$router.push({ name: "EditTheatre", params: { id: theatreId } });
      // Handle the edit action, e.g., navigate to the edit page
      console.log("Edit theatre with ID:", theatreId);
    },

    async deleteTheatre(theatreId) {
      try {
        const response = await api.delete(`/theatres/${theatreId}`);
        if (response.status === 204) {
          this.theatres = this.theatres.filter((theatre) => theatre.id !== theatreId);
          console.log("Theatre deleted successfully");
        }
      } catch (error) {
        console.error("Error deleting theatre:", error);
      }
    },

  },
};
</script>

<!-- <template>
  <div>
    <h1>Theatres List</h1>
    <ul>
      <li v-for="theatre in theatres" :key="theatre.id">
        {{ theatre.name }} - {{ theatre.address }}
      </li>
    </ul>
    <router-link to="/theatres/create">Create New Theatre</router-link>
  </div>
</template>

<script>
import api from "../api";
export default {
  data() {
    return {
      theatres: [],
    };
  },
  async created() {
    try {
      this.theatres = await this.getTheatres(); // Call the getTheatres method
    } catch (error) {
      console.error(error);
    }
  },
  methods: {
    async getTheatres() {
      const response = await api.get("/theatres");
      return response.data; // Return the data from the response
    },
  },

  //   async created() {
  //     this.theatres = await this.getTheatres();
  //   },
  //   methods: {
  //     async getTheatres() {
  //       return await api.get("/theatres");
  //     },
  //   },
};
</script> -->