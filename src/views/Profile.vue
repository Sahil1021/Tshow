<template>
  <div>
    <h1>Profile</h1>
    <p>Username: {{ username }}</p>
    <p>Role: {{ role }}</p>
    <p>Email: {{ email }}</p>

    <p v-if="role === 'admin'">Admin ID: {{ id }}</p>
  </div>
</template>

<script>
import api from "../api";

export default {
  data() {
    return {
      username: "",
      role: "",
      email: "",
      id: "",
    };
  },
  async created() {
    try {
      const response = await api.get("/profile", {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("access_token")}`,
        },
      });
      const { username, role, email, id } = response.data;
      this.username = username;
      this.role = role;
      this.email = email;
      this.id = id;
    } catch (error) {
      console.error(error);
    }
  },
};
</script>
