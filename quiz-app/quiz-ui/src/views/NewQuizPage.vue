<template>
  <body>
    <div>
      <table style="text-align: center;">
        <tr><h2>Saisissez votre nom :</h2></tr>
        <tr><input type="text" placeholder="Username" v-model="username"></tr>
        <tr><button @click="launchNewQuiz">GO!</button></tr>
      </table>
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
