<template>
  <h1>Home page</h1>

  Resultats :

  <div v-for="i in registeredScores.length">
    {{ registeredNames[i] }} - {{ registeredScores[i] }}
  </div>
  <router-link to="/start-new-quiz-page">Démarrer le quiz !</router-link>
  <router-link to="/quiz">Participer au quiz</router-link>
</template>

<script>
import quizApiService from "@/services/QuizApiService";

export default {
  name: "HomePage",
  data() {
    return {
      registeredNames: [],
      registeredScores: []
    };
  },
  async created() {
		console.log("Composant Home page 'created'")
    var json = await quizApiService.getQuizInfo()
    this.registeredNames = json.data.names
    this.registeredScores = json.data.scores
  }
};
</script>