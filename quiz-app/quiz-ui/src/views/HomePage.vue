<template>
  <h1>Home page</h1>

  Resultats :

  <div v-for="i in registeredScores.length">
    {{ registeredNames[i] }} - {{ registeredScores[i] }}
  </div>
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