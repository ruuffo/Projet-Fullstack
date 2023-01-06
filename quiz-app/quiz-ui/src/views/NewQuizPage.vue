<template>

  <body>
    <div class="name">
      <p>Saisissez votre nom :</p>
      <input type="text" placeholder="Username" v-model="username">
      <button @click="launchNewQuiz">GO!</button>
    </div>
  </body>
</template>

<script>
import participationStorageService from "@/services/ParticipationStorageService";
export default {
  name: "NewQuiz",
  data() {
    return {
      username: ''
    }
  },
  methods: {
    launchNewQuiz() {
      participationStorageService.savePlayerName(this.username);
      console.log("Launch new quiz with", this.username);
      this.$router.push('/quiz');
    }
  }
}

</script>
