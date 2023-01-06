<template>
  <body>
    <div class="name">
      <p>Saisissez votre nom :</p>
        <input type="text" placeholder="Username" v-model="username">
        <button @click="launchNewQuiz">GO!</button>
    </div>
  </body>
</template>

<script>
import participationStorageService from "@/services/ParticipationStorageService";
export default{
    name: "NewQuiz",
    data(){
        return{
            username : ''
        }
    },
    methods:{
        launchNewQuiz(){
            participationStorageService.savePlayerName(this.username);
            console.log("Launch new quiz with", this.username);
            this.$router.push('/quiz');
        }
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
