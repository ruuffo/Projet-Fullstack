<template>
  <h1>Home page</h1>
  {{ registeredScores }}
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