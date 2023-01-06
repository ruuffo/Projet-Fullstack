<template>

  <body>
    <h1>Super QUIZ</h1>
    <div class="container">
      <h2>Resultats :</h2>

      <div v-for="scoreEntry in registeredScores" v-bind:key="scoreEntry.date">
        {{ scoreEntry.playerName }} - {{ scoreEntry.score }}
      </div>
      <br>
      <button>
        <router-link to="/newquiz">
          <div class="bt">Participer au quiz</div>
        </router-link>
      </button>
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

h1 {
  font-size: 2em;
  margin-bottom: 0.5em;
}

h2 {
  font-size: 1.5em;
  margin-top: 0;
  margin-bottom: 0.5em;
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
