<template>
  <div>
    <h1>Theatres List</h1>
    <ul>
      <li v-for="theatre in theatres" :key="theatre.id">
        {{ theatre.id }} - {{ theatre.name }} - {{ theatre.address }}
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
