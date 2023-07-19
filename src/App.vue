<template>
  <div>
    <nav>
      <router-link to="/">Home</router-link> |
      <template v-if="!isAuthenticated">
        <!-- Show these links only if user is not authenticated -->
        <router-link to="/signup">Signup</router-link> |
        <router-link to="/login">Login</router-link>
      </template>
      <template v-if="isAuthenticated">
        <!-- Show these links only if user is authenticated -->
        <router-link v-if="userRole === 'user'" to="/userhome"
          >User Home</router-link
        >
        |
        <router-link v-if="userRole === 'admin'" to="/adminhome"
          >Admin Home</router-link
        >
        |
        <!-- Additional links for authenticated users -->
        <button @click="logout">Logout</button>
      </template>
    </nav>
    <router-view></router-view>
  </div>
</template>

<script>
// import api from "./api";

export default {
  data() {
    return {
      isAuthenticated: false,
      userRole: null,
    };
  },
  created() {
    // Check if user is already authenticated on page load
    const access_token = localStorage.getItem("access_token");
    const role = localStorage.getItem("role");
    if (access_token) {
      this.isAuthenticated = true;
      this.userRole = role;
    }
  },
  methods: {
    logout() {
      // Clear access token and role from local storage on logout
      localStorage.removeItem("access_token");
      localStorage.removeItem("role");
      this.isAuthenticated = false;
      this.userRole = null;
      // Redirect to the home page after logout
      this.$router.push("/");
    },
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}
</style>
