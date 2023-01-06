<template>
  <body>
    <h1>Home page</h1>

    <div class="container">
      <h2>Resultats :</h2>

      <div v-for="scoreEntry in registeredScores" v-bind:key="scoreEntry.date">
        {{ scoreEntry.playerName }} - {{ scoreEntry.score }}
      </div>
      <br>
      <button>
        <router-link to="/newquiz">Participer au quiz</router-link>
      </button>
    </div>
  </body>
</template>

<style scoped>
body {
  background-color: powderblue;
}

h1 {
  color: blue;
  text-align: center;
}

.container{
  text-align: center;
}

h2{
  color: darkgreen;
  text-align: center;
}

div{
  text-align: center;
}

p {
  color: red;
}
</style>


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