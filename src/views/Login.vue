<template>
  <div>
    <h1 class="mb-3">Login</h1>
    <form class="container w-25" @submit.prevent="login">
      <label>Username:</label>
      <input class="form-control" v-model="username" type="text" required />
      <br />
      <label>Password:</label>
      <input class="form-control" v-model="password" type="password" required />
      <br />
      <button class="btn btn-primary mb-3" type="submit">Login</button>
    </form>
    Don't have an account? <router-link to="/signup">Signup here</router-link>
  </div>
</template>

<script>
import api from "../api";

export default {
  data() {
    return {
      username: "",
      password: "",
    };
  },
  methods: {
    async login() {
      try {
        const response = await api.post("/login", {
          username: this.username,
          password: this.password,
        });
        const { access_token, role } = response.data;
        localStorage.setItem("access_token", access_token);
        localStorage.setItem("role", role);
        this.$root.isAuthenticated = true;
        this.$root.userRole = role;
        this.$router.push("/profile");
      } catch (error) {
        console.error(error);
      }
    },
  },
};
</script>
