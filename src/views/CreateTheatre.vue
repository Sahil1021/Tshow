<template>
  <div>
    <h1>Create a New Theatre</h1>
    <form class="container w-25" @submit.prevent="createTheatre">
      <label>Name:</label>
      <input class="form-control" v-model="name" type="text" required />
      <br />
      <label>Address:</label>
      <input class="form-control" v-model="address" type="text" required />
      <br />
      <label>Admin ID:</label>
      <input class="form-control" v-model="admin_id" type="number" required />
      <br />
      <label>Capacity:</label>
      <input class="form-control" v-model="capacity" type="number" required />
      <br />
      <button class="btn btn-primary" type="submit">Create Theatre</button>
    </form>
  </div>
</template>

<script>
import api from "../api";
export default {
  data() {
    return {
      name: "",
      address: "",
      admin_id: "",
      capacity: 0,
    };
  },
  methods: {
    async createTheatre() {
      try {
        const theatreData = {
          name: this.name,
          address: this.address,
          admin_id: this.admin_id,
          capacity: this.capacity,
        };
        await api.post("/theatres", theatreData);
        alert("Theatre created successfully!");
        this.$router.push("/theatres");
      } catch (error) {
        alert("Invalid ID")
        console.error(error);
      }
    },
  },
};
</script>
