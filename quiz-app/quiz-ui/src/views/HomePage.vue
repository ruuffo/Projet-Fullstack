<template>
  <body>
    <h1>Super QUIZ</h1>
    <button>
      <router-link to="/login"> <bt>Admin Tools</bt></router-link>
    </button>

    <div class="container">
      <h2>Resultats :</h2>

      <div v-for="scoreEntry in registeredScores" v-bind:key="scoreEntry.date">
        {{ scoreEntry.playerName }} - {{ scoreEntry.score }}
      </div>
      <br>
      <button>
        <router-link to="/newquiz"> <div class="bt">Participer au quiz</div></router-link>
      </button>
    </div>
  </body>
</template>

<style scoped>
body {
  background-color: powderblue;
}

bt {
  color:black;
  text-align:center;
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