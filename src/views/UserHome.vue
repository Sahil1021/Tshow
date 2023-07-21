<!-- App.vue -->
<template>
  <div>
    <h1>Theatres List</h1>
    <label>Enter Region:</label>
    <input class="form-control w-25 container mb-3" v-model="searchAddress" type="text" />
    <button class="btn btn-primary" @click="searchTheatres">Search</button>
    <ul v-if="showTheatres">
      <li v-for="theatre in filteredTheatres" :key="theatre.id">
        {{ theatre.name }} - {{ theatre.address }}
      </li>
    </ul>
  </div>
</template>

<script>
import api from "../api";

export default {
  data() {
    return {
      theatres: [],
      filteredTheatres: [], // Store filtered theaters separately
      searchAddress: "", // Input to store the search address
      showTheatres: false, // Flag to show/hide the theaters
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
    searchTheatres() {
      this.filteredTheatres = this.theatres.filter(theatre =>
        theatre.address.toLowerCase().includes(this.searchAddress.toLowerCase())
      );
      this.showTheatres = true; // Show the filtered theaters after search
    },
  },
};
</script>


<!-- 
<template>
  <div>
    <h1>Theatres List</h1>
    <label>Enter Address:</label>
    <input v-model="searchAddress" type="text" @input="filterTheatres" />
    <ul>
      <li v-for="theatre in filteredTheatres" :key="theatre.id">
        {{ theatre.name }} - {{ theatre.address }}
      </li>
    </ul>
  </div>
</template>

<script>
import api from "../api";

export default {
  data() {
    return {
      theatres: [],
      searchAddress: "", // Input to store the search address
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
    filterTheatres() {
      // Filter the theaters based on the search address
      this.filteredTheatres = this.theatres.filter(theatre =>
        theatre.address.toLowerCase().includes(this.searchAddress.toLowerCase())
      );
    },
  },
  
};
</script> -->
