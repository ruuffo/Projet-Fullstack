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
  flex-direction: column;
  align-items: center;
}

nav a {
  font-size: 3rem;
  margin: 1rem 0;
}
</style>

