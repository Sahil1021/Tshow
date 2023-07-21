<template>
  <div>
    <h1>Login</h1>
    <form @submit.prevent="login">
      <label>Username:</label>
      <input v-model="username" type="text" required />
      <br />
      <label>Password:</label>
      <input v-model="password" type="password" required />
      <br />
      <button type="submit">Login</button>
    </form>
    <router-link to="/signup">Don't have an account? Signup here</router-link>
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
