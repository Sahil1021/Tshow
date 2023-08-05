import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/Home.vue";
import Login from "../views/Login.vue";
import Profile from "../views/Profile.vue";
import Signup from "../views/Signup.vue";
import UserHome from "../views/UserHome.vue";
import AdminHome from "../views/AdminHome.vue";
import TheatresList from "../views/TheatresList.vue";
import CreateTheatre from "../views/CreateTheatre.vue";
import CreateShow from "../views/CreateShow.vue";
import ShowList from "../views/ShowList.vue";
import EditTheatre from "../views/EditTheatre.vue";
import EditShow from "../views/EditShow.vue";
import ShowBooking from "../views/ShowBooking.vue";
import UserBookings from "../views/UserBookings.vue";
import TheatreShows from "../views/TheatreShows.vue"; // Import the component for displaying shows under a theater
import dashboard from '../views/dashboard.vue';
import MonthlyReport from '../views/MonthlyReport.vue';


const routes = [
  { path: "/", name: "Home", component: Home },
  { path: "/signup", name: "Signup", component: Signup },
  { path: "/login", name: "Login", component: Login },
  { path: "/profile", name: "Profile", component: Profile },
  {
    path: "/userhome",
    name: "UserHome",
    component: UserHome,
    meta: { requiresAuth: true, role: "user" },
  },
  {
    path: "/adminhome",
    name: "AdminHome",
    component: AdminHome,
    meta: { requiresAuth: true, role: "admin" },
  },
  {
    path: "/theatres",
    name: "TheatresList",
    component: TheatresList,
    meta: { requiresAuth: true, role: "admin" },
  },
  {
    path: "/theatres/create",
    name: "CreateTheatre",
    component: CreateTheatre,
    meta: { requiresAuth: true, role: "admin" },
  },
  {
    path: "/shows/create",
    name: "CreateShow",
    component: CreateShow,
    meta: { requiresAuth: true, role: "admin" },
  },
  {
    path: "/shows",
    name: "ShowList",
    component: ShowList,
    meta: { requiresAuth: true, role: "admin" },
  },
  {
    path: "/shows/book",
    name: "ShowBooking",
    component: ShowBooking, // Add the new component to the router
  },
  {
    path: "/theatres/edit/:id", // Add dynamic segment for theatre ID
    name: "EditTheatre",
    component: EditTheatre,
  },
  {
    path: "/shows/edit/:id", // Add dynamic segment for theatre ID
    name: "EditShow",
    component: EditShow,
  },
  {
    path: "/shows/UserBookings",
    name: "UserBookings",
    component: UserBookings,
  },
  {
    path: "/theatres/:id/shows", // Dynamic parameter to capture the theater ID
    name: "TheatreShows", // Route name
    component: TheatreShows, // Component for displaying shows under a theater
  },
  {
    path: "/dashboard", // Dynamic parameter to capture the theater ID
    name: "dashboard", // Route name
    component: dashboard, // Component for displaying shows under a theater
  },
  {
    path: '/MonthlyReport',
    component: MonthlyReport
  }
  
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  // Check if the route requires authentication and role
  if (to.matched.some((record) => record.meta.requiresAuth)) {
    const role = localStorage.getItem("role");
    if (!role || role !== to.meta.role) {
      // Role does not match or user is not authenticated
      next("/login"); // Redirect to login page
    } else {
      next(); // Proceed to the requested page
    }
  } else {
    next(); // Proceed to the requested page (no authentication required)
  }
});

export default router;
