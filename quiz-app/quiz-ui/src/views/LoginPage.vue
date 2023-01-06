<template>
  <body>
    <div class="container">
      <h1>Adiminstrator login</h1>
      <div>
        <p>Saisissez votre mot de passe :</p>
        <input type="text" placeholder="Password" v-model="password">

        <button @click="loginwithpassword"> Log in </button>

        <div v-if="errormessage != undefined && errormessage != null && errormessage != ''">
          {{ errormessage }}
        </div>
      </div>
    </div>
  </body>
</template>

<script>
import quizApiService from "@/services/QuizApiService";
import adminStorageService from "@/services/AdminStorage";
export default{
    name: "Login",
    data(){
        return{
          password : '',
          errormessage :''
        }
    },
    methods:{
        async loginwithpassword(){
          var token = "";
          try{
            var response = await quizApiService.login(this.password);
            this.errormessage = ''
            token = response.data.token
          }
          catch(e){
            this.errormessage = "Invalid password"
          }
          finally{
            adminStorageService.saveToken(token)
            if (adminStorageService.getToken() != "")
              this.$router.push('/adminTools');
          }
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
