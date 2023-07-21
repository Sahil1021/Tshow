<template>
  <div>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet"
      integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous" />
    <nav>
      <router-link to="/">Home</router-link> |
      <template v-if="!isAuthenticated">
        <!-- Show these links only if user is not authenticated -->
        <router-link to="/signup">Signup</router-link> |
        <router-link to="/login">Login</router-link>
      </template>

      <template v-if="isAuthenticated">
        <!-- Show these links only if user is authenticated -->
        <template v-if="userRole === 'user'">
          <router-link to="/userhome">User Home</router-link> |
        </template>
        <template v-if="userRole === 'admin'">
          <router-link to="/adminhome">Admin Home</router-link> |
          <router-link to="/theatres">Manage Theatres</router-link> |
          <router-link to="/shows">Manage Shows</router-link> |
          <router-link to="/shows/create">Create Show</router-link> |
          <router-link to="/theatres/create">Create Theatres</router-link> |
        </template>

        <button class="btn btn-danger" @click="logout">Logout</button>
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
