<template>

  <body>
    <div class="d-flex flex-column mainblock gap-3">
      <h1>Le Super QUIZ</h1>
    <div class="container">
      <h2>Top 10 des scores :</h2>

      <div v-for="(scoreEntry, index) in registeredScores" v-bind:key="scoreEntry.date">
        <div v-if="index < 10">
          {{ scoreEntry.playerName }} - {{ scoreEntry.score }}
        </div>
      </div>
      <br>
      <div class="bt">
        <button>
        <router-link to="/newquiz">
          Participer au quiz
        </router-link>
      </button>
      </div>
    </div>
    </div>
  </body>
</template>

<script>

import quizApiService from "@/services/QuizApiService";

export default {
  name: "HomePage",
  data() {
    return {
      registeredScores: []
    };
  },
  async created() {
    console.log("Composant Home page 'created'")
    var json = await quizApiService.getQuizInfo()
    this.registeredScores = json.data.scores
  }
};
</script>


<style>
.container {
  max-width: 800px;
  margin: 0 auto;
  text-align: center;
  font-size: larger;
}

.mainblock{
  font-size: 1em;
}

.bt {
  background-color: #4CAF50;
  border: none;
  color: white;
  padding: 15px 32px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  margin: 4px 2px;
  cursor: pointer;
}
</style>
