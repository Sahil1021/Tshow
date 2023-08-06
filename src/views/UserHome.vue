<template>
  <div>
    <h1 class="mt-5">Theatres List</h1>
    <label>Enter Region:</label>
    <input class="form-control w-50 container mb-3" v-model="searchAddress" type="text" />
    <button class="btn btn-primary mb-4" @click="searchTheatres">Search Theatres</button>

    <ul v-if="showTheatres && filteredTheatres.length > 0">
      <div class="card w-50 container" v-for="theatre in filteredTheatres" :key="theatre.id">
        <div class="card-body">
          <h5 class="card-title">Theatre Name: {{ theatre.name }}</h5>
          <p class="card-text">Theatre Address: {{ theatre.address }}</p>
          <router-link :to="{ name: 'TheatreShows', params: { id: theatre.id } }" class="btn btn-primary">
            View Shows
          </router-link>
        </div>
      </div>
    </ul>
    <p v-else-if="showTheatres">No theatres found.</p>

    <h1 class="mt-5">Shows List</h1>
    <label>Enter Show Name:</label>
    <input class="form-control w-50 container mb-3" v-model="searchShowName" type="text" />
    <label>Enter Genre:</label>
    <input class="form-control w-50 container mb-3" v-model="searchGenre" type="text" />
    <button class="btn btn-primary mb-4" @click="searchShows">Search Shows</button>

    <ul v-if="showShows && filteredShows.length > 0">
      <li class="card w-50 container" v-for="show in filteredShows" :key="show.id">
        <div class="card-body">
          <h5 class="card-title">Show Name: {{ show.name }}</h5>
          <p class="card-text">Theatre Name: {{ show.theatre_name }}</p>
          <p class="card-text">Show Date: {{ show.date }}</p>
          <p class="card-text">Show Time: {{ show.time }}</p>
        </div>
      </li>
    </ul>
    <p v-else-if="showShows">No shows found.</p>
    <!-- <button class="btn btn-primary" @click="generateMonthlyReport">Generate Monthly Report</button> -->
    <br />
    <h1 class="mt-5">Monthly Report</h1>

    <router-link to="/MonthlyReport" class="btn btn-primary">
      Generate Monthly Report
    </router-link>

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
      const searchQuery = this.searchAddress.trim().toLowerCase();

      if (searchQuery === "") {
        this.showTheatres = false;
        this.filteredTheatres = [];
      } else {
        this.filteredTheatres = this.theatres.filter((theatre) =>
          theatre.address.toLowerCase().includes(searchQuery)
        );
        this.showTheatres = true;
      }
    },
    searchShows() {
      if (this.searchShowName.trim() === "" && this.searchGenre.trim() === "") {
        this.showShows = false;
        this.filteredShows = [];
      } else {
        const showNamePattern = new RegExp(`^${this.searchShowName.trim()}`, 'i');
        this.filteredShows = this.shows.filter(
          (show) =>
            (show.name.match(showNamePattern)) &&
            (this.searchGenre.trim() === "" || show.genre.toLowerCase().includes(this.searchGenre.toLowerCase()))
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