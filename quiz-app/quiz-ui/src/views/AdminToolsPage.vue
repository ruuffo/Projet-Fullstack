<template>
  <body>
    <div class="container">
      <h1>Adiminstrator Tools</h1>

        <div v-if="token != ''">
          <p>Choisissez une option :</p>
          <button @click="gotoPostQuestionPage">Ajouter une nouvelle question</button>
        </div>

        <div v-else>
          <p>You are not logged in !</p>
          <button @click="gotoLoginPage"> Go to login page </button>
        </div>

    </div>
  </body>
</template>

<script>
import adminStorageService from "@/services/AdminStorage";
export default{
    name: "AdminTools",
    data(){
        return{
          token: adminStorageService.getToken()
      }
    },
    methods:{
        gotoLoginPage(){
          this.$router.push('/login');
        },
        gotoPostQuestionPage(){
          this.$router.push('/postquestion');
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
