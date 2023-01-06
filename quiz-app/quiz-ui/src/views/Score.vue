<template>
    <body>
    <div class="score">
      <h1>{{playerName}}, Votre dernier score est: {{score}} </h1>
      <p> Vous êtes {{Classement}} dans le classement ! </p>
      <h2>Classement des scores globaux:</h2>
      <div v-for="scoreEntry in registeredScores" v-bind:key="scoreEntry.date">
        {{ scoreEntry.playerName }} - {{ scoreEntry.score }}
      </div>
      <button @click="goHome"></button>
    </div>
    </body>
</template>

<script>
import participationStorageService from "@/services/ParticipationStorageService";
export default{
    name: "Score",
    data(){
        return{
            score: 0,
            playerName: '',
            classement: '',
            registeredScores: []
        }
    },
    methods:{
        goHome(){
            this.$router.push('/');
        }
    },
    async created() {
		console.log("Composant Score 'created'")
        this.playerName = participationStorageService.getPlayerName()
        this.score = participationStorageService.getParticipationScore()
        var json = await quizApiService.getQuizInfo()
        this.registeredScores = json.data.scores
        var rank = 1
        for(score in registeredScores){
            if(score.playerName === this.playerName){
                this.classement = rank
                break;
            }
            rank++
        }
        this.classement = this.classement === 1 ? "1 er":this.classement+" eme"
    }
}
</script>
  
  <style scoped>
  @media (min-width: 1024px) {
    .about {
      min-height: 100vh;
      display: flex;
      align-items: center;
    }
  }
  
  body {
    background-color: powderblue;
  }
  
  h1 {
    color: blue;
    text-align: center;
  }
  
  .container {
    text-align: center;
  }
  
  h2 {
    color: darkgreen;
    text-align: center;
  }
  
  div {
    text-align: center;
  }
  
  p {
    color: red;
  }
  </style>