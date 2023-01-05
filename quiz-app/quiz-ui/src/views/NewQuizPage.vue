<template>
  <div class="name">
    <p>Saisissez votre nom :</p>
      <input type="text" placeholder="Username" v-model="username">
      <p>{{ username }}</p> 
      <button>GO!</button>
  </div>
</template>

<script>
  var username = '';

</script>


<style>
@media (min-width: 1024px) {
  .about {
    min-height: 100vh;
    display: flex;
    align-items: center;
  }
}
</style>
