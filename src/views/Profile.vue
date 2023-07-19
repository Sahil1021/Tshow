<template>
  <div>
    <h1>Profile</h1>
    <p>Username: {{ username }}</p>
    <p>Role: {{ role }}</p>
  </div>
</template>

<script>
import api from "../api";

export default {
  data() {
    return {
      username: "",
      role: "",
    };
  },
  async created() {
    try {
      const response = await api.get("http://localhost:5000/api/profile", {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("access_token")}`,
        },
      });
      const { username, role } = response.data;
      this.username = username;
      this.role = role;
    } catch (error) {
      console.error(error);
    }
  },
};
</script>
