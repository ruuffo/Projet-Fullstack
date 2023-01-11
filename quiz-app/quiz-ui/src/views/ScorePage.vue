<template>
  <body>
    <div class="score">
      <h1>{{ playerName }}, Votre dernier score est: {{ score }} </h1>
      <p> Vous êtes {{ classement }} dans le classement ! </p>
      <h2>Top 10 des scores globaux:</h2>
      <div v-for="(scoreEntry, index) in registeredScores" :key="index" v-bind:key="scoreEntry.date" >
        <div v-if="index < 10">
          {{ scoreEntry.playerName }} - {{ scoreEntry.score }}
        </div>
      </div>
      <button @click="goHome">Retour à la page d'accueil</button>
    </div>
  </body>
</template>

<script>
import participationStorageService from "@/services/ParticipationStorageService";
import quizApiService from "@/services/QuizApiService";
export default {
  name: "ScorePage",
  data() {
    return {
      score: 0,
      playerName: '',
      classement: '',
      registeredScores: []
    }
  },
  async created() {
    console.log("Composant Score 'created'")
    this.playerName = participationStorageService.getPlayerName()
    this.score = participationStorageService.getParticipationScore()
    var json = await quizApiService.getQuizInfo()
    this.registeredScores = json.data.scores
    var rank = 1
    for (var scoreEntry of this.registeredScores) {
      if (scoreEntry.playerName === this.playerName) {
        break;
      }
      rank++
    }
    this.classement = rank
    this.classement += (rank === 1) ? "er" : "eme"
  },
  methods: {
    goHome() {
      this.$router.push('/');
    }
  }
}

</script>
<style>
.score {
  max-width: 800px;
  margin: 0 auto;
  text-align: center;
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
</style>
