<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <header>
    <div class="wrapper">
      <nav>
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/login">Login</RouterLink>
        <RouterLink to="/admintools">Tools</RouterLink>
        <RouterLink to="/about">About</RouterLink>
        <RouterLink v-if="isConnected" tp="/disconnect">Disconnect</RouterLink>
      </nav>
    </div>
  </header>
  <RouterView />
</template>
<style>
nav {
  display: flex;
  justify-content: center;
}

nav a {
  font-size: larger;
  margin: 1rem;
}
</style>
