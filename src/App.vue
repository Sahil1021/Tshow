<template>
  <div>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet"
      integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous" />
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <div class="container">
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"
          aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse justify-content-center" id="navbarNav">
          <ul class="navbar-nav">
            <router-link class="navbar-brand" to="/">Home</router-link>

            <template v-if="!isAuthenticated">
              <!-- Show these links only if the user is not authenticated -->
              <li class="nav-item">
                <router-link class="nav-link" to="/signup">Signup</router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link" to="/login">Login</router-link>
              </li>
            </template>
            <template v-if="isAuthenticated">
              <!-- Show these links only if the user is authenticated -->
              <template v-if="userRole === 'user'">
                <li class="nav-item">
                  <router-link class="nav-link" to="/userhome">User Home</router-link>
                </li>
                <li class="nav-item">
                  <router-link class="nav-link" to="/shows/book">Book show</router-link>
                </li>
                <li class="nav-item">
                  <router-link class="nav-link" to="/shows/UserBookings">My Bookings</router-link>
                </li>
              </template>

              <template v-if="userRole === 'admin'">
                <li class="nav-item">
                  <router-link class="nav-link" to="/adminhome">Admin Home</router-link>
                </li>
                <li class="nav-item">
                  <router-link class="nav-link" to="/theatres">Manage Theatres</router-link>
                </li>
                <li class="nav-item">
                  <router-link class="nav-link" to="/shows">Manage Shows</router-link>
                </li>
                <li class="nav-item">
                  <router-link class="nav-link" to="/shows/create">Create Show</router-link>
                </li>
                <li class="nav-item">
                  <router-link class="nav-link" to="/theatres/create">Create Theatres</router-link>
                </li>
                <li class="nav-item">
                  <router-link class="nav-link" to="/dashboard">CSVs</router-link>
                </li>
              </template>
            </template>
          </ul>
        </div>
        <div class="ms-auto">
          <button class="btn btn-danger" @click="logout" v-if="isAuthenticated">Logout</button>
        </div>
      </div>
    </nav>
    <router-view></router-view>
  </div>
</template>

<script>
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


<!-- cd /mnt/c/Users/MYPC/Desktop/vue5_merge-cloned -->
<!-- -->
