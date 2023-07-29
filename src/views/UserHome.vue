<template>
  <div>
    <h1>Theatres List</h1>
    <label>Enter Region:</label>
    <input class="form-control w-25 container mb-3" v-model="searchAddress" type="text" />
    <button class="btn btn-primary mb-4" @click="searchTheatres">Search Theatres</button>
    <!-- Display the validation message if showTheatres is true and filteredTheatres is empty -->
    <!-- <p v-if="showTheatres && searchAddress.length === 0" class="text-danger">Please enter something to search.</p> -->
    <ul v-if="showTheatres && filteredTheatres.length > 0">
      <div class="card w-25 container" v-for="theatre in filteredTheatres" :key="theatre.id">
        <div class="card-body">
          <h5 class="card-title">{{ theatre.name }}</h5>
          <p class="card-text">{{ theatre.address }}</p>
          <!-- Add the button to view shows for the theater -->
          <router-link :to="{ name: 'TheatreShows', params: { id: theatre.id } }" class="btn btn-primary">
            View Shows
          </router-link>
        </div>
      </div>
    </ul>
    <p v-else-if="showTheatres">No theatres found.</p>
    <h1>Shows List</h1>
    <label>Enter Show Name:</label>
    <input class="form-control w-25 container mb-3" v-model="searchShowName" type="text" />
    <label>Enter Genre:</label>
    <input class="form-control w-25 container mb-3" v-model="searchGenre" type="text" />
    <button class="btn btn-primary mb-4" @click="searchShows">Search Shows</button>
    <!-- Display the validation message if showShows is true and filteredShows is empty -->
    <!-- <p v-if="showShows && searchShowName.length === 0" class="text-danger">Please enter something to search.</p> -->
    <ul v-if="showShows && filteredShows.length > 0">
      <li v-for="show in filteredShows" :key="show.id">
        {{ show.name }} - {{ show.theatre_name }} - {{ show.date }} - {{ show.time }}
      </li>
    </ul>
    <p v-else-if="showShows">No shows found.</p>
  </div>
</template>

<script>
import api from "../api";

export default {
  data() {
    return {
      theatres: [],
      filteredTheatres: [],
      searchAddress: "",
      showTheatres: false,

      shows: [],
      filteredShows: [],
      searchShowName: "",
      searchGenre: "",
      showShows: false,
    };
  },
  async created() {
    try {
      this.theatres = await this.getTheatres();
      this.shows = await this.getShows();
    } catch (error) {
      console.error(error);
    }
  },
  methods: {
    async getTheatres() {
      const response = await api.get("/theatres");
      return response.data;
    },
    async getShows() {
      const response = await api.get("/shows");
      return response.data;
    },
    searchTheatres() {
      if (this.searchAddress.trim() === "") {
        this.showTheatres = false;
        this.filteredTheatres = [];
      } else {
        this.filteredTheatres = this.theatres.filter(
          (theatre) =>
            theatre.address.toLowerCase() === this.searchAddress.toLowerCase()
        );
        this.showTheatres = true;
      }
    },
    searchShows() {
      if (this.searchShowName.trim() === "" && this.searchGenre.trim() === "") {
        this.showShows = false;
        this.filteredShows = [];
      } else {
        this.filteredShows = this.shows.filter(
          (show) =>
            show.name.toLowerCase().includes(this.searchShowName.toLowerCase()) &&
            show.genre.toLowerCase().includes(this.searchGenre.toLowerCase())
        );
        this.showShows = true;
      }
    },
  },
  watch: {
    searchAddress: function (newVal) {
      if (newVal.trim() === "") {
        this.showTheatres = false;
        this.filteredTheatres = [];
      }
    },
    searchShowName: function (newVal) {
      if (newVal.trim() === "" && this.searchGenre.trim() === "") {
        this.showShows = false;
        this.filteredShows = [];
      }
    },
    searchGenre: function (newVal) {
      if (newVal.trim() === "" && this.searchShowName.trim() === "") {
        this.showShows = false;
        this.filteredShows = [];
      }
    },
  },
};
</script>