<template>

  <body>
    <div class="d-flex flex-column gap-3">
      <h1>Administrator Tools</h1>
      <div v-if="token != ''">
        <p>Choisissez une option :</p>
        <div class="d-flex flex-column gap-3">
          <button @click="rebuildDB"> Rebuild database </button><br />
          <div v-if="db_rebuilt == true">
            Rebuilt database !
          </div>
          <button @click="gotoPostQuestionPage">Add a new question</button><br />
          <button @click="gotoShowQuestionsPage"> Show all questions </button><br />
        </div>
      </div>
      <div v-else>
        <p>You are not logged in !</p>
        <button @click="gotoLoginPage"> Go to login page </button><br/>
      </div>
    </div>
  </body>
</template>

<script>
import adminStorageService from "@/services/AdminStorage";
import quizApiService from "@/services/QuizApiService";
export default {
  name: "AdminTools",
  data() {
    return {
      token: adminStorageService.getToken(),
      db_rebuilt: false
    }
  },
  methods: {
    gotoLoginPage() {
      this.$router.push('/login');
    },
    gotoPostQuestionPage() {
      this.$router.push('/postquestion');
    },
    gotoShowQuestionsPage() {
      this.$router.push('/showquestions');
    },
    async rebuildDB() {
      if(confirm("Do you wish to rebuild the database ? (Useless if the tables already exist)")){
        await quizApiService.rebuildDB(this.token)
        this.db_rebuilt = true;
      }
    },
  }
}

</script>