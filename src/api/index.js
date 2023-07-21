import axios from "axios";

const apiClient = axios.create({
  baseURL: "http://localhost:5000/api",
});

export default apiClient;

// {  apiClient,
//   async createTheatre(theatreData) {
//     return await apiClient.post("/theatres", theatreData);
//   },

//   async getTheatres() {
//     return await apiClient.get("/theatres");
//   },
// }
// export default {
//   async login(credentials) {
//     return await apiClient.post("/login", credentials);
//   },

//   async createTheatre(theatreData) {
//     return await apiClient.post("/theatres", theatreData);
//   },

//   async getTheatres() {
//     return await apiClient.get("/theatres");
//   },
// };
