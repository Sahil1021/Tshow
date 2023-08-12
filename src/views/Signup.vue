<template>
  <div class="container">
    <div class="row">
      <div class="col-md-12">
        <!-- Add a wrapper div and apply padding to it for more margin -->
        <div class="form-container">
          <div class="row align-items-center">
            <!-- Left Column with Image -->
            <div class="col-md-6">
              <img src="../assets/signup.jpg" alt="Signup Image" class="img-fluid rounded" />
            </div>

            <!-- Right Column with Form -->
            <div class="ri col-md-6">
              <h1>Signup</h1>
              <form @submit.prevent="signup">
                <label>Username:</label>
                <input class="form-control mb-3" v-model="username" type="text" required />

                <label>Email:</label>
                <input class="form-control mb-3" v-model="email" type="email" required />

                <label>Password:</label>
                <input class="form-control mb-3" v-model="password" type="password" required />

                <label>Confirm Password:</label>
                <input class="form-control mb-3" v-model="confirmPassword" type="password" required />

                <label>Role:</label>
                <select class="form-control mb-3" v-model="role" required>
                  <option value="user">User</option>
                  <option value="admin">Admin</option>
                </select>

                <button class="btn btn-primary" type="submit">Signup</button>
              </form>

              <p>Already have an account? <router-link to="/login">Login here</router-link></p>
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
      email: "",
      password: "",
      confirmPassword: "",
      role: "",
    };
  },
  methods: {
    async signup() {
      if (this.password !== this.confirmPassword) {
        alert("Passwords do not match");
        return;
      }

      try {
        await api.post("/signup", {
          username: this.username,
          email: this.email,
          password: this.password,
          role: this.role, // or 'admin' depending on your signup logic
        });
        alert("Signup successful! Please login.");
        this.$router.push("/login");
      } catch (error) {
        console.error(error);
      }
    },
  },
};
</script>


<style>
.ri {
  width: 35% !important;
}
</style>