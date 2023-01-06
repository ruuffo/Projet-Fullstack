<template>
  <body>
    <container>
      <h1>Adiminstrator login</h1>
      <div>
        <p>Saisissez votre mot de passe :</p>
        <input type="text" placeholder="Password" v-model="password">

        <button @click="login"> Log in </button>

        <div v-if="errormessage != null && errormessage != ''">
          {{ errormessage }}
        </div>
      </div>
    </container>
  </body>
</template>

<script>
import quizApiService from "@/services/QuizApiService";
export default{
    name: "Login",
    data(){
        return{
          password : '',
          errormessage :''
        }
    },
    methods:{
        async login(){
          response = await quizApiService.login(this.password);
          console.log("Login with password : ", this.password);
          token = response.data.token
          print(token)
        if (token != null)
          this.$router.push('/adminTools');
        else
          this.errormessage = "Invalid password"
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
