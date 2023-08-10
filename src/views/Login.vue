<template>
  <div class="container">
    <div class="row">
      <div class="col-md-12">
        <!-- Add a wrapper div and apply padding to it for more margin -->
        <div class="form-container">
          <div class="row align-items-center">
            <!-- Left Column with Image -->
            <div class="col-md-6">
              <img src="../assets/login.svg" alt="Login Image" class="img-fluid rounded" />
            </div>

            <!-- Right Column with Form -->
            <div class="col-md-6 ri">
              <h1 class="mb-3">Login</h1>
              <div v-if="errorMessage" class="alert alert-danger mb-3">
                {{ errorMessage }}
              </div>

              <form @submit.prevent="login">
                <label>Username:</label>
                <input class="form-control mb-3" v-model="username" type="text" required />

                <label>Password:</label>
                <input class="form-control mb-3" v-model="password" type="password" required />

                <button class="btn btn-primary" type="submit">Login</button>
              </form>

              <p>Don't have an account? <router-link to="/signup">Signup here</router-link></p>

            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from "../api";

export default {
  data() {
    return {
      username: "",
      password: "",
      errorMessage: "",
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
        // Set the error message to be displayed
        this.errorMessage = "Invalid credentials. Please try again.";
        console.error(error);
      }
    },
  },
};
</script>

<style>
/* Custom styles can be added here if needed */
.ri {
  width: 35% !important;
}
</style>
