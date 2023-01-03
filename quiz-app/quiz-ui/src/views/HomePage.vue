<template>
  <h1>Home page</h1>
  Resultats : {{ registeredScores }}
  <div v-for="scoreEntry in registeredScores" v-bind:key="scoreEntry.date">
    {{scoreEntry.Player_Name}} - {{scoreEntry.score}}
  </div>
  <router-link to="/start-new-quiz-page">Démarrer le quiz !</router-link>
</template>

<script>
import quizApiService from "@/services/QuizApiService";

export default {
  name: "HomePage",
  data() {
    return {
      registeredScores : []
    };
  },
  async created() {
		console.log("Composant Home page 'created'")
    this.registeredScores.push(0)
  }
};
</script>

<style>
</style>