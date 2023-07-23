<template>
  <div>
    <h1>Theatres List</h1>
    <label>Enter Region:</label>
    <input class="form-control w-25 container mb-3" v-model="searchAddress" type="text" />
    <button class="btn btn-primary mb-4" @click="searchTheatres">Search</button>
    <!-- Display the validation message if showTheatres is true and filteredTheatres is empty -->
    <!-- <p v-if="showTheatres && searchAddress.length === 0" class="text-danger">Please enter something to search.</p> -->
    <ul v-if="showTheatres && filteredTheatres.length > 0">
      <li v-for="theatre in filteredTheatres" :key="theatre.id">
        {{ theatre.name }} - {{ theatre.address }}
      </li>
    </ul>
    <p v-else-if="showTheatres">No theatres found.</p>
  </div>
</template>

<script>
import api from "../api";
// import axios from "axios";
export default {
  data() {
    return {
      theatres: [],
      filteredTheatres: [],
      searchAddress: "",
      showTheatres: false,
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
      const response = await api.get("/theatres");
      return response.data;
    },
    searchTheatres() {
      if (this.searchAddress.trim() === '') {
        this.showTheatres = false;
        this.filteredTheatres = [];
      } else {
        this.filteredTheatres = this.theatres.filter((theatre) =>
          theatre.address.toLowerCase() === this.searchAddress.toLowerCase()
        );
        this.showTheatres = true;
      }
    },
    
  },
  watch: {
    searchAddress: function (newVal) {
      if (newVal.trim() === '') {
        this.showTheatres = false;
        this.filteredTheatres = [];
      }
    },
  },
};
</script>
