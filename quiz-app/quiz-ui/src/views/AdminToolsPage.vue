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
export default {
  name: "AdminTools",
  data() {
    return {
      token: adminStorageService.getToken()
    }
  },
  methods: {
    gotoLoginPage() {
      this.$router.push('/login');
    },
    gotoPostQuestionPage() {
      this.$router.push('/postquestion');
    }
  }
}

</script>