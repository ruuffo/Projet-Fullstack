<template>

  <body>
      <div class="d-flex flex-column gap-3">
        <h1>Administrator login</h1>
        <p>Saisissez votre mot de passe :</p>
        <input type="password" placeholder="Password" v-model="password">

        <button @click="loginwithpassword"> Log in </button>

        <div v-if="errormessage != undefined && errormessage != null && errormessage != ''">
          {{ errormessage }}
        </div>
      </div>
  </body>
</template>

<script>
import quizApiService from "@/services/QuizApiService";
import adminStorageService from "@/services/AdminStorage";
export default {
  name: "Login",
  data() {
    return {
      password: '',
      errormessage: ''
    }
  },
  methods: {
    async loginwithpassword() {
      var token = "";
      try {
        var response = await quizApiService.login(this.password);
        this.errormessage = '';
        token = response.data.token;
      }
      catch (e) {
        this.errormessage = "Invalid password";
        this.password = '';
      }
      finally {
        adminStorageService.saveToken(token);
        if (adminStorageService.getToken() != "")
          this.$router.push('/adminTools');
      }
    }
  }
}


</script>

<style>
.container {
  max-width: 400px;
  margin: 0 auto;
  text-align: center;
}

h1 {
  font-size: 1.5em;
  margin-bottom: 0.5em;
}

input {
  display: block;
  margin: 0 auto;
  padding: 0.5em;
  font-size: 1em;
  border: 1px solid #ddd;
}

button {
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
