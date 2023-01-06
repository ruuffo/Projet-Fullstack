<script setup>
import { RouterLink, RouterView } from 'vue-router'
import adminStorageService from "@/services/AdminStorage";
function isConnected() {
  return adminStorageService.getToken() === '' ? false : true
}
</script>

<template>
  <header>
    <div class="wrapper">
      <nav>
        <RouterLink to="/">Home</RouterLink>
        <RouterLink v-if="!isConnected()" :key="$route.fullPath" to="/login">Login</RouterLink>
        <RouterLink v-if="isConnected()" :key="$route.fullPath" to="/disconnect">Disconnect</RouterLink>
        <RouterLink to="/admintools">Tools</RouterLink>
        <RouterLink to="/about">About</RouterLink>
      </nav>
    </div>
  </header>
  <RouterView />
</template>
<style>
nav {
  display: flex;
  align-items: center;
}

nav a {
  font-size: 2rem;
  margin: 1rem 0;
  margin-left: 1rem;
  margin-right: 1rem;
}
</style>

