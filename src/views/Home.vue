<template>
  <div class="container mt-5">
    <!-- Header Section -->
    <div class="row align-items-center">
      <div class="col-md-6">
        <h1>Welcome to Tshow</h1>
        <h3>Book Your Movie Tickets Now! Enjoy the Latest Blockbusters with Easy Booking</h3>
        <p class="lead">Book tickets for your favorite shows</p>
      </div>
      <div class="col-md-6 mb-5 animate__animated animate__fadeIn">
        <img src="../assets/main3.avif" alt="Movie Tickets" class="img-fluid rounded" />
      </div>
    </div>

    <!-- Information Cards Section -->
    <div class="row mt-5">
      <div class="col-md-4 mb-4 animate__animated animate__bounceIn">
        <div class="card h-100">
          <img src="../assets/home5.jpg" class="card-img-top " alt="Card 1">
          <div class="card-body">
            <h5 class="card-title">Easy Booking</h5>
            <p class="card-text">
              With Tshow, booking movie tickets is a breeze. Our user-friendly interface allows you to select your
              preferred showtime, choose your seats, and reserve your tickets in just a few clicks.
            </p>
          </div>
        </div>
      </div>

      <div class="col-md-4 mb-4 animate__animated animate__bounceIn">
        <div class="card h-100">
          <img src="../assets/h7.jpg" class="card-img-top h-100" alt="Card 2">
          <div class="card-body">
            <h5 class="card-title">Wide Movie Selection</h5>
            <p class="card-text">
              Explore our vast collection of movies from various genres. Whether you're a fan of action, romance,
              comedy, or thrillers, we've got it all. Discover your next cinematic adventure with Tshow.
            </p>
          </div>
        </div>
      </div>

      <div class="col-md-4 mb-4 animate__animated animate__bounceIn">
        <div class="card h-100">
          <img src="../assets/home6.jpg" class="card-img-top" alt="Card 3">
          <div class="card-body">
            <h5 class="card-title">Real-Time Updates</h5>
            <p class="card-text">
              Stay informed with real-time updates on movie schedules, new releases, and special events. Never miss
              out on the action! We keep you updated to enhance your movie-going experience.
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import 'animate.css';
export default {
  name: "Home",
};
</script>

<style>
/* Custom styles can be added here */
</style>
