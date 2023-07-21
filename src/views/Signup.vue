<template>
  <div>
    <h1 class="mb-3">Signup</h1>
    <form class="container w-25" @submit.prevent="signup">
      <label>Username:</label>
      <input class="form-control" v-model="username" type="text" required />
      <br />
      <label>Email:</label>
      <input class="form-control" v-model="email" type="email" required />
      <br />
      <label>Password:</label>
      <input class="form-control" v-model="password" type="password" required />
      <br />
      <label>Confirm Password:</label>
      <input class="form-control" v-model="confirmPassword" type="password" required />
      <br />
      <label>Role:</label>
      <select class="form-control" v-model="role" required>
        <option value="user">User</option>
        <option value="admin">Admin</option>
      </select>
      <br />
      <button class="btn btn-primary mb-3" type="submit">Signup</button>
    </form>
    Already have an account? <router-link to="/login">Login here</router-link>
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
