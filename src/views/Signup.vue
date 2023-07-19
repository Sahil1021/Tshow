<template>
  <div>
    <h1>Signup</h1>
    <form @submit.prevent="signup">
      <label>Username:</label>
      <input v-model="username" type="text" required />
      <br />
      <label>Email:</label>
      <input v-model="email" type="email" required />
      <br />
      <label>Password:</label>
      <input v-model="password" type="password" required />
      <br />
      <label>Confirm Password:</label>
      <input v-model="confirmPassword" type="password" required />
      <br />
      <label>Role:</label>
      <select v-model="role" required>
        <option value="user">User</option>
        <option value="admin">Admin</option>
      </select>
      <br />
      <button type="submit">Signup</button>
    </form>
    <router-link to="/login">Already have an account? Login here</router-link>
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
        await api.post("http://localhost:5000/api/signup", {
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
